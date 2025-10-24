"""
Database manager for PostgreSQL operations (Neon)
"""
import asyncpg
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from models.character import Character
from models.game import Game, GameRound
from models.player import Player
import config

# Setup logger
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages all PostgreSQL database operations"""
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or config.DATABASE_URL
        self.pool = None
    
    async def create_pool(self):
        """Create database connection pool with proper timeout settings"""
        if not self.pool:
            logger.info("Creating database connection pool...")
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=1,
                max_size=10,
                command_timeout=60,
                timeout=30  # Connection acquisition timeout
            )
            logger.info("Database connection pool created")
    
    async def close_pool(self):
        """Close database connection pool"""
        if self.pool:
            logger.info("Closing database connection pool...")
            await self.pool.close()
            self.pool = None
            logger.info("Database connection pool closed")
    
    async def init_database(self):
        """Initialize database and create tables"""
        logger.info("Initializing database...")
        
        if not self.pool:
            await self.create_pool()
        
        # Acquire connection with explicit timeout
        conn = await self.pool.acquire(timeout=10.0)
        try:
            # Characters table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS characters (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    mbti TEXT NOT NULL,
                    zodiac TEXT NOT NULL,
                    description TEXT,
                    personality_traits TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Games table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS games (
                    id SERIAL PRIMARY KEY,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    winner_team INTEGER,
                    current_round INTEGER DEFAULT 0,
                    lobby_message_id BIGINT,
                    lobby_chat_id BIGINT,
                    theme_id INTEGER DEFAULT 1
                )
            ''')
            
            # Game players table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS game_players (
                    id SERIAL PRIMARY KEY,
                    game_id INTEGER NOT NULL,
                    user_id BIGINT NOT NULL,
                    username TEXT,
                    team_number INTEGER NOT NULL,
                    is_leader INTEGER DEFAULT 0,
                    FOREIGN KEY (game_id) REFERENCES games (id) ON DELETE CASCADE,
                    UNIQUE(game_id, user_id)
                )
            ''')
            
            # Game rounds table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS game_rounds (
                    id SERIAL PRIMARY KEY,
                    game_id INTEGER NOT NULL,
                    round_number INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    team_id INTEGER NOT NULL,
                    selected_character_id INTEGER,
                    votes TEXT,
                    score INTEGER,
                    explanation TEXT,
                    FOREIGN KEY (game_id) REFERENCES games (id) ON DELETE CASCADE,
                    FOREIGN KEY (selected_character_id) REFERENCES characters (id),
                    UNIQUE(game_id, round_number, team_id)
                )
            ''')
            
            # Lobby queue table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS lobby_queue (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL UNIQUE,
                    username TEXT,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
        finally:
            # Always release connection back to pool
            await self.pool.release(conn)
    
    # ==================== Character Operations ====================
    
    async def add_character(self, character: Character) -> int:
        """Add a new character"""
        logger.debug(f"Adding character: {character.name} (MBTI: {character.mbti}, Zodiac: {character.zodiac})")
        async with self.pool.acquire() as conn:
            char_id = await conn.fetchval(
                '''INSERT INTO characters (name, mbti, zodiac, description, personality_traits)
                   VALUES ($1, $2, $3, $4, $5) RETURNING id''',
                character.name, character.mbti, character.zodiac, 
                character.description, character.personality_traits
            )
            logger.info(f"Character added successfully: {character.name} (ID: {char_id})")
            return char_id
    
    async def get_character(self, character_id: int) -> Optional[Character]:
        """Get character by ID"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT * FROM characters WHERE id = $1',
                character_id
            )
            
            if row:
                return Character(
                    id=row['id'],
                    name=row['name'],
                    mbti=row['mbti'],
                    zodiac=row['zodiac'],
                    description=row['description'],
                    personality_traits=row['personality_traits']
                )
            return None
    
    async def get_random_characters(self, n: int = 4, exclude_ids: List[int] = None) -> List[Character]:
        """Get n random characters, optionally excluding specified IDs"""
        if exclude_ids is None:
            exclude_ids = []
        
        logger.debug(f"Fetching {n} random characters, excluding {len(exclude_ids)} IDs")
        async with self.pool.acquire() as conn:
            if exclude_ids:
                rows = await conn.fetch(
                    'SELECT * FROM characters WHERE id <> ALL($1::int[]) ORDER BY RANDOM() LIMIT $2',
                    exclude_ids, n
                )
            else:
                rows = await conn.fetch(
                    'SELECT * FROM characters ORDER BY RANDOM() LIMIT $1',
                    n
                )
            
            characters = []
            for row in rows:
                characters.append(Character(
                    id=row['id'],
                    name=row['name'],
                    mbti=row['mbti'],
                    zodiac=row['zodiac'],
                    description=row['description'],
                    personality_traits=row['personality_traits']
                ))
            
            return characters
    
    async def get_all_characters(self) -> List[Character]:
        """Get all characters"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('SELECT * FROM characters')
            
            characters = []
            for row in rows:
                characters.append(Character(
                    id=row['id'],
                    name=row['name'],
                    mbti=row['mbti'],
                    zodiac=row['zodiac'],
                    description=row['description'],
                    personality_traits=row['personality_traits']
                ))
            
            return characters
    
    async def get_character_count(self) -> int:
        """Get total number of characters"""
        async with self.pool.acquire() as conn:
            count = await conn.fetchval('SELECT COUNT(*) FROM characters')
            return count if count else 0
    
    # ==================== Lobby Operations ====================
    
    async def add_to_lobby(self, user_id: int, username: str) -> bool:
        """Add player to lobby queue"""
        logger.debug(f"Adding player to lobby: {username} (ID: {user_id})")
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(
                    'INSERT INTO lobby_queue (user_id, username) VALUES ($1, $2)',
                    user_id, username
                )
                logger.info(f"Player added to lobby: {username}")
                return True
        except asyncpg.UniqueViolationError:
            logger.warning(f"Player already in lobby: {username}")
            return False
    
    async def remove_from_lobby(self, user_id: int) -> bool:
        """Remove player from lobby queue"""
        logger.debug(f"Removing player from lobby: User ID {user_id}")
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                'DELETE FROM lobby_queue WHERE user_id = $1',
                user_id
            )
            removed = result != 'DELETE 0'
            if removed:
                logger.info(f"Player removed from lobby: User ID {user_id}")
            else:
                logger.warning(f"Player not in lobby: User ID {user_id}")
            return removed
    
    async def get_lobby_players(self) -> List[Dict[str, Any]]:
        """Get all players in lobby"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                'SELECT user_id, username FROM lobby_queue ORDER BY joined_at'
            )
            
            return [
                {'user_id': row['user_id'], 'username': row['username']}
                for row in rows
            ]
    
    async def get_lobby_count(self) -> int:
        """Get number of players in lobby"""
        async with self.pool.acquire() as conn:
            count = await conn.fetchval('SELECT COUNT(*) FROM lobby_queue')
            return count if count else 0
    
    async def clear_lobby(self, chat_id: int = None):
        """Clear all players from lobby"""
        logger.info(f"Clearing lobby queue (chat_id: {chat_id})")
        async with self.pool.acquire() as conn:
            result = await conn.execute('DELETE FROM lobby_queue')
            logger.debug(f"Cleared lobby: {result}")
    
    # ==================== Game Operations ====================
    
    async def create_game(self, lobby_message_id: int = None, lobby_chat_id: int = None, theme_id: int = 1) -> int:
        """Create a new game with theme"""
        logger.info(f"Creating new game with theme {theme_id}...")
        async with self.pool.acquire() as conn:
            game_id = await conn.fetchval(
                '''INSERT INTO games (status, created_at, lobby_message_id, lobby_chat_id, theme_id)
                   VALUES ($1, $2, $3, $4, $5) RETURNING id''',
                'lobby', datetime.now(), lobby_message_id, lobby_chat_id, theme_id
            )
            return game_id
    
    async def get_game(self, game_id: int) -> Optional[Game]:
        """Get game by ID"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT * FROM games WHERE id = $1',
                game_id
            )
            
            if row:
                return Game.from_dict(dict(row))
            return None
    
    async def update_game_status(self, game_id: int, status: str):
        """Update game status"""
        logger.debug(f"Updating game {game_id} status to: {status}")
        async with self.pool.acquire() as conn:
            await conn.execute(
                'UPDATE games SET status = $1 WHERE id = $2',
                status, game_id
            )
        logger.info(f"Game {game_id} status updated to: {status}")
    
    async def update_game_round(self, game_id: int, round_number: int):
        """Update current round"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                'UPDATE games SET current_round = $1 WHERE id = $2',
                round_number, game_id
            )
    
    async def get_game_theme(self, game_id: int) -> int:
        """Get theme ID for a game"""
        async with self.pool.acquire() as conn:
            theme_id = await conn.fetchval(
                'SELECT theme_id FROM games WHERE id = $1',
                game_id
            )
            return theme_id if theme_id else 1
    
    async def set_game_winner(self, game_id: int, team_number: int):
        """Set game winner"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                'UPDATE games SET winner_team = $1, status = $2 WHERE id = $3',
                team_number, 'finished', game_id
            )
    
    # ==================== Game Players Operations ====================
    
    async def add_game_players(self, game_id: int, players: List[Dict[str, Any]]):
        """Add players to a game with team assignments and leader status"""
        logger.debug(f"Adding {len(players)} players to game {game_id}")
        async with self.pool.acquire() as conn:
            for player in players:
                await conn.execute(
                    '''INSERT INTO game_players (game_id, user_id, username, team_number, is_leader)
                       VALUES ($1, $2, $3, $4, $5)''',
                    game_id, player['user_id'], player['username'], player['team_number'], 
                    int(player.get('is_leader', False))
                )
        logger.info(f"Added {len(players)} players to game {game_id}")
    
    async def get_game_players(self, game_id: int) -> Dict[int, List[Dict[str, Any]]]:
        """Get all players in a game, organized by team"""
        logger.debug(f"Getting players for game {game_id}")
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                '''SELECT user_id, username, team_number, is_leader 
                   FROM game_players 
                   WHERE game_id = $1 
                   ORDER BY team_number, id''',
                game_id
            )
            
            teams = {}
            for row in rows:
                team_num = row['team_number']
                if team_num not in teams:
                    teams[team_num] = []
                teams[team_num].append({
                    'user_id': row['user_id'],
                    'username': row['username'],
                    'is_leader': bool(row['is_leader'])
                })
            
            logger.debug(f"Found {len(teams)} teams with total {sum(len(p) for p in teams.values())} players")
            return teams
    
    async def is_user_in_game(self, game_id: int, user_id: int) -> bool:
        """Check if user is in a specific game"""
        logger.debug(f"Checking if user {user_id} is in game {game_id}")
        async with self.pool.acquire() as conn:
            count = await conn.fetchval(
                'SELECT COUNT(*) FROM game_players WHERE game_id = $1 AND user_id = $2',
                game_id, user_id
            )
            is_in_game = count > 0
            logger.debug(f"User {user_id} in game {game_id}: {is_in_game}")
            return is_in_game
    
    # ==================== Game Rounds Operations ====================
    
    async def save_round_selection(self, game_id: int, round_number: int, 
                                   team_id: int, role: str, character_id: int, 
                                   votes: Dict[int, int]):
        """Save round selection"""
        logger.debug(f"Saving round selection - Game: {game_id}, Round: {round_number}, Team: {team_id}, Character: {character_id}")
        votes_json = json.dumps(votes)
        async with self.pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO game_rounds 
                   (game_id, round_number, role, team_id, selected_character_id, votes)
                   VALUES ($1, $2, $3, $4, $5, $6)
                   ON CONFLICT (game_id, round_number, team_id) 
                   DO UPDATE SET selected_character_id = $5, votes = $6, role = $3''',
                game_id, round_number, role, team_id, character_id, votes_json
            )
        logger.info(f"Round selection saved - Game: {game_id}, Round: {round_number}, Team: {team_id}")
    
    async def get_round_votes(self, game_id: int, round_number: int, team_id: int) -> Optional[Dict[int, int]]:
        """Get individual votes for a round (user_id -> character_id)"""
        async with self.pool.acquire() as conn:
            votes_json = await conn.fetchval(
                '''SELECT votes FROM game_rounds 
                   WHERE game_id = $1 AND round_number = $2 AND team_id = $3''',
                game_id, round_number, team_id
            )
            if votes_json:
                return json.loads(votes_json)
            return None
    
    async def save_round_score(self, game_id: int, round_number: int, 
                               team_id: int, score: int, explanation: str):
        """Save round score and explanation"""
        logger.debug(f"Saving round score - Game: {game_id}, Round: {round_number}, Team: {team_id}, Score: {score}")
        async with self.pool.acquire() as conn:
            await conn.execute(
                '''UPDATE game_rounds 
                   SET score = $1, explanation = $2
                   WHERE game_id = $3 AND round_number = $4 AND team_id = $5''',
                score, explanation, game_id, round_number, team_id
            )
        logger.info(f"Round score saved - Game: {game_id}, Round: {round_number}, Team: {team_id}, Score: {score}")
    
    async def get_game_rounds(self, game_id: int) -> List[GameRound]:
        """Get all rounds for a game"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                '''SELECT * FROM game_rounds 
                   WHERE game_id = $1 
                   ORDER BY round_number, team_id''',
                game_id
            )
            
            rounds = []
            for row in rows:
                rounds.append(GameRound.from_dict(dict(row)))
            
            return rounds
    
    async def get_team_rounds(self, game_id: int, team_id: int) -> List[GameRound]:
        """Get all rounds for a specific team"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                '''SELECT * FROM game_rounds 
                   WHERE game_id = $1 AND team_id = $2 
                   ORDER BY round_number''',
                game_id, team_id
            )
            
            rounds = []
            for row in rows:
                rounds.append(GameRound.from_dict(dict(row)))
            
            return rounds
    
    async def get_game_results(self, game_id: int) -> Dict[int, Dict[str, Any]]:
        """Get final results for all teams"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                '''SELECT gr.team_id, gr.round_number, gr.role, 
                          gr.selected_character_id, gr.score, gr.explanation,
                          c.name as character_name
                   FROM game_rounds gr
                   LEFT JOIN characters c ON gr.selected_character_id = c.id
                   WHERE gr.game_id = $1
                   ORDER BY gr.team_id, gr.round_number''',
                game_id
            )
            
            results = {}
            for row in rows:
                team_id = row['team_id']
                if team_id not in results:
                    results[team_id] = {
                        'rounds': [],
                        'total_score': 0
                    }
                
                round_data = {
                    'round_number': row['round_number'],
                    'role': row['role'],
                    'character_id': row['selected_character_id'],
                    'character_name': row['character_name'],
                    'score': row['score'] or 0,
                    'explanation': row['explanation']
                }
                
                results[team_id]['rounds'].append(round_data)
                results[team_id]['total_score'] += (row['score'] or 0)
            
            return results
    
    async def get_team_used_character_ids(self, game_id: int, team_id: int) -> List[int]:
        """Get character IDs already used by a team in the current game
        
        Args:
            game_id: Game ID
            team_id: Team ID
            
        Returns:
            List of character IDs used by this team
        """
        logger.debug(f"Getting used characters for game {game_id}, team {team_id}")
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT DISTINCT selected_character_id FROM game_rounds
                WHERE game_id = $1 AND team_id = $2 AND selected_character_id IS NOT NULL
            ''', game_id, team_id)
            
            used_ids = [row['selected_character_id'] for row in rows]
            logger.debug(f"Team {team_id} has used {len(used_ids)} characters: {used_ids}")
            return used_ids
    
    async def is_user_in_active_game(self, user_id: int) -> bool:
        """Check if user is already in an active game or lobby
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if user is in an active game or lobby
        """
        logger.debug(f"Checking if user {user_id} is in active game or lobby")
        async with self.pool.acquire() as conn:
            # Check if user is in an active game
            game_count = await conn.fetchval('''
                SELECT COUNT(*) FROM game_players p
                INNER JOIN games g ON p.game_id = g.id
                WHERE p.user_id = $1 AND g.status IN ('lobby', 'in_progress')
            ''', user_id)
            
            # Check if user is in any lobby queue
            lobby_count = await conn.fetchval('''
                SELECT COUNT(*) FROM lobby_queue
                WHERE user_id = $1
            ''', user_id)
            
            is_active = (game_count > 0) or (lobby_count > 0)
            logger.debug(f"User {user_id} - Active games: {game_count}, In lobby: {lobby_count}, Total active: {is_active}")
            return is_active
    
    async def is_channel_has_active_game(self, chat_id: int) -> bool:
        """Check if channel already has an active game
        
        Args:
            chat_id: Telegram chat ID
            
        Returns:
            True if channel has an active game
        """
        logger.debug(f"Checking if channel {chat_id} has active game")
        async with self.pool.acquire() as conn:
            count = await conn.fetchval('''
                SELECT COUNT(*) FROM games
                WHERE lobby_chat_id = $1 AND status IN ('lobby', 'in_progress')
            ''', chat_id)
            
            has_active = count > 0
            logger.debug(f"Channel {chat_id} active game status: {has_active}")
            return has_active


# Global database manager instance
db_manager = DatabaseManager()
