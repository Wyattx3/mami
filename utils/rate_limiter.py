"""
Token Bucket Rate Limiter for Telegram API
Allows burst sending while maintaining safe long-term rate
"""
import time
import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TokenBucketRateLimiter:
    """
    Token Bucket algorithm for rate limiting
    
    Telegram limits: ~30 msg/s official, but ~20 msg/s safe in practice
    We use conservative 15 msg/s to avoid any issues
    """
    
    def __init__(
        self, 
        rate: float = 15.0,  # messages per second
        capacity: float = 20.0  # bucket capacity (allows small bursts)
    ):
        self.rate = rate  # tokens added per second
        self.capacity = capacity  # max tokens in bucket
        self.tokens = capacity  # current tokens
        self.last_update = time.time()
        self.lock = asyncio.Lock()
        
        logger.info(
            f"Rate limiter initialized: {rate} msg/s, "
            f"burst capacity: {capacity} messages"
        )
    
    async def acquire(self, tokens: int = 1) -> bool:
        """
        Acquire tokens to send messages
        
        Args:
            tokens: Number of tokens needed (usually 1 per message)
            
        Returns:
            True when tokens acquired (after waiting if needed)
        """
        async with self.lock:
            while True:
                # Refill tokens based on time passed
                now = time.time()
                elapsed = now - self.last_update
                self.tokens = min(
                    self.capacity,
                    self.tokens + elapsed * self.rate
                )
                self.last_update = now
                
                # Check if we have enough tokens
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True
                
                # Calculate wait time needed
                tokens_needed = tokens - self.tokens
                wait_time = tokens_needed / self.rate
                
                logger.debug(
                    f"Rate limit: waiting {wait_time:.2f}s "
                    f"(have {self.tokens:.1f}, need {tokens})"
                )
                
                # Wait outside the lock to allow other tasks
                await asyncio.sleep(wait_time)
    
    def get_status(self) -> dict:
        """Get current rate limiter status"""
        now = time.time()
        elapsed = now - self.last_update
        current_tokens = min(
            self.capacity,
            self.tokens + elapsed * self.rate
        )
        
        return {
            'tokens': current_tokens,
            'capacity': self.capacity,
            'rate': self.rate,
            'percentage': (current_tokens / self.capacity) * 100
        }


# Global rate limiter instance
rate_limiter = TokenBucketRateLimiter(rate=15.0, capacity=20.0)

