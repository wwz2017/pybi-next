import typing
from playwright.sync_api import Page
from instaui.launch_collector import PageInfo
from .server import TestServer
from __tests.screen import BaseContext


class Context(BaseContext):
    num = 0

    def __init__(
        self,
        test_server: TestServer,
        page: Page,
    ) -> None:
        super().__init__(page)
        self.num = Context.num
        Context.num += 1

        self._test_server = test_server
        self._root_path = test_server.url
        self._path = f"/{self.num}"

    @typing.overload
    def register_page(self, fn: typing.Callable): ...

    @typing.overload
    def register_page(
        self,
        *,
        path: typing.Optional[str] = None,
    ): ...

    def register_page(
        self,
        fn: typing.Optional[typing.Callable] = None,
        *,
        path: typing.Optional[str] = None,
    ):
        if fn is None:

            def wrapper(fn: typing.Callable):
                self.register_page(
                    fn,
                    path=path,
                )  # type: ignore

            return wrapper

        self._test_server._server.register_page(
            PageInfo(
                self._path + (path or ""),
                fn,
            )
        )

    @property
    def path(self) -> str:
        return self._path

    def open(self) -> None:
        url = self._root_path + self._path
        self.page.goto(url)

    def open_by_path(self, path: str) -> None:
        url = self._root_path + self._path + path
        self.page.goto(url)
