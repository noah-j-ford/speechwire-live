import threading
import time
from collections.abc import Callable
from datetime import datetime

from ..client.base import SpeechwireClient
from .snapshot import Dataset, Snapshot

MIN_INTERVAL_SECONDS = 5


class EmptyScrape(Exception):
    pass


class Poller:
    def __init__(
        self,
        client_factory: Callable[[], SpeechwireClient],
        datasets: list[Dataset],
        interval_seconds: int,
    ):
        self._client_factory = client_factory
        self._datasets = datasets
        self._interval = max(MIN_INTERVAL_SECONDS, int(interval_seconds))
        self._snapshots: dict[str, Snapshot] = {}
        self._status = "Starting..."
        self._stop = threading.Event()
        self._wake = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    @property
    def status(self) -> str:
        return self._status

    @property
    def interval_seconds(self) -> int:
        return self._interval

    def snapshot(self, name: str) -> Snapshot | None:
        return self._snapshots.get(name)

    def set_interval(self, seconds) -> None:
        self._interval = max(MIN_INTERVAL_SECONDS, int(seconds))

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._wake.set()

    def refresh_now(self) -> None:
        self._wake.set()

    def _run(self) -> None:
        client = None
        while not self._stop.is_set():
            try:
                if client is None:
                    self._status = "Logging in..."
                    client = self._client_factory()
                for dataset in self._datasets:
                    self._scrape(client, dataset)
            except Exception as error:
                client = None
                self._status = f"Error: {type(error).__name__}: {error} - will retry"
            self._wake.wait(timeout=self._interval)
            self._wake.clear()

    def _scrape(self, client: SpeechwireClient, dataset: Dataset) -> None:
        self._status = f"Scraping {dataset.title.lower()}..."
        started = time.monotonic()
        df = dataset.fetch(client)
        if df.empty:
            raise EmptyScrape(f"{dataset.title}: scrape returned no rows")

        df = df.reset_index(drop=True)
        previous = self._snapshots.get(dataset.name)
        changed = previous is None or not df.equals(previous.df)
        if changed:
            version = 1 if previous is None else previous.version + 1
            self._snapshots[dataset.name] = Snapshot(df, version, datetime.now())

        elapsed = time.monotonic() - started
        self._status = f"Updated {datetime.now():%H:%M:%S} (scrape took {elapsed:.0f}s)"
        if not changed:
            self._status += " - no changes"
