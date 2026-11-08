from nicegui import ui

from ..polling.snapshot import Dataset, Snapshot
from .grid_rows import to_grid_rows


class TableView:
    def __init__(self, dataset: Dataset):
        self._dataset = dataset
        self._shown_version = 0
        self._grid = ui.aggrid(
            {
                "columnDefs": [self._column_def(name) for name in dataset.columns],
                "rowData": [],
                "defaultColDef": {"sortable": True, "resizable": True, "floatingFilter": True},
                # Column names such as "Spkr Pos." contain dots, which AG Grid would read as paths.
                "suppressFieldDotNotation": True,
                "enableCellTextSelection": True,
                "ensureDomOrder": True,
            },
            auto_size_columns=False,
        ).style("height: calc(100vh - 110px)")

    def _column_def(self, name: str) -> dict:
        numeric = name in self._dataset.numeric_columns
        return {
            "headerName": name,
            "field": name,
            "filter": "agNumberColumnFilter" if numeric else "agTextColumnFilter",
        }

    def update(self, snapshot: Snapshot | None) -> None:
        if snapshot is None or snapshot.version == self._shown_version:
            return
        first_load = self._shown_version == 0
        self._shown_version = snapshot.version
        rows = to_grid_rows(snapshot.df, self._dataset.numeric_columns)
        # Replacing only the row data keeps the user's sort, filters, and column widths.
        self._grid.run_grid_method("setGridOption", "rowData", rows)
        if first_load:
            ui.timer(0.5, lambda: self._grid.run_grid_method("autoSizeAllColumns"), once=True)
