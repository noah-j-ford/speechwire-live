from .cleaning.times import COLUMNS, clean_up_formatting
from .config import Config
from .polling.snapshot import Dataset
from .scrapers.balloting import COLUMNS as BALLOTING_COLUMNS
from .scrapers.balloting import BallotingScraper
from .scrapers.times import TimesScraper

TIMES = "times"
BALLOTING = "balloting"


def build_datasets(config: Config) -> list[Dataset]:
    times_scraper = TimesScraper(config.team_filter)
    balloting_scraper = BallotingScraper()

    def fetch_times(client):
        raw = times_scraper.fetch(client)
        return raw if raw.empty else clean_up_formatting(raw)

    return [
        Dataset(
            name=TIMES,
            title="Performance times",
            columns=tuple(COLUMNS),
            numeric_columns=frozenset({"Spkr Pos.", "Seconds", "Rank"}),
            fetch=fetch_times,
        ),
        Dataset(
            name=BALLOTING,
            title="Ballot status",
            columns=tuple(BALLOTING_COLUMNS),
            numeric_columns=frozenset({"Slot"}),
            fetch=balloting_scraper.fetch,
        ),
    ]
