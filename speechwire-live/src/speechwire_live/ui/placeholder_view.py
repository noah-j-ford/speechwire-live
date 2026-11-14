from nicegui import ui

from ..session import Session
from .page_shell import PageBuilder
from .pages import PageInfo


def build_placeholder(page: PageInfo) -> PageBuilder:
    def build(session: Session) -> None:
        with ui.card().classes("w-full max-w-xl mx-auto mt-8 gap-3"):
            ui.label(page.title).classes("text-xl font-medium")
            ui.label("This view has not been built yet.").classes("text-slate-500")
            ui.button("Back to home").props("outline no-caps href=/")

    return build
