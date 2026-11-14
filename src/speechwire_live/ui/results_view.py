import re
from collections.abc import Callable
from dataclasses import dataclass

from nicegui import ui

from ..datasets import RESULTS
from ..session import Session


@dataclass(frozen=True)
class ResultTable:
    event: str
    headers: tuple[object, ...]
    rows: list[dict]


def _tables_from_snapshot(df) -> list[ResultTable]:
    tables = []
    for row in df.itertuples(index=False):
        headers = tuple(row.Headers)
        rows = [
            {f"column_{index}": value for index, value in enumerate(values)}
            for values in row.Rows
        ]
        tables.append(ResultTable(str(row.Event), headers, rows))
    return tables


def print_column_def(header: str, index: int) -> dict:
    label = header.casefold()
    column = {
        "headerName": header,
        "field": f"column_{index}",
        "cellStyle": {"textAlign": "center"},
        "headerClass": "centered-header",
        "headerStyle": {
            "backgroundColor": "#000",
            "color": "#fff",
            "textAlign": "center",
            "whiteSpace": "pre-line",
        },
    }

    if "prelim" in label and re.search(r"\b[1-9]\d*\b", label):
        column["width"] = 38
    elif label.strip() == "code":
        column["width"] = 70
    elif label.strip() == "team":
        column.update({"flex": 2, "minWidth": 150})
    elif "competitor" in label or "speaker" in label:
        column.update({"flex": 2, "minWidth": 180})
    elif "division" in label:
        column.update({"flex": 1, "minWidth": 75})
    else:
        column.update({"flex": 1, "minWidth": 70})
    return column


def _header_parts(header) -> tuple[str, ...]:
    return tuple(str(part).strip() for part in header) if isinstance(header, tuple) else (str(header).strip(),)


def _header_label(header) -> str:
    parts = _header_parts(header)
    parts = tuple(part for part in parts if part and not part.startswith("Unnamed:"))
    if not parts:
        return ""
    if len(set(parts)) == 1:
        return parts[0]
    return " ".join(parts)


def _results_column_defs(headers: tuple[object, ...]) -> list[dict]:
    labels = [_header_label(header) for header in headers]
    prelim_indices = [
        index
        for index, header in enumerate(headers)
        if any(part.casefold() == "prelims" for part in _header_parts(header))
        or labels[index].casefold() == "prelims"
    ]
    line_breaks = {
        "opp. avg. rank": "Opp. Avg.\nRank",
        "head to head": "Head to\nhead",
        "prelim result": "Prelim\nresult",
        "rank total": "Rank\ntotal",
        "final result": "Final\nresult",
        "finals ranks": "Finals\nranks",
        "judges pref.": "Judges\npref.",
    }
    columns = []
    for index, label in enumerate(labels):
        column = print_column_def(label, index)
        normalized = " ".join(label.casefold().split())
        if index in prelim_indices:
            prelim_number = prelim_indices.index(index) + 1
            column.update({"headerName": f"P{prelim_number}", "width": 32})
        else:
            column["headerName"] = line_breaks.get(normalized, label)
            if normalized in {"prelim result", "final result"}:
                column["cellStyle"] = {
                    "textAlign": "center",
                    "fontWeight": "bold",
                }
        column["wrapHeaderText"] = True
        column["autoHeaderHeight"] = True
        columns.append(column)
    return columns


def build_results(session: Session) -> Callable[[], None]:
    poller = session.poller
    waiting = ui.label("Waiting for results data...").classes("text-slate-500")
    container = ui.column().classes("w-full gap-2")
    grids: dict[int, ui.aggrid] = {}
    shown = {"version": 0, "keys": None}

    def rebuild(tables: list[ResultTable]) -> None:
        container.clear()
        grids.clear()
        with container:
            for index, table in enumerate(tables):
                with ui.column().classes("w-full gap-1 border-b pb-2"):
                    ui.label(table.event).classes(
                        "w-full text-center text-xl font-bold"
                    )
                    column_defs = _results_column_defs(table.headers)
                    grids[index] = ui.aggrid(
                        {
                            "columnDefs": column_defs,
                            "rowData": table.rows,
                            "rowHeight": 18,
                            "headerHeight": 30,
                            "floatingFiltersHeight": 18,
                            "defaultColDef": {
                                "sortable": True,
                                "resizable": True,
                                "filter": True,
                                "floatingFilter": True,
                                "cellStyle": {"fontSize": "11px", "padding": "0 2px"},
                                "headerStyle": {"fontSize": "11px", "padding": "0 2px"},
                            },
                            "domLayout": "autoHeight",
                        },
                        auto_size_columns=False,
                    ).style("height: auto; width: 100%")

    def refresh() -> None:
        snapshot = poller.snapshot(RESULTS)
        if snapshot is None or snapshot.version == shown["version"]:
            return
        shown["version"] = snapshot.version
        waiting.visible = False
        tables = _tables_from_snapshot(snapshot.df)
        keys = [(table.event, table.headers) for table in tables]
        if keys == shown["keys"]:
            for index, table in enumerate(tables):
                grids[index].run_grid_method("setGridOption", "rowData", table.rows)
        else:
            shown["keys"] = keys
            rebuild(tables)

    return refresh
