"""
Database Transaction Manager
Ensures atomic operations and data consistency
"""
import logging
from typing import Optional, Callable, Any
from contextlib import asynccontextmanager
import asyncpg
from database.db_manager import db_manager

logger = logging.getLogger(__name__)


class TransactionManager:
    """Manages database transactions with rollback support"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @asynccontextmanager
    async def transaction(self, isolation_level: str = 'read_committed'):
        """
        Context manager for database transactions
        
        Usage:
            async with transaction_manager.transaction():
                # All operations here are atomic
                await some_db_operation()
                await another_db_operation()
                # If any operation fails, all will rollback
        
        Args:
            isolation_level: Transaction isolation level
                - 'read_uncommitted'
                - 'read_committed' (default)
                - 'repeatable_read'
                - 'serializable'
        """
        conn = await db_manager.pool.acquire()
        transaction = None
        
        try:
            # Start transaction
            transaction = conn.transaction(isolation=isolation_level)
            await transaction.start()
            
            self.logger.debug(f"Transaction started (isolation: {isolation_level})")
            
            # Yield connection for operations
            yield conn
            
            # Commit transaction
            await transaction.commit()
            self.logger.debug("Transaction committed successfully")
            
        except Exception as e:
            # Rollback on error
            if transaction:
                await transaction.rollback()
                self.logger.warning(f"Transaction rolled back due to error: {e}")
            raise
            
        finally:
            # Release connection
            await db_manager.pool.release(conn)
    
    async def execute_atomic(self, operations: list[Callable], 
                            rollback_on_error: bool = True) -> tuple[bool, Optional[Exception]]:
        """
        Execute multiple operations atomically
        
        Args:
            operations: List of async functions to execute
            rollback_on_error: Whether to rollback all on error
        
        Returns:
            (success, error) tuple
        
        Example:
            async def op1():
                await db_manager.deduct_coins(user_id, 100)
            
            async def op2():
                await db_manager.add_item(user_id, item_id)
            
            success, error = await transaction_manager.execute_atomic([op1, op2])
        """
        async with self.transaction():
            try:
                for operation in operations:
                    await operation()
                return True, None
            except Exception as e:
                self.logger.error(f"Atomic operation failed: {e}", exc_info=True)
                return False, e


class CriticalOperations:
    """
    Wrappers for critical operations that require transactions
    """
    
    def __init__(self, transaction_manager: TransactionManager):
        self.tm = transaction_manager
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def transfer_player_to_team(self, game_id: int, user_id: int, 
                                     team_number: int) -> bool:
        """
        Atomically transfer player to team
        Ensures player is removed from old team and added to new team
        """
        async with self.tm.transaction():
            try:
                conn = await db_manager.pool.acquire()
                try:
                    # Remove from any existing team
                    await conn.execute(
                        """
                        DELETE FROM team_members 
                        WHERE game_id = $1 AND user_id = $2
                        """,
                        game_id, user_id
                    )
                    
                    # Add to new team
                    await conn.execute(
                        """
                        INSERT INTO team_members (game_id, user_id, team_number)
                        VALUES ($1, $2, $3)
                        """,
                        game_id, user_id, team_number
                    )
                    
                    self.logger.info(
                        f"Player {user_id} transferred to team {team_number} in game {game_id}"
                    )
                    return True
                    
                finally:
                    await db_manager.pool.release(conn)
                    
            except Exception as e:
                self.logger.error(f"Failed to transfer player to team: {e}", exc_info=True)
                return False
    
    async def record_vote_with_validation(self, game_id: int, user_id: int, 
                                         round_number: int, character_id: int) -> tuple[bool, str]:
        """
        Atomically record vote with validation
        Checks if vote is valid before recording
        
        Returns:
            (success, message) tuple
        """
        async with self.tm.transaction():
            try:
                conn = await db_manager.pool.acquire()
                try:
                    # Check if user already voted this round
                    existing_vote = await conn.fetchval(
                        """
                        SELECT vote_id FROM votes 
                        WHERE game_id = $1 AND user_id = $2 AND round_number = $3
                        """,
                        game_id, user_id, round_number
                    )
                    
                    if existing_vote:
                        return False, "သင် ဒီ round မှာ vote ပေးပြီးသားဖြစ်ပါသည်။"
                    
                    # Check if round is still active
                    round_active = await conn.fetchval(
                        """
                        SELECT is_active FROM rounds 
                        WHERE game_id = $1 AND round_number = $2
                        """,
                        game_id, round_number
                    )
                    
                    if not round_active:
                        return False, "ဒီ round ပိတ်ပြီးဖြစ်ပါသည်။"
                    
                    # Record vote
                    await conn.execute(
                        """
                        INSERT INTO votes (game_id, user_id, round_number, character_id, voted_at)
                        VALUES ($1, $2, $3, $4, NOW())
                        """,
                        game_id, user_id, round_number, character_id
                    )
                    
                    self.logger.info(
                        f"Vote recorded: user={user_id}, game={game_id}, round={round_number}, character={character_id}"
                    )
                    return True, "✅ Vote မှတ်တမ်းတင်ပြီးပါပြီ!"
                    
                finally:
                    await db_manager.pool.release(conn)
                    
            except Exception as e:
                self.logger.error(f"Failed to record vote: {e}", exc_info=True)
                return False, "Vote မှတ်တမ်းတင်ရာတွင် အမှားဖြစ်ပေါ်ခဲ့သည်။"
    
    async def complete_round_atomically(self, game_id: int, round_number: int, 
                                       team_scores: dict) -> bool:
        """
        Atomically complete round: update scores, close round, start next round
        
        Args:
            game_id: Game ID
            round_number: Current round number
            team_scores: Dict of {team_number: score_increment}
        
        Returns:
            Success status
        """
        async with self.tm.transaction():
            try:
                conn = await db_manager.pool.acquire()
                try:
                    # Update team scores
                    for team_number, score_increment in team_scores.items():
                        await conn.execute(
                            """
                            UPDATE teams 
                            SET score = score + $1
                            WHERE game_id = $2 AND team_number = $3
                            """,
                            score_increment, game_id, team_number
                        )
                    
                    # Close current round
                    await conn.execute(
                        """
                        UPDATE rounds 
                        SET is_active = FALSE, completed_at = NOW()
                        WHERE game_id = $1 AND round_number = $2
                        """,
                        game_id, round_number
                    )
                    
                    # Check if game should end (5 rounds completed)
                    if round_number < 5:
                        # Start next round
                        await conn.execute(
                            """
                            INSERT INTO rounds (game_id, round_number, is_active, started_at)
                            VALUES ($1, $2, TRUE, NOW())
                            """,
                            game_id, round_number + 1
                        )
                        self.logger.info(f"Round {round_number} completed, Round {round_number + 1} started")
                    else:
                        # Mark game as completed
                        await conn.execute(
                            """
                            UPDATE games 
                            SET status = 'completed', ended_at = NOW()
                            WHERE game_id = $1
                            """,
                            game_id
                        )
                        self.logger.info(f"Game {game_id} completed after round {round_number}")
                    
                    return True
                    
                finally:
                    await db_manager.pool.release(conn)
                    
            except Exception as e:
                self.logger.error(f"Failed to complete round atomically: {e}", exc_info=True)
                return False
    
    async def cancel_game_with_cleanup(self, game_id: int, chat_id: int) -> bool:
        """
        Atomically cancel game and cleanup all related data
        """
        async with self.tm.transaction():
            try:
                conn = await db_manager.pool.acquire()
                try:
                    # Delete all votes
                    await conn.execute(
                        "DELETE FROM votes WHERE game_id = $1",
                        game_id
                    )
                    
                    # Delete all rounds
                    await conn.execute(
                        "DELETE FROM rounds WHERE game_id = $1",
                        game_id
                    )
                    
                    # Delete team members
                    await conn.execute(
                        "DELETE FROM team_members WHERE game_id = $1",
                        game_id
                    )
                    
                    # Delete teams
                    await conn.execute(
                        "DELETE FROM teams WHERE game_id = $1",
                        game_id
                    )
                    
                    # Delete players
                    await conn.execute(
                        "DELETE FROM players WHERE game_id = $1",
                        game_id
                    )
                    
                    # Delete game
                    await conn.execute(
                        "DELETE FROM games WHERE game_id = $1",
                        game_id
                    )
                    
                    # Clear state management
                    await conn.execute(
                        "DELETE FROM game_states WHERE chat_id = $1",
                        chat_id
                    )
                    
                    await conn.execute(
                        "DELETE FROM user_states WHERE chat_id = $1",
                        chat_id
                    )
                    
                    self.logger.info(f"Game {game_id} cancelled and cleaned up successfully")
                    return True
                    
                finally:
                    await db_manager.pool.release(conn)
                    
            except Exception as e:
                self.logger.error(f"Failed to cancel game with cleanup: {e}", exc_info=True)
                return False


# Global instances
transaction_manager = TransactionManager()
critical_ops = CriticalOperations(transaction_manager)


# Export
__all__ = [
    'TransactionManager',
    'CriticalOperations',
    'transaction_manager',
    'critical_ops'
]

