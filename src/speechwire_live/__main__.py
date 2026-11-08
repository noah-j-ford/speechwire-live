from dataclasses import replace

from .client.tournament_lookup import choose_tournament
from .config import load_config
from .ui.app import run_app


def main() -> None:
    config = load_config()
    if not config.tournament_id:
        config = replace(config, tournament_id=choose_tournament(config.season_id))
    run_app(config)


if __name__ == "__main__":
    main()
