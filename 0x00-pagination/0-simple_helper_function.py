#!/usr/bin/env python3
"""task 0
"""


def index_range(page, page_size):
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)

