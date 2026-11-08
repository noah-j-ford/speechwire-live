from .cleaning.times import COLUMNS, clean_up_formatting
from .config import Config
from .polling.snapshot import Dataset
from .scrapers.times import TimesScraper

TIMES = "times"


def build_datasets(config: Config) -> list[Dataset]:
    scraper = TimesScraper(config.team_filter)

    def fetch_times(client):
        raw = scraper.fetch(client)
        return raw if raw.empty else clean_up_formatting(raw)

    return [
        Dataset(
            name=TIMES,
            title="Performance times",
            columns=tuple(COLUMNS),
            numeric_columns=frozenset({"Spkr Pos.", "Seconds", "Rank"}),
            fetch=fetch_times,
        )
    ]
