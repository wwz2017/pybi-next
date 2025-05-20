import re
import typing
from playwright.sync_api import Page, expect, Locator

_TKind = typing.Literal[
    "alert",
    "alertdialog",
    "application",
    "article",
    "banner",
    "blockquote",
    "button",
    "caption",
    "cell",
    "checkbox",
    "code",
    "columnheader",
    "combobox",
    "complementary",
    "contentinfo",
    "definition",
    "deletion",
    "dialog",
    "directory",
    "document",
    "emphasis",
    "feed",
    "figure",
    "form",
    "generic",
    "grid",
    "gridcell",
    "group",
    "heading",
    "img",
    "insertion",
    "link",
    "list",
    "listbox",
    "listitem",
    "log",
    "main",
    "marquee",
    "math",
    "menu",
    "menubar",
    "menuitem",
    "menuitemcheckbox",
    "menuitemradio",
    "meter",
    "navigation",
    "none",
    "note",
    "option",
    "paragraph",
    "presentation",
    "progressbar",
    "radio",
    "radiogroup",
    "region",
    "row",
    "rowgroup",
    "rowheader",
    "scrollbar",
    "search",
    "searchbox",
    "separator",
    "slider",
    "spinbutton",
    "status",
    "strong",
    "subscript",
    "superscript",
    "switch",
    "tab",
    "table",
    "tablist",
    "tabpanel",
    "term",
    "textbox",
    "time",
    "timer",
    "toolbar",
    "tooltip",
    "tree",
    "treegrid",
    "treeitem",
    "input",
    "input-number",
]

_kind_map = {"input": "textbox", "input-number": "spinbutton"}


class BaseContext:
    def __init__(
        self,
        page: Page,
    ) -> None:
        self.page = page

    def pause(self) -> None:
        self.page.pause()

    def find(
        self,
        kind: _TKind,
        *,
        checked: typing.Optional[bool] = None,
        disabled: typing.Optional[bool] = None,
        expanded: typing.Optional[bool] = None,
        include_hidden: typing.Optional[bool] = None,
        level: typing.Optional[int] = None,
        name: typing.Optional[typing.Union[str, typing.Pattern[str]]] = None,
        pressed: typing.Optional[bool] = None,
        selected: typing.Optional[bool] = None,
        exact: typing.Optional[bool] = None,
    ):
        return self.page.get_by_role(
            role=_kind_map.get(kind, kind),  # type: ignore
            checked=checked,
            disabled=disabled,
            expanded=expanded,
            include_hidden=include_hidden,
            level=level,
            name=name,
            pressed=pressed,
            selected=selected,
            exact=exact,
        )

    def find_input_number(self, classes: typing.Optional[str] = None):
        target = self.find("input-number")
        if classes:
            return target.filter(has=self.find_by_class(classes))

        return target

    def find_list_items(self, ul_classes: typing.Optional[str] = None):
        if ul_classes:
            ul = self.find("list").filter(has=self.find_by_class(ul_classes))
            return ul.locator("li")

        return self.find("listitem")

    def find_by_text(self, text: str, *, exact: typing.Optional[bool] = True):
        return self.page.get_by_text(text, exact=exact)

    def find_by_class(self, class_name: str):
        return self.page.locator(f".{class_name}")

    def find_by_selector(self, selector: str):
        return self.page.locator(selector)

    def expect_style_value(self, locator: Locator, property_name: str, value: str):
        expect(locator).to_have_attribute(
            "style", re.compile(f"{property_name}: {value}")
        )

    def expect_have_class(self, locator: Locator, value: str):
        expect(locator).to_have_class(re.compile(value))

    def expect_not_to_have_class(self, locator: Locator, value: str):
        expect(locator).not_to_have_class(re.compile(value))

    def should_see(
        self,
        text: str,
        equal_to=False,
        exact: typing.Optional[bool] = None,
        *,
        timeout_ms: typing.Optional[float] = None,
    ) -> None:
        if equal_to:
            text = self.exact_text(text)  # type: ignore

        expect(self.page.get_by_text(text, exact=exact)).to_be_visible(
            timeout=timeout_ms
        )

    def should_not_see(
        self,
        text: str,
        exact: typing.Optional[bool] = None,
        *,
        timeout_ms: typing.Optional[float] = None,
    ) -> None:
        expect(self.page.get_by_text(text, exact=exact)).not_to_be_visible(
            timeout=timeout_ms
        )

    def expect(self, locator: Locator):
        return expect(locator)

    def exact_text(self, text: str, *, ignore_case: bool = True):
        return re.compile(
            f"^{re.escape(text)}$", flags=re.IGNORECASE if ignore_case else 0
        )
