from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Optional, Sequence
from instaui import ui
from .data_view_store import DataViewStore
from .sql import create_sql
from . import data_set_store
from ._mixin import DataTableMixin

if TYPE_CHECKING:
    from .data_view import DataView


class DataTable(DataTableMixin):
    def __init__(
        self, data_view: DataView, fields: Optional[Sequence[str]] = None
    ) -> None:
        self._data_view = data_view
        self.fields = fields

    def get_element_ref(self):
        return self._data_view._data_source_element._ele_ref

    def query_table(self, *, exclude_query_key: Optional[str] = None) -> Dict:
        data_view = self._data_view
        dep_info = data_view.get_dependency_info()

        dataset_id = data_view._dataset_id
        select_stem = ", ".join(self.fields) if self.fields else "*"

        @ui.computed(
            inputs=[
                data_view.name,
                dataset_id,
                select_stem,
                exclude_query_key,
                DataViewStore.get().data,
                data_view._get_filters(),
                dep_info.view_names,
                *dep_info.filters,
            ],
            deep_compare_on_input=True,
        )
        def result(
            current_view_name,
            dataset_id,
            select_stem,
            exclude_query_key,
            data_view_store,
            filters,
            dep_view_names,
            *dep_filters,
        ):
            sql_info = create_sql(
                current_view_name,
                exclude_query_key,
                select_stem,
                "",
                data_view_store,
                filters,
                dep_view_names,
                dep_filters,
            )

            ds = data_set_store.get_data_set(dataset_id)
            result = ds.query(sql_info.sql, sql_info.params)

            real_cols = [{"title": col, "dataIndex": col} for col in result.columns]

            real_values = [
                {col: val for col, val in zip(result.columns, row)}
                for row in result.values
            ]

            return {
                "columns": real_cols,
                "data": real_values,
            }

        return result  # type: ignore
