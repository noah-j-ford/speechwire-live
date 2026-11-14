from dataclasses import dataclass


@dataclass(frozen=True)
class PageInfo:
    title: str
    path: str
    description: str
    built: bool


HOME = PageInfo("Home", "/", "", True)

FEATURES = (
    PageInfo("Times", "/times", "Performance times for every event and round", True),
    PageInfo("Ballot Status", "/balloting", "Balloting status for all rounds at once", True),
    PageInfo("Results", "/results", "Tournament ranks as they come in", False),
    PageInfo("Team Sweepstakes", "/sweepstakes", "Team sweepstakes standings", False),
)
