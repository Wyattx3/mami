"""
State Management System
Persistent state management with database backend
"""
import logging
import json
from enum import Enum
from typing import Optional, Dict, Any
from database.db_manager import db_manager

logger = logging.getLogger(__name__)


class GameState(Enum):
    """Game state definitions"""
    IDLE = "idle"
    LOBBY_OPEN = "lobby_open"
    TEAMS_FORMING = "teams_forming"
    ROUND_VOTING = "round_voting"
    ROUND_RESULTS = "round_results"
    GAME_ENDED = "game_ended"
    ERROR = "error"


class UserState(Enum):
    """User state definitions"""
    MENU = "menu"
    IN_LOBBY = "in_lobby"
    PLAYING = "playing"
    VOTING = "voting"
    WAITING = "waiting"


class StateManager:
    """Manages game and user states with database persistence"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def set_game_state(self, chat_id: int, state: GameState, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Set game state for a chat
        
        Args:
            chat_id: Telegram chat ID
            state: GameState enum
            metadata: Optional additional data (e.g., round number, current players)
        
        Returns:
            bool: Success status
        """
        try:
            # Store state in database
            conn = await db_manager.pool.acquire()
            try:
                # Check if state record exists
                existing = await conn.fetchval(
                    "SELECT chat_id FROM game_states WHERE chat_id = $1",
                    chat_id
                )
                
                if existing:
                    # Update existing state
                    await conn.execute(
                        """
                        UPDATE game_states 
                        SET state = $1, metadata = $2::jsonb, updated_at = NOW()
                        WHERE chat_id = $3
                        """,
                        state.value,
                        json.dumps(metadata or {}),
                        chat_id
                    )
                else:
                    # Insert new state
                    await conn.execute(
                        """
                        INSERT INTO game_states (chat_id, state, metadata, updated_at)
                        VALUES ($1, $2, $3::jsonb, NOW())
                        """,
                        chat_id,
                        state.value,
                        json.dumps(metadata or {})
                    )
                
                self.logger.info(f"Game state set: chat_id={chat_id}, state={state.value}")
                return True
                
            finally:
                await db_manager.pool.release(conn)
                
        except Exception as e:
            self.logger.error(f"Error setting game state for chat {chat_id}: {e}", exc_info=True)
            return False
    
    async def get_game_state(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """
        Get current game state for a chat
        
        Returns:
            Dict with 'state' and 'metadata' or None
        """
        try:
            conn = await db_manager.pool.acquire()
            try:
                result = await conn.fetchrow(
                    "SELECT state, metadata FROM game_states WHERE chat_id = $1",
                    chat_id
                )
                
                if result:
                    # Parse JSON string back to dict
                    metadata = result['metadata']
                    if isinstance(metadata, str):
                        metadata = json.loads(metadata)
                    return {
                        'state': GameState(result['state']),
                        'metadata': metadata or {}
                    }
                
                # Default state if not found
                return {'state': GameState.IDLE, 'metadata': {}}
                
            finally:
                await db_manager.pool.release(conn)
                
        except Exception as e:
            self.logger.error(f"Error getting game state for chat {chat_id}: {e}", exc_info=True)
            return {'state': GameState.ERROR, 'metadata': {}}
    
    async def set_user_state(self, user_id: int, chat_id: int, state: UserState, 
                            metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Set user state
        
        Args:
            user_id: Telegram user ID
            chat_id: Telegram chat ID
            state: UserState enum
            metadata: Optional additional data (e.g., votes, team assignment)
        
        Returns:
            bool: Success status
        """
        try:
            conn = await db_manager.pool.acquire()
            try:
                # Check if state record exists
                existing = await conn.fetchval(
                    "SELECT user_id FROM user_states WHERE user_id = $1 AND chat_id = $2",
                    user_id, chat_id
                )
                
                if existing:
                    # Update existing state
                    await conn.execute(
                        """
                        UPDATE user_states 
                        SET state = $1, metadata = $2::jsonb, updated_at = NOW()
                        WHERE user_id = $3 AND chat_id = $4
                        """,
                        state.value,
                        json.dumps(metadata or {}),
                        user_id,
                        chat_id
                    )
                else:
                    # Insert new state
                    await conn.execute(
                        """
                        INSERT INTO user_states (user_id, chat_id, state, metadata, updated_at)
                        VALUES ($1, $2, $3, $4::jsonb, NOW())
                        """,
                        user_id,
                        chat_id,
                        state.value,
                        json.dumps(metadata or {})
                    )
                
                self.logger.debug(f"User state set: user_id={user_id}, chat_id={chat_id}, state={state.value}")
                return True
                
            finally:
                await db_manager.pool.release(conn)
                
        except Exception as e:
            self.logger.error(f"Error setting user state: user_id={user_id}, chat_id={chat_id}: {e}", exc_info=True)
            return False
    
    async def get_user_state(self, user_id: int, chat_id: int) -> Optional[Dict[str, Any]]:
        """
        Get current user state
        
        Returns:
            Dict with 'state' and 'metadata' or None
        """
        try:
            conn = await db_manager.pool.acquire()
            try:
                result = await conn.fetchrow(
                    "SELECT state, metadata FROM user_states WHERE user_id = $1 AND chat_id = $2",
                    user_id, chat_id
                )
                
                if result:
                    # Parse JSON string back to dict
                    metadata = result['metadata']
                    if isinstance(metadata, str):
                        metadata = json.loads(metadata)
                    return {
                        'state': UserState(result['state']),
                        'metadata': metadata or {}
                    }
                
                # Default state if not found
                return {'state': UserState.MENU, 'metadata': {}}
                
            finally:
                await db_manager.pool.release(conn)
                
        except Exception as e:
            self.logger.error(f"Error getting user state: user_id={user_id}, chat_id={chat_id}: {e}", exc_info=True)
            return {'state': UserState.MENU, 'metadata': {}}
    
    async def clear_game_state(self, chat_id: int) -> bool:
        """Clear game state (after game ends or cancellation)"""
        try:
            conn = await db_manager.pool.acquire()
            try:
                await conn.execute(
                    "DELETE FROM game_states WHERE chat_id = $1",
                    chat_id
                )
                self.logger.info(f"Game state cleared for chat_id={chat_id}")
                return True
            finally:
                await db_manager.pool.release(conn)
        except Exception as e:
            self.logger.error(f"Error clearing game state for chat {chat_id}: {e}", exc_info=True)
            return False
    
    async def clear_user_states(self, chat_id: int) -> bool:
        """Clear all user states for a chat (after game ends)"""
        try:
            conn = await db_manager.pool.acquire()
            try:
                await conn.execute(
                    "DELETE FROM user_states WHERE chat_id = $1",
                    chat_id
                )
                self.logger.info(f"User states cleared for chat_id={chat_id}")
                return True
            finally:
                await db_manager.pool.release(conn)
        except Exception as e:
            self.logger.error(f"Error clearing user states for chat {chat_id}: {e}", exc_info=True)
            return False
    
    async def init_state_tables(self):
        """Initialize state management tables in database"""
        try:
            conn = await db_manager.pool.acquire()
            try:
                # Create game_states table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS game_states (
                        chat_id BIGINT PRIMARY KEY,
                        state VARCHAR(50) NOT NULL,
                        metadata JSONB DEFAULT '{}',
                        updated_at TIMESTAMP DEFAULT NOW()
                    )
                """)
                
                # Create user_states table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_states (
                        user_id BIGINT NOT NULL,
                        chat_id BIGINT NOT NULL,
                        state VARCHAR(50) NOT NULL,
                        metadata JSONB DEFAULT '{}',
                        updated_at TIMESTAMP DEFAULT NOW(),
                        PRIMARY KEY (user_id, chat_id)
                    )
                """)
                
                # Create indexes for faster queries
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_game_states_state 
                    ON game_states(state)
                """)
                
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_user_states_user 
                    ON user_states(user_id)
                """)
                
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_user_states_chat 
                    ON user_states(chat_id)
                """)
                
                self.logger.info("State management tables initialized successfully")
                
            finally:
                await db_manager.pool.release(conn)
                
        except Exception as e:
            self.logger.error(f"Error initializing state tables: {e}", exc_info=True)
            raise


# Global state manager instance
state_manager = StateManager()

