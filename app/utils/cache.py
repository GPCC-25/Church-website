import asyncio
import logging
from typing import Any, Optional
from collections import OrderedDict

logger = logging.getLogger(__name__)

class SimpleMemoryCache:
    """In-memory cache implementation for development purposes"""
    def __init__(self, max_size=1000, default_ttl=300):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.lock = asyncio.Lock()
        
    async def init(self):
        """Initialize the cache (for interface compatibility)"""
        logger.info("Initialized in-memory cache")
        return self
        
    async def close(self):
        """Close the cache (for interface compatibility)"""
        logger.info("Closed in-memory cache")
        self.cache.clear()
        
    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a value in the cache with optional TTL"""
        async with self.lock:
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)  # Remove oldest item
                
            expire_at = asyncio.get_event_loop().time() + (ttl or self.default_ttl)
            self.cache[key] = (value, expire_at)
            logger.debug(f"Cache SET: {key}")
            
    async def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the cache if it exists and hasn't expired"""
        async with self.lock:
            if key not in self.cache:
                logger.debug(f"Cache MISS: {key}")
                return default
                
            value, expire_at = self.cache[key]
            if asyncio.get_event_loop().time() > expire_at:
                del self.cache[key]
                logger.debug(f"Cache EXPIRED: {key}")
                return default
                
            logger.debug(f"Cache HIT: {key}")
            # Move to end to mark as recently used
            self.cache.move_to_end(key)
            return value
            
    async def delete(self, key: str):
        """Delete a value from the cache"""
        async with self.lock:
            if key in self.cache:
                del self.cache[key]
                logger.debug(f"Cache DELETE: {key}")
                return True
            return False
            
    async def clear(self):
        """Clear all items from the cache"""
        async with self.lock:
            self.cache.clear()
            logger.info("Cache CLEARED")

# Create cache instance (use SimpleMemoryCache for development)
# For production, you would replace this with a Redis-based cache
cache = SimpleMemoryCache(max_size=1000, default_ttl=300)

# Decorator for caching async functions
def cached(ttl: int = 300):
    """Decorator to cache the result of an async function"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate a unique key based on function and arguments
            key = f"{func.__module__}:{func.__name__}:{args}:{kwargs}"
            
            # Try to get cached result
            cached_result = await cache.get(key)
            if cached_result is not None:
                return cached_result
                
            # Call function if not in cache
            result = await func(*args, **kwargs)
            
            # Store result in cache
            await cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator