#!/usr/bin/python3
"""task 0
"""


BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """basic caching
    """

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return
        return self.cache_data.get(key, None)
