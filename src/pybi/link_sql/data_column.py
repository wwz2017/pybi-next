from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from instaui import ui
from .data_view_store import DataViewStore
from .sql import create_sql
from . import data_set_store

if TYPE_CHECKING:
    from .data_view import DataView


class DataColumn:
    def __init__(self, data_view: DataView, field: str) -> None:
        self._data_view = data_view
        self.field = field

    def get_element_ref(self):
        return self._data_view._data_source_element._ele_ref

    def query_distinct(self, *, exclude_query_key: Optional[str] = None):
        data_view = self._data_view
        dep_info = data_view.get_dependency_info()

        dataset_id = data_view._dataset_id

        @ui.computed(
            inputs=[
                data_view.name,
                dataset_id,
                f"distinct {self.field}",
                f"{self.field} asc",
                exclude_query_key,
                DataViewStore.get().data,
                data_view._get_filters(exclude_query_key=exclude_query_key),
                dep_info.view_names,
                *dep_info.filters,
            ],
            deep_compare_on_input=True,
        )
        def distinct_values(
            current_view_name,
            dataset_id,
            select_stem,
            order_stem,
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
                order_stem,
                data_view_store,
                filters,
                dep_view_names,
                dep_filters,
            )

            ds = data_set_store.get_data_set(dataset_id)
            result = ds.query(sql_info.sql, sql_info.params)
            return [value[0] for value in result.values]

        return distinct_values
