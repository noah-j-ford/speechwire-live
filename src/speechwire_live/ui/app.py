from nicegui import app, ui

from ..config import Config
from ..session import Session
from .balloting_view import build_balloting
from .landing_view import build_landing
from .page_shell import PageBuilder, run_page
from .pages import FEATURES, HOME, PageInfo
from .placeholder_view import build_placeholder
from .results_view import build_results
from .times_view import build_times
from .sweepstakes_view import build_sweepstakes

BUILDERS: dict[str, PageBuilder] = {
    "/": build_landing,
    "/times": build_times,
    "/balloting": build_balloting,
    "/results": build_results,
    "/sweepstakes": build_sweepstakes,
}


def _register_page(session: Session, page: PageInfo) -> None:
    build_content = BUILDERS[page.path] if page.built else build_placeholder(page)

    @ui.page(page.path)
    async def _page():
        await run_page(session, page, build_content)


def run_app(config: Config) -> None:
    ui.add_css(
        "body { font-family: Tahoma, sans-serif; } "
        ".ag-root-wrapper { font-family: Tahoma, sans-serif; "
        "--ag-font-family: Tahoma, sans-serif; } "
        ".ag-header-cell.centered-header .ag-header-cell-label "
        "{ justify-content: center; }",
        shared=True,
    )
    session = Session(config)
    app.on_startup(session.start_from_config)
    app.on_shutdown(session.shutdown)
    for page in (HOME, *FEATURES):
        _register_page(session, page)
    ui.run(host=config.host, port=config.port, title="Speechwire Live", reload=False)
