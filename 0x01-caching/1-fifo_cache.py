#!/usr/bin/env python3
"""task 1
"""


BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """FIFO caching
    """

    def __init__(self):
        super().__init__()
        self.keys = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if len(self.keys) == self.MAX_ITEMS and key not in self.keys:
            current_top = self.keys[0]
            self.keys.remove(current_top)
            print("DISCARD: {}".format(current_top))
            del self.cache_data[current_top]
        if key not in self.keys:
            self.keys.append(key)
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return
        return self.cache_data.get(key, None)
