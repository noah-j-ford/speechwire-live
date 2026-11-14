from collections.abc import Callable

from nicegui import ui

from ..datasets import SWEEPSTAKES
from ..session import Session
from .results_view import print_column_def


def build_sweepstakes(session: Session) -> Callable[[], None]:
    poller = session.poller
    waiting = ui.label("Waiting for sweepstakes data...").classes("text-slate-500")
    container = ui.column().classes("w-full gap-1")
    grid = {"value": None}
    shown = {"version": 0, "headers": None}

    def rebuild(headers: tuple[str, ...], rows: list[dict]) -> None:
        container.clear()
        with container:
            ui.label("Team Sweepstakes").classes("w-full text-center text-xl font-bold")
            column_defs = [
                print_column_def(header, index)
                for index, header in enumerate(headers)
            ]
            grid["value"] = ui.aggrid(
                {
                    "columnDefs": column_defs,
                    "rowData": rows,
                    "rowHeight": 18,
                    "headerHeight": 22,
                    "defaultColDef": {
                        "sortable": True,
                        "cellStyle": {"fontSize": "11px", "padding": "0 2px"},
                        "headerStyle": {"fontSize": "11px", "padding": "0 2px"},
                    },
                    "domLayout": "autoHeight",
                },
                auto_size_columns=False,
            ).style("height: auto; width: 100%")

    def refresh() -> None:
        snapshot = poller.snapshot(SWEEPSTAKES)
        if snapshot is None or snapshot.version == shown["version"]:
            return
        shown["version"] = snapshot.version
        waiting.visible = False
        if snapshot.df.empty:
            return
        row = next(snapshot.df.itertuples(index=False))
        headers = tuple(row.Headers)
        rows = [
            {f"column_{index}": value for index, value in enumerate(values)}
            for values in row.Rows
        ]
        if headers == shown["headers"] and grid["value"] is not None:
            grid["value"].run_grid_method("setGridOption", "rowData", rows)
        else:
            shown["headers"] = headers
            rebuild(headers, rows)

    return refresh
