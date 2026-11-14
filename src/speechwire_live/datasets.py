from .cleaning.times import COLUMNS, clean_up_formatting
from .cleaning.sweepstakes import clean_sweepstakes
from .config import Config
from .polling.snapshot import Dataset
from .scrapers.balloting import COLUMNS as BALLOTING_COLUMNS
from .scrapers.balloting import BallotingScraper
from .scrapers.results import COLUMNS as RESULTS_COLUMNS
from .scrapers.results import ResultsScraper
from .scrapers.sweepstakes import COLUMNS as SWEEPSTAKES_COLUMNS
from .scrapers.sweepstakes import SweepstakesScraper
from .scrapers.times import TimesScraper

TIMES = "times"
BALLOTING = "balloting"
RESULTS = "results"
SWEEPSTAKES = "sweepstakes"


def build_datasets(config: Config) -> list[Dataset]:
    times_scraper = TimesScraper(config.team_filter)
    balloting_scraper = BallotingScraper()
    results_scraper = ResultsScraper()
    sweepstakes_scraper = SweepstakesScraper()

    def fetch_times(client):
        raw = times_scraper.fetch(client)
        return raw if raw.empty else clean_up_formatting(raw)

    def fetch_sweepstakes(client):
        return clean_sweepstakes(sweepstakes_scraper.fetch(client))

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
        Dataset(
            name=RESULTS,
            title="Results",
            columns=tuple(RESULTS_COLUMNS),
            numeric_columns=frozenset(),
            fetch=results_scraper.fetch,
        ),
        Dataset(
            name=SWEEPSTAKES,
            title="Team sweepstakes",
            columns=tuple(SWEEPSTAKES_COLUMNS),
            numeric_columns=frozenset(),
            fetch=fetch_sweepstakes,
        ),
    ]
