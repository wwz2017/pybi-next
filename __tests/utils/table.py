from playwright.sync_api import expect
import re

from __tests.screen import BaseContext


class Table:
    def __init__(self, context: BaseContext, target_selector: str = "table"):
        self.__page = context.page
        self.__target_selector = target_selector

    def should_rows_count(self, count: int):
        expect(self.__page.locator(f"{self.__target_selector} tbody tr")).to_have_count(
            count
        )
        return self

    def should_values_any_cell(self, *values: str):
        body_cells = self.__page.locator(f"{self.__target_selector} tbody td")

        for value in values:
            expect(
                body_cells.filter(has_text=re.compile(f"^{value}$", re.IGNORECASE))
            ).not_to_have_count(0)

    def should_values_not_any_cell(self, *values: str):
        body_cells = self.__page.locator(f"{self.__target_selector} tbody td")

        for value in values:
            expect(
                body_cells.filter(has_text=re.compile(f"^{value}$", re.IGNORECASE))
            ).to_have_count(0)
