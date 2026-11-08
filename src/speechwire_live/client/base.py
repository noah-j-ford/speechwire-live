from collections.abc import Mapping
from typing import Protocol


class SpeechwireClient(Protocol):
    def get_html(self, page: str, params: Mapping[str, str] | None = None) -> str:
        """Return the HTML of a Speechwire manager page."""
