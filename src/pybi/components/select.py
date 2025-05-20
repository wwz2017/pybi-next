import typing
from typing_extensions import Unpack
from instaui import arco, ui
from instaui.arco import component_types

from pybi.link_sql import data_set_store
from pybi.link_sql.data_view_store import DataViewStore
from pybi.link_sql._mixin import DataColumnMixin
from pybi.link_sql.query import query
from pybi.link_sql.models import ExcludeFilterInfo

_DEFAULT_PROPS = {
    "allow-clear": True,
}


def select(
    options: DataColumnMixin,
    value: typing.Optional[ui.TMaybeRef[typing.Union[str, int]]] = None,
    **kwargs: Unpack[component_types.TSelect],
):
    data_view = options.get_data_view()
    field = options.field
    query_id = DataViewStore.get().gen_field_query_id(field)
    query_key = f"{field}-{query_id}"
    exclude_info = ExcludeFilterInfo(
        data_view_name=data_view.str_name, query_key=query_key
    )

    main_query_sql = f"SELECT DISTINCT {field} FROM {data_view} ORDER BY {field} ASC"
    source = query(
        main_query_sql,
        dataset=data_set_store.try_get_data_set(data_view._dataset_id),
        exclude_info=exclude_info,
    ).flat_values()

    element_ref = options.get_element_ref()

    props = {**_DEFAULT_PROPS, "placeholder": field, **kwargs}

    on_change = ui.js_event(
        inputs=[ui.event_context.e(), field, query_id],
        outputs=[element_ref],
        code=r"""(value,field,query_id) => {

if (value === null || value === undefined || value === '' || (Array.isArray(value) && value.length === 0)){
    return {method:'removeFilter', args:[{field,query_id}]};
}

const realValue = Array.isArray(value)? value : [value];
return {method: 'addFilter', args:[{field, expr: `${field} in ?`,value,query_id}]};
}""",
    )

    return arco.select(options=source, value=value, **props).on_change(on_change)  # type: ignore
