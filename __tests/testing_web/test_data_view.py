from __tests.testing_web.context import Context
from instaui import ui
import pandas as pd
import pybi
from .utils import Table


def test_base(context: Context):
    data = {"Name": ["foo", "foo", "bar"], "Age": [18, 19, 20]}

    dataset = pybi.duckdb.from_pandas({"df": pd.DataFrame(data)})

    @context.register_page
    def index():
        table = dataset["df"]
        dv1 = pybi.data_view(f"SELECT Name, AVG(Age) as Age FROM {table} GROUP BY Name")
        pybi.table(dv1)

    context.open()

    Table(context).one_cell().should_see("18.5")


def test_select_columns(context: Context):
    data = {"Name": ["foo"], "Age": [18], "class": [1]}

    dataset = pybi.duckdb.from_pandas({"df": pd.DataFrame(data)})

    @context.register_page
    def index():
        table = dataset["df"]
        dv1 = pybi.data_view(f"SELECT * FROM {table}")
        pybi.table(dv1[["Name", "Age"]])

    context.open()
    table = Table(context)

    table.one_cell().should_see("foo", "18")
    table.one_cell().should_not_see("1")


def test_select_column(context: Context):
    data = {"Name": ["foo"], "Age": [18], "class": [1]}

    dataset = pybi.duckdb.from_pandas({"df": pd.DataFrame(data)})

    @context.register_page
    def index():
        table = dataset["df"]
        dv1 = pybi.data_view(f"SELECT * FROM {table}")
        pybi.label(dv1["Name"])

    context.open()
    assert False
