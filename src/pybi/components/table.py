from typing_extensions import Unpack
from instaui import arco, ui
from instaui.arco import component_types

from pybi.link_sql._mixin import QueryableMixin


def table(
    query: QueryableMixin,
    **kwargs: Unpack[component_types.TTable],
):
    info = ui.js_computed(
        inputs=[query.result],
        code=r"""result=>{
        const columns = result.columns;
        const values = result.values;
        const real_cols = columns.map(col => ({title: col, dataIndex: col, ellipsis: true, tooltip: true}));
        const real_values = values.map(row => Object.fromEntries(row.map((value,index) => [columns[index], value])));
        return {columns: real_cols, data: real_values};                     
}""",
    )

    args = {**kwargs, "columns": info["columns"], "data": info["data"]}

    return arco.table(**args)
