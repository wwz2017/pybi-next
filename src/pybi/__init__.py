__all__ = [
    "__version__",
    "data_view",
    "page",
    "content",
    "server",
    "duckdb",
    "column",
    "row",
    "select",
    "table",
    "input",
]

from .version import __version__
from instaui.ui import page, content, server, column, row
from .link_sql import duckdb
from instaui.arco import *
from .components.select import select
from .components.table import table
from .components.input import input
from .link_sql.facade import data_view

from . import _setup
