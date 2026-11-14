from collections.abc import Callable

from nicegui import ui

from ..session import Session
from .pages import FEATURES, HOME, PageInfo
from .setup_views import build_login_form, build_tournament_picker

PageBuilder = Callable[[Session], Callable[[], None] | None]


def _build_nav_header(session: Session, header, active: PageInfo):
    def switch_tournament():
        try:
            path = session.save_latest()
        except OSError as error:
            ui.notify(f"Could not save before switching: {error}", type="negative")
            return
        if path:
            ui.notify(f"Saved {path}")
        session.end()

    with header:
        ui.label(session.tournament.name).classes("text-lg font-medium")
        for page in (HOME, *FEATURES):
            button = ui.button(page.title).props(f"flat no-caps href={page.path}")
            if page == active:
                button.classes("bg-slate-600")
        ui.space()
        status = ui.label().classes("text-sm text-slate-300")
        ui.button("Switch tournament", on_click=switch_tournament).props("flat")
    return status


async def run_page(session: Session, active: PageInfo, build_content: PageBuilder) -> None:
    header = ui.header().classes("items-center gap-4 bg-slate-800 text-white")
    body = ui.column().classes("w-full")
    shown = {"stage": None, "status": None, "refresh": None}

    async def render_stage():
        stage = session.stage
        if stage == shown["stage"]:
            return
        shown.update(stage=stage, status=None, refresh=None)
        header.clear()
        body.clear()
        if stage == "dashboard":
            shown["status"] = _build_nav_header(session, header, active)
            with body:
                shown["refresh"] = build_content(session)
            return
        with header:
            ui.label("Speechwire Live").classes("text-lg font-medium")
        with body:
            if stage == "tournament":
                await build_tournament_picker(session)
            else:
                build_login_form(session)

    def refresh():
        poller = session.poller
        if shown["status"] is not None and poller is not None:
            shown["status"].text = poller.status
        if shown["refresh"]:
            shown["refresh"]()

    await render_stage()
    ui.timer(0.3, render_stage)
    ui.timer(1.0, refresh)
