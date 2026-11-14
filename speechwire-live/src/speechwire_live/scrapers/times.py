from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup

from ..client.base import SpeechwireClient

PAGE = "comps-perftimes.php"
ROUNDS = ("1", "2", "3", "F")
# Grouping (event) IDs change from tournament to tournament, so a fixed range is probed.
EVENT_IDS = range(1, 30)
# Every Nth successful scrape re-probes all IDs, so events that start late are still found.
FULL_RESCAN_EVERY = 10

_END_OF_HEADER = "Please select a round to view performance times for:"


def reset_header(df: pd.DataFrame) -> pd.DataFrame:
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    return df


def parse_page(html: str, rd: str, team_filter: str = ""):
    """Return (event, table). event is None when the page is not a real grouping;
    table is None when the page has no usable performance-times table."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text().split(_END_OF_HEADER)[0]
    try:
        event = text.split("Selected grouping: ")[1]
    except IndexError:
        return None, None
    table_tag = soup.find("table", {"class": "dd"})
    if table_tag is None:
        return event, None
    try:
        table = pd.read_html(StringIO(str(table_tag)))[0]
        table = reset_header(table)
        if team_filter:
            table = table[table["Team"] == team_filter]
        table = table.reset_index(drop=True)
    except ValueError:
        return event, None
    table["Event"] = event
    table["Rd"] = rd
    return event, table


class TimesScraper:
    def __init__(self, team_filter: str = ""):
        self._team_filter = team_filter
        self._empty_ids: set[int] = set()
        self._successful_scrapes = 0

    def fetch(self, client: SpeechwireClient) -> pd.DataFrame:
        full_scan = self._successful_scrapes % FULL_RESCAN_EVERY == 0
        skip_ids = set() if full_scan else self._empty_ids
        newly_empty: set[int] = set()
        tables = []

        for event_id in EVENT_IDS:
            if event_id in skip_ids:
                continue
            found_any = False
            for rd in ROUNDS:
                html = client.get_html(
                    PAGE,
                    {"selround": rd, "Submit": "Select round", "groupingid": str(event_id)},
                )
                event, table = parse_page(html, rd, self._team_filter)
                if event is None:
                    break
                if table is not None:
                    tables.append(table)
                    found_any = True
            if not found_any:
                newly_empty.add(event_id)

        if not tables:
            return pd.DataFrame()
        df = pd.concat(tables, axis=0)

        # An empty result usually means a failed login or a site hiccup, not that every
        # event is empty, so the skip list is only updated after a scrape that found data.
        if not df.empty:
            self._empty_ids = newly_empty if full_scan else self._empty_ids | newly_empty
            self._successful_scrapes += 1

        df = df.sort_values(["Event", "Team", "Entry", "Rd"])
        return df[["Event", "Section", "Spkr Pos.", "Rd", "Entry", "Team", "Time", "Rank", "Judge"]]
