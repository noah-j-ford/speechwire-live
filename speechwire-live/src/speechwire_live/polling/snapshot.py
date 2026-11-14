from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from ..client.base import SpeechwireClient


@dataclass(frozen=True)
class Dataset:
    name: str
    title: str
    columns: tuple[str, ...]
    numeric_columns: frozenset[str]
    fetch: Callable[[SpeechwireClient], pd.DataFrame]


@dataclass(frozen=True)
class Snapshot:
    df: pd.DataFrame
    version: int
    taken_at: datetime
