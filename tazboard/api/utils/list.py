from typing import Optional


def get_index_or_none(search_list: list, value) -> Optional[int]:
    try:
        return search_list.index(value)
    except ValueError:
        return None
