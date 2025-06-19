import pybi
from instaui import ui
import pandas as pd
from templates import make_bar, make_line, make_pie


data = {
    "Class": [
        "Class 1",
        "Class 1",
        "Class 1",
        "Class 1",
        "Class 1",
        "Class 2",
        "Class 2",
        "Class 2",
        "Class 2",
        "Class 2",
        "Class 3",
        "Class 3",
        "Class 3",
        "Class 3",
        "Class 3",
    ],
    "Name": [
        "name1",
        "name2",
        "name3",
        "name4",
        "name5",
        "name1",
        "name2",
        "name3",
        "name4",
        "name5",
        "name1",
        "name2",
        "name3",
        "name4",
        "name5",
    ],
    "Age": [10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 30, 31, 32, 33, 34],
}

dataset = pybi.duckdb.from_pandas({"df": pd.DataFrame(data)})


@ui.page()
def index():
    table = dataset["df"]

    with pybi.row().gap("0.25rem"):
        pybi.select(table["Class"], multiple=True, allow_clear=True)
        pybi.select(table["Name"], multiple=True, allow_clear=True)

    with pybi.grid(columns=pybi.grid.auto_columns(min_width="20vw")).classes(
        "min-h-[300px]"
    ):
        pybi.echarts(make_bar(table, x="Name", y="Age", color="Class", agg="avg"))
        pybi.echarts(make_line(table, x="Name", y="Age", agg="avg"))
        pybi.echarts(make_pie(table, name="Class", value="Age", agg="sum"))


ui.server(debug=True).run()
