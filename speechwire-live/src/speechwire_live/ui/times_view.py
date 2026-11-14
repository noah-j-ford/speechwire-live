from collections.abc import Callable

from nicegui import ui

from ..datasets import TIMES
from ..polling.poller import MIN_INTERVAL_SECONDS
from ..session import Session
from .table_view import TableView


def build_times(session: Session) -> Callable[[], None]:
    poller = session.poller
    times = session.datasets[TIMES]

    def save_clicked():
        try:
            path = session.save_latest()
        except OSError as error:
            ui.notify(f"Could not save: {error}", type="negative")
            return
        ui.notify(f"Saved {path}" if path else "Nothing to save yet.")

    def interval_changed(event):
        if event.value:
            poller.set_interval(event.value)

    with ui.row().classes("w-full items-center gap-4"):
        ui.number(
            "Refresh every (seconds)",
            value=poller.interval_seconds,
            min=MIN_INTERVAL_SECONDS,
            step=15,
            format="%d",
            on_change=interval_changed,
        ).props("dense outlined").classes("w-48")
        ui.button("Refresh now", on_click=poller.refresh_now).props("outline no-caps")
        ui.button("Save .xlsx", on_click=save_clicked).props("outline no-caps")
        row_count = ui.label().classes("text-sm text-slate-500")

    view = TableView(times)

    def refresh():
        snapshot = poller.snapshot(TIMES)
        view.update(snapshot)
        row_count.text = f"{len(snapshot.df)} rows" if snapshot else ""

    return refresh
