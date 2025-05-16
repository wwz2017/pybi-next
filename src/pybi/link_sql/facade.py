from .data_view import DataView


def data_view(sql: str) -> DataView:
    return DataView(sql)
