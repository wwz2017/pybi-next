from __tests.testing_web.context import Context
from instaui import ui
import pandas as pd
import pybi
from . import utils
from .utils import Table


def test_data_from_pandas(context: Context):
    data = {"Name": ["foo"]}

    dataset = pybi.duckdb.from_pandas({"df": pd.DataFrame(data)})

    @context.register_page
    def index():
        table = dataset["df"]
        pybi.table(table)

    context.open()

    Table(context).one_cell().should_see("foo")


def test_data_from_db(context: Context):
    data = {"Name": ["foo"]}
    file = utils.create_duckdb_file("test.db", "df", pd.DataFrame(data))

    dataset = pybi.duckdb(file)

    @context.register_page
    def index():
        table = dataset["df"]
        pybi.table(table)

    context.open()
    Table(context).one_cell().should_see("foo")
