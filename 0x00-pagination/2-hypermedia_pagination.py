#!/usr/bin/env python3
"""task 2
"""

import csv
import math
from typing import List, Dict


def index_range(page, page_size):
    start = 0
    for _ in range(page - 1):
        start += page_size
    return (start, start + page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.dataset()

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Gets the page requested

        Args:
            page (int, optional): page number. Defaults to 1.
            page_size (int, optional): page size. Defaults to 10.

        Returns:
            List[List]: The page list
        """
        assert isinstance(page, int)
        assert isinstance(page_size, int)
        assert page > 0
        assert page_size > 0
        start, end = index_range(page, page_size)
        try:
            result = self.__dataset[start:end]
            return result
        except Exception:
            return []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        no_of_pages = math.ceil(len(self.__dataset) / page_size)
        data = self.get_page(page, page_size)
        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": page + 1 if page + 1 < no_of_pages else None,
            "prev_page": page - 1 if page - 1 > 0 else None,
            "total_pages": no_of_pages
        }
