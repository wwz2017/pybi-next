from typing import Any, Dict, List, Optional, Sequence, Tuple


from dataclasses import dataclass

from pybi.link_sql.models import ExcludeFilterInfo


@dataclass
class SqlInfo:
    sql: str
    params: List[Any]


class _ExcludeFilters:
    def __init__(self, exclude_info: Optional[ExcludeFilterInfo] = None):
        self._query_key = None
        self._view_name = None
        if exclude_info is not None:
            self._query_key = exclude_info.query_key
            self._view_name = exclude_info.data_view_name

    def is_keep_filter(self, query_key: str, view_name: str) -> bool:
        if self._query_key is None:
            return True
        return query_key != self._query_key or view_name != self._view_name


def _create_filters(
    filters: Dict[str, Sequence[Dict[str, str]]],
    view_name: str,
    exclude_filters: _ExcludeFilters,
):
    if not filters:
        return ""

    and_stem = " AND ".join(
        f["expr"]
        for query_key, item in filters.items()
        for f in item
        if exclude_filters.is_keep_filter(query_key, view_name)
    )

    if not and_stem:
        return ""

    return " WHERE " + and_stem


def create_sql(
    *,
    main_sql: str,
    data_view_store: Dict[str, str],
    exclude_info: Optional[ExcludeFilterInfo] = None,
    dep_view_names: Optional[Sequence[str]] = None,
    dep_filters: Optional[Tuple[Dict[str, Sequence[Dict[str, str]]], ...]] = None,
):
    dep_view_names = dep_view_names or []
    dep_filters = dep_filters or ()

    exclude_filters = _ExcludeFilters(exclude_info)

    cte_stems = [
        f"{name} as ({data_view_store[name]}{_create_filters(filters,name,exclude_filters)})"
        for name, filters in zip(dep_view_names, dep_filters)
    ]

    if not cte_stems:
        cte_sql = ""
    else:
        cte_sql = f'WITH {", ".join(cte_stems)} '

    sql = f"{cte_sql}{main_sql}"

    cte_params = list(
        filter["value"]
        for filters, view_name in zip(dep_filters, dep_view_names)
        for query_key, item in filters.items()
        if exclude_filters.is_keep_filter(query_key, view_name)
        for filter in item
    )

    return SqlInfo(sql=sql, params=cte_params)
