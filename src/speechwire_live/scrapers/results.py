from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup

from ..client.base import SpeechwireClient

PAGE = "tab-grouping-print.php"
PARAMS = {
    "groupingid": "0",
    "sortby": "prelimresults",
    "divisionrestrict": "0",
    "compsperpage": "200",
    "Submit": "Print tab sheet",
}
COLUMNS = ["Event", "Headers", "Rows"]


def _text(element) -> str:
    return " ".join(element.get_text(" ", strip=True).split())


def _header_value(value):
    if isinstance(value, tuple):
        return tuple(str(part) for part in value)
    return str(value)


def _header_text(value) -> str:
    parts = value if isinstance(value, tuple) else (value,)
    parts = tuple(str(part).strip() for part in parts)
    parts = tuple(part for part in parts if part and not part.startswith("Unnamed:"))
    if not parts:
        return ""
    if len(set(parts)) == 1:
        return parts[0]
    return " ".join(parts)


def _is_duplicate_header_row(frame, headers) -> bool:
    if frame.empty:
        return False
    row = tuple(" ".join(str(value).split()).casefold() for value in frame.iloc[0])
    header_row = tuple(
        " ".join(_header_text(header).split()).casefold() for header in headers
    )
    leaf_row = tuple(
        " ".join((header[-1] if isinstance(header, tuple) else header).split()).casefold()
        for header in headers
    )
    parent_row = tuple(
        " ".join((header[0] if isinstance(header, tuple) else header).split()).casefold()
        for header in headers
    )
    return row in {header_row, leaf_row, parent_row}


def parse_page(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    tables = []
    for table in soup.find_all("table", class_="ddprint"):
        heading = table.find_previous("p")
        spans = heading.find_all("span") if heading else []
        if len(spans) < 2:
            raise ValueError("Results table is missing its event heading")

        frame = pd.read_html(StringIO(str(table)))[0]
        if table.find("th") is None:
            headers = tuple(str(value) for value in frame.iloc[0])
            frame = frame.iloc[1:]
        else:
            headers = tuple(_header_value(header) for header in frame.columns)
            if _is_duplicate_header_row(frame, headers):
                frame = frame.iloc[1:]
        frame = frame.fillna("")
        tables.append(
            {
                "Event": _text(spans[1]),
                "Headers": headers,
                "Rows": tuple(tuple(row) for row in frame.itertuples(index=False, name=None)),
            }
        )
    return pd.DataFrame(tables, columns=COLUMNS)


class ResultsScraper:
    def fetch(self, client: SpeechwireClient) -> pd.DataFrame:
        return parse_page(client.get_html(PAGE, PARAMS))
