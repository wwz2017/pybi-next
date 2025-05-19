from typing import Any, List, Optional, Union
from typing_extensions import overload
from instaui import ui
from pybi.link_sql._base import DataSourceElement
from pybi.link_sql._mixin import CanGetitem
from ._mixin import QueryableMixin, DataSetMixin
from .data_view_store import DataViewStore
from . import _utils
from .data_column import DataColumn
from .query import QueryInfo


class DataView(QueryableMixin):
    def __init__(self, sql: str, *, dataset: Optional[DataSetMixin] = None) -> None:
        self._data_source_element = DataSourceElement()
        self.__sql = sql
        self.str_name = DataViewStore.get().store_view(sql, self)
        self.name = ui.data(self.str_name)

        self._dataset_id = self.__get_dataset_id(dataset, sql)

    def __get_dataset_id(self, dataset: Optional[DataSetMixin], sql: str):
        if dataset is not None:
            return dataset.get_id()

        upstream_views = [
            DataViewStore.get().get_data_view(name)
            for name in _utils.extract_special_tags(sql)
        ]

        for view in upstream_views:
            if view._dataset_id is not None:
                return view._dataset_id

        return None

    def _get_filters(self, *, exclude_query_key: Optional[str] = None):
        if exclude_query_key is None:
            return self._data_source_element.filters

        filters_without_key = ui.js_computed(
            inputs=[self._data_source_element.filters, exclude_query_key],
            deep_compare_on_input=True,
            code=r"""(filters, exclude_query_key) =>{
 const new_filters = {...filters};
 delete new_filters[exclude_query_key];
 return   new_filters         
}""",
        )
        return filters_without_key

    @property
    def sql_str(self):
        return self.__sql

    def _to_sql(self) -> ui.TMaybeRef[str]:
        return ui.js_computed(inputs=[self.__sql], code="sql => sql")

    def __str__(self) -> str:
        return self.str_name

    def to_sql(self):
        return self._to_sql()

    @overload
    def __getitem__(self, field: List[str]) -> QueryInfo: ...

    @overload
    def __getitem__(self, field: str) -> DataColumn: ...

    def __getitem__(self, field: Union[str, List[str]]) -> Union[DataColumn, QueryInfo]:
        if isinstance(field, str):
            return DataColumn(self, field)

        select_stem = ", ".join(field) if field else "*"
        return QueryInfo(f"SELECT {select_stem} FROM {self}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataView):
            return False

        return self.str_name == other.str_name

    def __hash__(self) -> int:
        return hash(self.str_name)

    @property
    def result(self) -> CanGetitem:
        return self[[]].result

    def flat_values(self) -> ui.TMaybeRef[List[Any]]:
        return self[[]].flat_values()


def data_view(sql: str) -> DataView:
    return DataView(sql)
