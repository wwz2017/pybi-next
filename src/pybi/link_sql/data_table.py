from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Sequence

from ._mixin import DataTableMixin

if TYPE_CHECKING:
    from .data_view import DataView


class DataTable(DataTableMixin):
    def __init__(
        self, data_view: DataView, fields: Optional[Sequence[str]] = None
    ) -> None:
        self._data_view = data_view
        self.__fields = fields or []

    def get_element_ref(self):
        return self._data_view._data_source_element._ele_ref

    @property
    def fields(self) -> Sequence[str]:
        return self.__fields

    def get_data_view(self) -> DataView:
        return self._data_view
