from .config import load_config
from .ui.app import run_app


def main() -> None:
    run_app(load_config())


if __name__ == "__main__":
    main()
