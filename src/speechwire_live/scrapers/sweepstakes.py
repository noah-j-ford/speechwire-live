from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup

from ..client.base import SpeechwireClient

PAGE = "tab-team-print.php"
PARAMS = {"sstyleid": "0", "Submit": "Print sweepstakes"}
COLUMNS = ["Headers", "Rows"]


def parse_page(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table", class_="ddprint")
    if len(tables) != 1:
        raise ValueError(f"Expected one sweepstakes table, found {len(tables)}")

    table = tables[0]
    frame = pd.read_html(StringIO(str(table)))[0]
    if table.find("th") is None:
        headers = tuple(str(value) for value in frame.iloc[0])
        frame = frame.iloc[1:]
    else:
        headers = tuple(str(header) for header in frame.columns)
    return pd.DataFrame(
        [{"Headers": headers, "Rows": tuple(tuple(row) for row in frame.itertuples(index=False, name=None))}],
        columns=COLUMNS,
    )


class SweepstakesScraper:
    def fetch(self, client: SpeechwireClient) -> pd.DataFrame:
        return parse_page(client.get_html(PAGE, PARAMS))
