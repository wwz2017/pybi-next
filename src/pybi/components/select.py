import typing
from typing_extensions import Unpack
from instaui import arco, ui
from instaui.arco import component_types

# from pybi.link_sql.protocols import (
#     DataColumnProtocol,
#     is_data_column,
# )

from pybi.link_sql.data_column import DataColumn
from pybi.link_sql.data_view_store import DataViewStore

_DEFAULT_PROPS = {
    "allow-clear": True,
}


def select(
    options: DataColumn,
    value: typing.Optional[ui.TMaybeRef[typing.Union[str, int]]] = None,
    **kwargs: Unpack[component_types.TSelect],
):
    field = options.field
    query_id = DataViewStore.get().gen_field_query_id(field)
    source = options.query_distinct(exclude_query_key=f"{options.field}-{query_id}")
    element_ref = options.get_element_ref()

    props = {**_DEFAULT_PROPS, **kwargs}

    on_change = ui.js_event(
        inputs=[ui.event_context.e(), field, query_id],
        outputs=[element_ref],
        code=r"""(value,field,query_id) => {
if (value) {
return {method: 'addFilter', args:[{field, expr: `${field}= ?`,value,query_id}]};
}

return {method:'removeFilter', args:[{field,query_id}]};
        }""",
    )

    return arco.select(options=source, value=value, **props).on_change(on_change)  # type: ignore


#     real_options, info = options.query_distinct()

#     props = {**_DEFAULT_PROPS, **kwargs}

#     on_change = ui.js_event(
#         inputs=[ui.event_context.e(), info.field, info.query_id],
#         outputs=[info.element_ref],
#         code=r"""(value,field,query_id) => {
# if (value) {
# return {method: 'addFilter', args:[{field, expr: `${field}= ?`,value,query_id}]};
# }

# return {method:'removeFilter', args:[{field,query_id}]};
#         }""",
#     )

#     return arco.select(options=real_options, value=value, **props).on_change(on_change)  # type: ignore
