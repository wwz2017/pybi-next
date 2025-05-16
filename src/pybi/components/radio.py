import typing
from typing_extensions import Unpack
from instaui import arco
from instaui.arco import component_types


def radio(
    dataset: typing.Any,
    **kwargs: Unpack[component_types.TRadio],
):
    return arco.radio.use_init(dataset)
