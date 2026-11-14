from collections.abc import Callable
from pathlib import Path

from .client.base import SpeechwireClient
from .client.live import LiveClient
from .client.tournament_lookup import Tournament
from .config import Config
from .datasets import TIMES, build_datasets
from .export.xlsx import save_times
from .polling.poller import Poller
from .polling.snapshot import Dataset


class Session:
    """The server-wide state: which tournament is selected and the poller logged in to it.

    Credentials are held in memory only, inside the poller's client factory.
    """

    def __init__(
        self,
        config: Config,
        client_factory: Callable[[str, str, str], SpeechwireClient] = LiveClient,
    ):
        self.config = config
        self._client_factory = client_factory
        self.tournament: Tournament | None = None
        if config.tournament_id:
            self.tournament = Tournament(
                config.tournament_name or config.tournament_id, config.tournament_id
            )
        self.poller: Poller | None = None
        self.datasets: dict[str, Dataset] = {}

    @property
    def stage(self) -> str:
        if self.poller is not None:
            return "dashboard"
        return "tournament" if self.tournament is None else "login"

    def start_from_config(self) -> None:
        if self.tournament is not None and self._config_has_credentials():
            self.log_in(self.config.username, self.config.password)

    def choose_tournament(self, tournament: Tournament) -> None:
        self.tournament = tournament
        if self._config_has_credentials():
            self.log_in(self.config.username, self.config.password)

    def clear_tournament(self) -> None:
        self.tournament = None

    def log_in(self, username: str, password: str) -> None:
        tournament_id = self.tournament.id
        self.datasets = {dataset.name: dataset for dataset in build_datasets(self.config)}
        self.poller = Poller(
            lambda: self._client_factory(username, password, tournament_id),
            list(self.datasets.values()),
            self.config.poll_seconds,
        )
        self.poller.start()

    def end(self) -> None:
        if self.poller is not None:
            self.poller.stop()
        self.poller = None
        self.datasets = {}
        self.tournament = None

    def save_latest(self) -> Path | None:
        if self.poller is None:
            return None
        snapshot = self.poller.snapshot(TIMES)
        return save_times(snapshot.df, self.tournament.name) if snapshot else None

    def shutdown(self) -> None:
        if self.poller is not None:
            self.poller.stop()
        self.save_latest()

    def _config_has_credentials(self) -> bool:
        return bool(self.config.username and self.config.password)
