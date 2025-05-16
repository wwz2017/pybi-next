from typing import Any, Dict, List, Optional, Sequence, Set, Union
from typing_extensions import overload
from instaui import ui
from pybi.link_sql._base import DataSourceElement
from pybi.link_sql.data_table import DataTable
from ._mixin import QueryableMixin, DataSetMixin, DataTableMixin
from .data_view_store import DataViewStore
from ._types import DependencyInfo
from . import _utils
from .data_column import DataColumn


class DataView(QueryableMixin, DataTableMixin):
    def __init__(self, sql: str, *, dataset: Optional[DataSetMixin] = None) -> None:
        self._data_source_element = DataSourceElement()
        self.sql = sql
        self.str_name = DataViewStore.get().store_view(sql, self)
        self.name = ui.data(self.str_name)
        self._query_id = 0
        self.__dependency_info: Optional[DependencyInfo] = None
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

    def _get_dependency_views(self):
        stack = [
            DataViewStore.get().get_data_view(name)
            for name in _utils.extract_special_tags(self.sql)
        ]

        result: Set[DataView] = set(stack)

        while stack:
            view = stack.pop()
            result.add(view)

            stack.extend(view._get_dependency_views())

        return list(result)

    def get_dependency_info(self):
        if self.__dependency_info is None:
            dep_views = self._get_dependency_views()
            view_names = [view.str_name for view in dep_views]
            filters = [view._get_filters() for view in dep_views]

            self.__dependency_info = DependencyInfo(
                view_names=view_names, filters=filters
            )

        return self.__dependency_info

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

    def _to_sql(self) -> ui.TMaybeRef[str]:
        return ui.js_computed(inputs=[self.sql], code="sql => sql")

    def __str__(self) -> str:
        return self.str_name

    def to_sql(self):
        return self._to_sql()

    @overload
    def __getitem__(self, field: List[str]) -> DataTableMixin: ...

    @overload
    def __getitem__(self, field: str) -> DataColumn: ...

    def __getitem__(
        self, field: Union[str, List[str]]
    ) -> Union[DataColumn, DataTableMixin]:
        if isinstance(field, str):
            return DataColumn(self, field)

        return DataTable(self, field)

    def new_query_info(self):
        self._query_id += 1
        return self._query_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataView):
            return False

        return self.str_name == other.str_name

    def __hash__(self) -> int:
        return hash(self.str_name)

    def query_table(self, *, exclude_query_key: Optional[str] = None):
        return DataTable(self).query_table(exclude_query_key=exclude_query_key)
