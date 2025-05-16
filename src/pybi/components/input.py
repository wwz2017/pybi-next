import typing
from typing_extensions import Unpack
from instaui import arco, ui
from instaui.arco import component_types

from pybi.link_sql.protocols import (
    DataColumnProtocol,
    is_data_column,
)

_DEFAULT_PROPS = {
    "allow-clear": True,
}


def input(
    data_column: DataColumnProtocol,
    *,
    value: typing.Optional[ui.TMaybeRef[str]] = None,
    **kwargs: Unpack[component_types.TInput],
):
    info = data_column.get_infos()

    props = {**_DEFAULT_PROPS, **kwargs}

    on_change = ui.js_event(
        inputs=[ui.event_context.e(), info.field, info.query_id],
        outputs=[info.element_ref],
        code=r"""(value,field,query_id) => {
if (value) {
value = `%${value.trim()}%`
return {method: 'addFilter', args:[{field, expr: `${field} like ?`,value,replace:true,query_id}]};
}

return {method:'removeFilter', args:[{field,query_id}]};
        }""",
    )

    return arco.input(value=value, **props).on_input(on_change)  # type: ignore
