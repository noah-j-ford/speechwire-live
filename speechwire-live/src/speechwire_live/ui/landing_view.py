from nicegui import ui

from ..session import Session
from .pages import FEATURES


def build_landing(session: Session) -> None:
    ui.label(session.tournament.name).classes("text-2xl font-medium")
    ui.label("Choose a view").classes("text-slate-500")
    with ui.row().classes("gap-4"):
        for page in FEATURES:
            button = ui.button().props(f"outline no-caps href={page.path}").classes("w-64 h-28")
            with button:
                with ui.column().classes("items-start gap-0"):
                    ui.label(page.title).classes("text-lg font-medium")
                    ui.label(page.description if page.built else "Coming soon").classes(
                        "text-xs text-slate-500"
                    )
