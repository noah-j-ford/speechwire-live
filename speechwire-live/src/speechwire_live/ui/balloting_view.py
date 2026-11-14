from collections.abc import Callable

from nicegui import ui

from ..datasets import BALLOTING
from ..session import Session
from .ballot_rows import SlotTable, split_into_slot_tables


def _column_defs() -> list[dict]:
    return [
        {"field": "Section", "width": 90},
        {"field": "Rm", "width": 80},
        {"field": "Judge", "flex": 1, "minWidth": 160},
        # One-line snippet: the grid uses the colors Python computed for each row's status.
        {"field": "Status", "width": 140, ":cellStyle": "params => params.data.statusStyle"},
    ]


def build_balloting(session: Session) -> Callable[[], None]:
    poller = session.poller
    waiting = ui.label("Waiting for ballot status data...").classes("text-slate-500")
    container = ui.row().classes("w-full items-start gap-4")
    grids: dict[int, ui.aggrid] = {}
    shown = {"version": 0, "keys": None}

    def rebuild(tables: list[SlotTable]) -> None:
        container.clear()
        grids.clear()
        with container:
            for table in tables:
                with ui.card().style("width: 34rem"):
                    ui.label(f"Slot {table.slot}").classes("text-lg font-medium")
                    if table.title:
                        ui.label(table.title).classes("text-xs text-slate-500")
                    grids[table.slot] = ui.aggrid(
                        {
                            "columnDefs": _column_defs(),
                            "rowData": table.rows,
                            "defaultColDef": {"sortable": True, "resizable": True, "filter": True},
                            "domLayout": "autoHeight",
                        },
                        auto_size_columns=False,
                    ).style("height: auto; width: 100%")

    def refresh() -> None:
        snapshot = poller.snapshot(BALLOTING)
        if snapshot is None or snapshot.version == shown["version"]:
            return
        shown["version"] = snapshot.version
        waiting.visible = False
        tables = split_into_slot_tables(snapshot.df)
        keys = [(table.slot, table.title) for table in tables]
        if keys == shown["keys"]:
            for table in tables:
                grids[table.slot].run_grid_method("setGridOption", "rowData", table.rows)
        else:
            shown["keys"] = keys
            rebuild(tables)

    return refresh
