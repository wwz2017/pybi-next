from pathlib import Path
import os
import re
import pandas as pd
import duckdb

from __tests.testing_web.context import Context

__DIR__ = Path(__file__).parent / ".dataset"

__DIR__.mkdir(exist_ok=True)


def create_duckdb_file(filename: str, table_name: str, df: pd.DataFrame):
    file_path = __DIR__ / filename
    if file_path.exists():
        os.remove(file_path)

    with duckdb.connect(file_path) as conn:
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")

    return file_path


class Table:
    def __init__(self, context: Context, selector: str = "table"):
        self.__context = context
        self.__selector = selector

    def one_cell(self):
        return Table(self.__context, f"{self.__selector} td")

    def should_see(self, *texts: str):
        for text in texts:
            target = self.__context.find_by_selector(self.__selector).filter(
                has_text=text
            )
            self.__context.expect(target).to_have_count(1)

    def should_not_see(self, *texts: str):
        for text in texts:
            target = self.__context.find_by_selector(self.__selector).filter(
                has_text=re.compile(f"^{text}$", re.IGNORECASE)
            )
            self.__context.expect(target).to_have_count(0)
