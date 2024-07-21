#!/usr/bin/python3
"""task 2
"""


BaseCaching = __import__('base_caching').BaseCaching


class Node:
    """Node for linked list
    """

    def __init__(self, value) -> None:
        self.value = value
        self.next = None
        self.prev = None


class LinkedList:
    """Linked lsit Data structure
    """

    def __init__(self) -> None:
        self.items = 0
        self.head: Node = None

    def addFirst(self, key: Node):
        if self.head is not None:
            key.next = self.head
            self.head.prev = key
        self.head = key
        self.items += 1

    def remove(self, key):
        item = self.getNode(key)
        if self.head != item:
            item.prev.next = item.next
        if item.next is not None:
            item.next.prev = item.prev
        if self.head == item:
            self.head = item.next
        self.items -= 1
        return item

    def getNode(self, key):
        temp = self.head
        while temp is not None:
            if temp.value == key:
                return temp
            temp = temp.next
        return None

    def removeLast(self):
        return self.remove(self.head.value)


class LIFOCache(BaseCaching):
    """FIFO caching
    """

    def __init__(self):
        super().__init__()
        self.ll = LinkedList()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.ll.remove(key)
        if key not in self.cache_data and self.ll.items == self.MAX_ITEMS:
            item_ = self.ll.removeLast()
            print("DISCARD: {}".format(item_.value))
            del self.cache_data[item_.value]
        self.ll.addFirst(Node(key))
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return
        return self.cache_data.get(key, None)
