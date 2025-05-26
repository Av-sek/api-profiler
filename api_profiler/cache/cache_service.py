import os
import tempfile
from typing import Any, Optional
import diskcache as dc 
class CacheService:

    def __init__(self):
        cache_dir = os.path.join(tempfile.gettempdir(), "api_profiler_cache")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        self.cache = dc.Cache(cache_dir)
    
    def set(self, key:str, value: str, expires: Optional[int]) -> None: 
        """
        Set a value in cache with optional expiration time.
        :param key: The key to set in the cache
        :param valu: the value to set in the cache
        :param expires: the expiration time in seconds (optional)
        """
        if expires:
            self.cache.set(key, value, expire=expires)
        else:
            self.cache.set(key, value)
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        :param key: The key to get from the cache
        :return: The value from the cache or None if not found
        """
        return self.cache.get(key)
    
    def get_boolean(self, key:str)->bool:
        """
        Get a boolean value from the cache.
        :param key: The key to get from the cache
        :return: The boolean value from the cache or False if not found
        """
        value =self.get(key)
        return value.lower() == "true" if value else False

    def get_int(self, key:str, default=0)->int:
        """
        Get an integer value from the cache.
        :param key: The key to get from the cache
        :return: The integer value from the cache or 0 if not found
        """
        value = self.get(key)
        return int(value) if value else default

cache = CacheService()