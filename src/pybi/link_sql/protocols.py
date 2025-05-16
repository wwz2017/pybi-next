from __future__ import annotations
from typing import Protocol as _Protocol, Tuple, Union, runtime_checkable, Sequence
from typing_extensions import overload, TypeIs
from dataclasses import dataclass
from instaui.ui import TMaybeRef, element_ref as TElementRef


@runtime_checkable
class DatasetProtocol(_Protocol):
    @overload
    def __getitem__(self, field_or_fields: str) -> DataColumnProtocol: ...

    @overload
    def __getitem__(self, field_or_fields: Sequence) -> DataTableProtocol: ...

    def __getitem__(
        self, field_or_fields: Union[str, Sequence]
    ) -> Union[DataColumnProtocol, DataTableProtocol]: ...


@runtime_checkable
class DataColumnProtocol(_Protocol):
    def query_distinct(self) -> Tuple[TMaybeRef[Sequence], DataColumnInfo]: ...

    def get_infos(self) -> DataColumnInfo: ...


@runtime_checkable
class DataTableProtocol(_Protocol):
    def get_data(self) -> DataTableQueryInfo: ...


def is_dataset(obj: object) -> TypeIs[DatasetProtocol]:
    return isinstance(obj, DatasetProtocol)


def is_data_table(obj: object) -> TypeIs[DataTableProtocol]:
    return isinstance(obj, DataTableProtocol)


def is_data_column(obj: object) -> TypeIs[DataColumnProtocol]:
    return isinstance(obj, DataColumnProtocol)


#
@dataclass
class DataTableQueryInfo:
    sql: str
    query_id: int
    element_ref: TElementRef
    rows: TMaybeRef[Sequence]
    columns: TMaybeRef[Sequence]


@dataclass
class DataColumnInfo:
    field: str
    query_id: int
    element_ref: TElementRef
