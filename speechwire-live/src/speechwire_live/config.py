import os
import tomllib
from dataclasses import dataclass, fields
from pathlib import Path


@dataclass(frozen=True)
class Config:
    username: str = ""
    password: str = ""
    tournament_id: str = ""
    tournament_name: str = ""
    team_filter: str = ""
    season_id: int = 19
    poll_seconds: int = 120
    host: str = "127.0.0.1"
    port: int = 8080


def load_config(path=None) -> Config:
    path = Path(path or os.environ.get("SPEECHWIRE_CONFIG", "config.toml"))
    values = {}
    if path.exists():
        with path.open("rb") as f:
            values = tomllib.load(f)

    for field in fields(Config):
        env_value = os.environ.get(f"SPEECHWIRE_{field.name.upper()}")
        if env_value is not None:
            values[field.name] = env_value

    known = {field.name for field in fields(Config)}
    unknown = sorted(set(values) - known)
    if unknown:
        raise SystemExit(f"Unknown setting(s) in {path}: {', '.join(unknown)}")

    for field in fields(Config):
        if field.name in values:
            values[field.name] = field.type(values[field.name])
    return Config(**values)
