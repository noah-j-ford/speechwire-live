from dataclasses import dataclass
from datetime import date
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

REQUEST_TIMEOUT_SECONDS = 30


@dataclass(frozen=True)
class Tournament:
    name: str
    id: str
    location: str = ""


def _get_today() -> str:
    today = date.today()
    return str(today.strftime(f"{today:%b}. {today.day}, {today:%Y}"))


def _reset_header(df: pd.DataFrame) -> pd.DataFrame:
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    return df


def _get_bluetable(soup: BeautifulSoup) -> pd.DataFrame:
    table = soup.find("table", {"class": "bluetable"})
    table = pd.read_html(StringIO(str(table)))[0]
    table = _reset_header(table)  # moves "TOURNAMENT NAME" to header
    table = _reset_header(table)  # moves the actual header into place
    table.columns = ["Date", "Tournament Name", "More info", "Level", "Platform", "Location"]
    # Tournaments without a hyperlinked Speechwire page have no "More info" value.
    table = table[table["More info"] == table["More info"]]
    return table.reset_index(drop=True)


def parse_todays_tournaments(html: str, today: str) -> list[Tournament]:
    soup = BeautifulSoup(html, "html.parser")
    table = _get_bluetable(soup)
    table = table[table["Date"] == today]

    ids: dict[str, str] = {}
    for cell in soup.find("table", {"class": "bluetable"}).find_all("td", {"class": "bluetablesmall"}):
        if cell.a is not None and cell.text not in ids:
            ids[cell.text] = cell.a["href"].split("tournid=")[-1]

    return [
        Tournament(name=name, id=ids[name], location=str(location))
        for name, location in zip(table["Tournament Name"], table["Location"])
        if name in ids
    ]


def list_todays_tournaments(season_id: int) -> list[Tournament]:
    url = (
        "https://postings.speechwire.com/p-calendar.php?stateid=27&tournlevelid=1"
        f"&seasonid={season_id}&viewmode=all&Submit=View+tournaments&upcomingonly=1"
    )
    response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
    return parse_todays_tournaments(response.text, _get_today())
