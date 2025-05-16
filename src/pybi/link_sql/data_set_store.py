from typing import Dict
from ._mixin import DataSetMixin


_DATA_SET_ID_COUNT = 0
_DATA_SET_MAP: Dict[int, DataSetMixin] = {}


def store_data_set(data_set: DataSetMixin) -> int:
    global _DATA_SET_ID_COUNT
    _DATA_SET_ID_COUNT += 1
    _DATA_SET_MAP[_DATA_SET_ID_COUNT] = data_set
    return _DATA_SET_ID_COUNT


def get_data_set(id: int):
    return _DATA_SET_MAP[id]
