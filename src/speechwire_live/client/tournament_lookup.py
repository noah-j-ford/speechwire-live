from datetime import date

import pandas as pd
import requests
from bs4 import BeautifulSoup


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
    table = pd.read_html(str(table))[0]
    table = _reset_header(table)  # moves "TOURNAMENT NAME" to header
    table = _reset_header(table)  # moves the actual header into place
    table.columns = ["Date", "Tournament Name", "More info", "Level", "Platform", "Location"]
    # Tournaments without a hyperlinked Speechwire page have no "More info" value.
    table = table[table["More info"] == table["More info"]]
    return table.reset_index(drop=True)


def _select_tournament(table: pd.DataFrame) -> str:
    table = table[table["Date"] == _get_today()]
    names = table["Tournament Name"].to_list()
    dates = table["Date"].to_list()
    for i, (name, tournament_date) in enumerate(zip(names, dates), start=1):
        print(f"[{i}] {name} --- {tournament_date}")
    selection = int(input("Choose which tournament [NUMBER]"))
    return names[selection - 1]


def _get_tournament_id_value(soup: BeautifulSoup, selected_tournament: str) -> str:
    table = soup.find("table", {"class": "bluetable"})
    for cell in table.find_all("td", {"class": "bluetablesmall"}):
        if cell.text == selected_tournament:
            return cell.a["href"].split("tournid=")[-1]
    raise LookupError(f"Tournament not found on the calendar: {selected_tournament}")


def choose_tournament(season_id: int) -> str:
    url = (
        "https://postings.speechwire.com/p-calendar.php?stateid=27&tournlevelid=1"
        f"&seasonid={season_id}&viewmode=all&Submit=View+tournaments&upcomingonly=1"
    )
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    selected = _select_tournament(_get_bluetable(soup))
    return _get_tournament_id_value(soup, selected)
