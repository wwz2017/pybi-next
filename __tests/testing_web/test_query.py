from __tests.testing_web.context import Context
from __tests.testing_web.memory_db import MemoryDb
import pandas as pd
import pybi
from __tests.utils import Table


def test_base(context: Context, memory_db: MemoryDb):
    data = {"Name": ["foo", "foo", "bar"], "Age": [18, 19, 20]}
    dataset = memory_db.from_dataframe({"df": pd.DataFrame(data)})

    @context.register_page
    def index():
        table = dataset["df"]
        gp = pybi.query(f"SELECT Name, AVG(Age) as Age FROM {table} GROUP BY Name")
        pybi.table(gp)

    context.open()

    Table(context).should_values_any_cell("18.5")


def test_select_columns(context: Context, memory_db: MemoryDb):
    data = {"Name": ["foo"], "Age": [18], "class": [1]}
    dataset = memory_db.from_dataframe({"df": pd.DataFrame(data)})

    @context.register_page
    def index():
        table = dataset["df"]
        dv1 = pybi.query(f"SELECT * FROM {table}")
        pybi.table(dv1[["Name", "Age"]])

    context.open()
    table = Table(context)

    table.should_values_any_cell("foo", "18")
    table.should_values_not_any_cell("1")
