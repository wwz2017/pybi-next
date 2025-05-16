from typing import Optional
from instaui import ui
from ._types import TFilters


class DataSourceElement(ui.element, esm="./data_source.js"):
    def __init__(self):
        super().__init__()

        self._ele_ref = ui.element_ref()
        self.element_ref(self._ele_ref)

        self.filters: TFilters = ui.state({})

        self.on(
            "filter-changed",
            ui.js_event(
                inputs=[ui.event_context.e()],
                outputs=[self.filters],
                code="v=> v.filters",
            ),
        )

    def new_filters_exclude(
        self,
        exclude_field: Optional[str] = None,
        exclude_query_id: Optional[int] = None,
    ):
        if exclude_field is None:
            return self.filters

        return ui.js_computed(
            inputs=[self.filters, exclude_field, exclude_query_id],
            code=r"""(filters,exclude_field,exclude_query_id)=>{
    delete filters[`${exclude_field}-${exclude_query_id}`];
    return filters; 
    }""",
        )
