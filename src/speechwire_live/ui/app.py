from nicegui import app, ui

from ..client.live import LiveClient
from ..config import Config
from ..datasets import TIMES, build_datasets
from ..export.xlsx import save_times
from ..polling.poller import MIN_INTERVAL_SECONDS, Poller
from .table_view import TableView


def run_app(config: Config) -> None:
    datasets = {dataset.name: dataset for dataset in build_datasets(config)}
    times = datasets[TIMES]
    poller = Poller(
        lambda: LiveClient(config.username, config.password, config.tournament_id),
        list(datasets.values()),
        config.poll_seconds,
    )

    def save_latest():
        snapshot = poller.snapshot(TIMES)
        return save_times(snapshot.df, config.tournament_name) if snapshot else None

    def shutdown():
        poller.stop()
        save_latest()

    app.on_startup(poller.start)
    app.on_shutdown(shutdown)

    @ui.page("/")
    def index():
        def save_clicked():
            try:
                path = save_latest()
            except OSError as error:
                ui.notify(f"Could not save: {error}", type="negative")
                return
            ui.notify(f"Saved {path}" if path else "Nothing to save yet.")

        def interval_changed(event):
            if event.value:
                poller.set_interval(event.value)

        with ui.header().classes("items-center gap-4 bg-slate-800 text-white"):
            ui.label(f"{config.tournament_name}: {times.title.lower()}").classes("text-lg font-medium")
            status = ui.label().classes("text-sm text-slate-300")
            ui.space()
            ui.number(
                "Refresh every (seconds)",
                value=poller.interval_seconds,
                min=MIN_INTERVAL_SECONDS,
                step=15,
                format="%d",
                on_change=interval_changed,
            ).props("dense outlined dark").classes("w-48")
            ui.button("Refresh now", on_click=poller.refresh_now).props("flat")
            ui.button("Save .xlsx", on_click=save_clicked).props("flat")

        view = TableView(times)

        def refresh():
            snapshot = poller.snapshot(TIMES)
            view.update(snapshot)
            row_count = f" - {len(snapshot.df)} rows" if snapshot else ""
            status.text = poller.status + row_count

        ui.timer(1.0, refresh)

    ui.run(host=config.host, port=config.port, title="Speechwire Live", reload=False)
