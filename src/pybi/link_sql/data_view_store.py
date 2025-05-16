from contextvars import ContextVar
from typing import TYPE_CHECKING, Dict, Optional
from instaui import ui
from collections import defaultdict


if TYPE_CHECKING:
    from .data_view import DataView


class DataViewStore(ui.element):
    _data_view_store_context: ContextVar[Optional["DataViewStore"]] = ContextVar(
        "data_view_store_context", default=None
    )

    def __init__(self):
        super().__init__("template")
        self._name_to_data_view_map: Dict[str, "DataView"] = {}
        self._org_data = {}
        self.data = ui.state(self._org_data)
        self._field_query_id_count: Dict[str, int] = defaultdict(lambda: 0)

    def gen_field_query_id(self, field: str):
        self._field_query_id_count[field] += 1
        return self._field_query_id_count[field]

    def store_view(self, sql: str, data_view: "DataView"):
        name = self.__gen_name()
        self._org_data[name] = sql
        self._name_to_data_view_map[name] = data_view
        return name

    def get_data_view(self, name: str):
        return self._name_to_data_view_map[name]

    def __gen_name(self):
        id = len(self._org_data)
        return f"'@_{id}_@'"

    @classmethod
    def get(cls) -> "DataViewStore":
        dv = cls._data_view_store_context.get()
        if dv is None:
            dv = cls()
            cls._data_view_store_context.set(dv)

        return cls._data_view_store_context.get()  # type: ignore

    def _to_json_dict(self):
        self.data._ref_.value = self._org_data  # type: ignore
        return super()._to_json_dict()
