import re
from datetime import datetime
from pathlib import Path

import pandas as pd

COLUMN_WIDTHS = {
    "A:A": 4, "B:B": 5, "C:C": 6, "D:D": 2, "E:E": 9, "F:F": 17, "G:G": 10,
    "H:J": 4, "K:L": 7, "M:M": 12,
}
SHEET_NAME_MAX_LENGTH = 31


def _safe_name(name: str) -> str:
    return re.sub(r"[\[\]:*?/\\]", "", name).strip() or "Tournament"


def save_times(df: pd.DataFrame, tournament_name: str, directory: Path | str = ".") -> Path:
    safe_name = _safe_name(tournament_name)
    sheet_name = safe_name[:SHEET_NAME_MAX_LENGTH]
    current_time = datetime.now().strftime("%H-%M")
    path = Path(directory) / f"{safe_name} {current_time} Times.xlsx"
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        cell_format = writer.book.add_format(
            {"font_name": "Calibri", "font_size": "8", "align": "left", "valign": "top"}
        )
        for columns, width in COLUMN_WIDTHS.items():
            writer.sheets[sheet_name].set_column(columns, width=width, cell_format=cell_format)
    return path
