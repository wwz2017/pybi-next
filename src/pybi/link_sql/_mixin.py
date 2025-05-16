from abc import abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from instaui import ui


class QueryableMixin:
    @abstractmethod
    def _to_sql(self) -> ui.TMaybeRef[str]:
        pass


@dataclass
class DataSetQueryInfo:
    columns: List[str]
    values: List[List[Any]]


class DataSetMixin:
    @abstractmethod
    def query(self, sql: str, params: Optional[List] = None) -> DataSetQueryInfo:
        pass

    @abstractmethod
    def get_id(self) -> int:
        pass


class DataTableMixin:
    @abstractmethod
    def query_table(self, *, exclude_query_key: Optional[str] = None) -> Dict[str, Any]:
        pass
