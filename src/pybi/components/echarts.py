from __future__ import annotations
from typing import Dict
from instaui import ui
from instaui.vars.mixin_types.element_binding import ElementBindingMixin


def echarts(option: EChartsOption):
    return ui.echarts(option)


class EChartsOption(ElementBindingMixin):
    def __init__(self, computed_option: ui.TMaybeRef) -> None:
        self.__computed_option = computed_option

    def _to_element_binding_config(self) -> Dict:
        return self.__computed_option._to_element_binding_config()
