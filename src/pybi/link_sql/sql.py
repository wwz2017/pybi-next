from typing import Any, Dict, List, Optional, Tuple


from dataclasses import dataclass


@dataclass
class SqlInfo:
    sql: str
    params: List[Any]


def _create_filters(filters: Dict[str, List[Dict[str, str]]]):
    if not filters:
        return ""

    filter_values = filters.values()

    return " WHERE " + " AND ".join(f["expr"] for item in filter_values for f in item)


def create_sql(
    current_view_name: str,
    exclude_query_key: Optional[str],
    select_stem: str,
    order_stem: str,
    data_view_store: Dict[str, str],
    current_filters: Dict[str, List[Dict[str, str]]],
    dep_view_names: List[str],
    dep_filters: Tuple[Dict[str, List[Dict[str, str]]], ...],
):
    current_filters = {
        name: values
        for name, values in current_filters.items()
        if name != exclude_query_key
    }

    cte_stems = [
        f"{name} as ({data_view_store[name]}{_create_filters(filters)})"
        for name, filters in zip(dep_view_names, dep_filters)
    ]

    if not cte_stems:
        cte_sql = ""
    else:
        cte_sql = f'WITH {", ".join(cte_stems)} '

    main_query_sql = data_view_store[current_view_name]

    if select_stem:
        main_query_sql = main_query_sql.replace("select *", f"select {select_stem}")

    sql = f"{cte_sql}{main_query_sql}{_create_filters(current_filters)}"

    if order_stem:
        sql = f"{sql} order by {order_stem}"

    cte_params = list(
        filter["value"]
        for filters in dep_filters
        for item in filters.values()
        for filter in item
    )
    current_params = list(f["value"] for item in current_filters.values() for f in item)

    return SqlInfo(sql=sql, params=[*cte_params, *current_params])
