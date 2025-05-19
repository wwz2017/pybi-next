from __future__ import annotations
from typing import TYPE_CHECKING


from ._mixin import DataColumnMixin

if TYPE_CHECKING:
    from .data_view import DataView


class DataColumn(DataColumnMixin):
    def __init__(self, data_view: DataView, field: str) -> None:
        self._data_view = data_view
        self.__field = field

    @property
    def field(self) -> str:
        return self.__field

    def get_element_ref(self):
        return self._data_view._data_source_element._ele_ref

    def get_data_view(self) -> DataView:
        return self._data_view
