import typing
from typing_extensions import Unpack
from instaui import arco
from instaui.arco import component_types

from pybi.link_sql._mixin import DataTableMixin


def table(
    data_table: DataTableMixin,
    **kwargs: Unpack[component_types.TTable],
):
    info = data_table.query_table()

    args = {**kwargs, "columns": info["columns"], "data": info["data"]}

    return arco.table(**args)
