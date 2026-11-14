from dataclasses import dataclass

import lxml.etree
import lxml.html
import pandas as pd

from ..client.base import SpeechwireClient

PAGE = "ballots-byslot.php"
# Slot IDs are small integers whose order does not follow the round order, so a fixed range is probed.
SLOT_IDS = range(1, 30)
# Every Nth successful scrape re-probes all unknown IDs, so a round whose page only gets a table
# once it is paired is found within a few polls.
FULL_RESCAN_EVERY = 3
HEADER = ["Section", "Rm", "Judge", "Status"]
COLUMNS = ["Slot", "Title", *HEADER]
MAX_HEADING_LENGTH = 120


@dataclass(frozen=True)
class SlotPage:
    heading: str
    rows: list[list[str]]


def _text(element) -> str:
    return " ".join(element.text_content().split())


def _heading(document) -> str:
    body = document.xpath("/html/body")[0]
    parts = body.xpath("./text()") + [
        _text(element)
        for element in body.xpath("./*[not(self::table or self::script or self::style)]")
    ]
    heading = " ".join(" ".join(parts).split())
    return heading if len(heading) <= MAX_HEADING_LENGTH else ""


def parse_page(html: str) -> SlotPage | None:
    """Return the page's table, or None when there is no table at /html/body/table."""
    if not html.strip():
        return None
    try:
        document = lxml.html.document_fromstring(html)
    except lxml.etree.ParserError:
        return None
    tables = document.xpath("/html/body/table")
    if not tables:
        return None

    rows = [
        [_text(cell) for cell in tr.xpath("./th|./td")] for tr in tables[0].xpath(".//tr")
    ]
    if not rows:
        return SlotPage(_heading(document), [])
    header_index = next((i for i, row in enumerate(rows) if row == HEADER), None)
    if header_index is None:
        raise ValueError(f"Unexpected ballot status table header: {rows[0]}")
    data = [row for row in rows[header_index + 1:] if len(row) == len(HEADER)]
    return SlotPage(_heading(document), data)


class BallotingScraper:
    def __init__(self):
        self._known_ids: set[int] = set()
        self._empty_ids: set[int] = set()
        self._successful_scrapes = 0

    def fetch(self, client: SpeechwireClient) -> pd.DataFrame:
        full_scan = self._successful_scrapes % FULL_RESCAN_EVERY == 0
        skip_ids = set() if full_scan else self._empty_ids
        found: dict[int, SlotPage] = {}
        newly_empty: set[int] = set()

        for slot_id in SLOT_IDS:
            if slot_id in skip_ids:
                continue
            html = client.get_html(PAGE, {"selslotid": str(slot_id), "sortmode": "status"})
            page = parse_page(html)
            if page is not None:
                found[slot_id] = page
            elif slot_id in self._known_ids:
                # A slot that had a table before and now has none is a failed fetch, not a
                # removed round, so the previous snapshot is kept.
                raise RuntimeError(f"Ballot status page for slot {slot_id} returned no table")
            else:
                newly_empty.add(slot_id)

        frames = [
            pd.DataFrame(page.rows, columns=HEADER).assign(Slot=slot_id, Title=page.heading)
            for slot_id, page in found.items()
        ]
        if not frames:
            return pd.DataFrame()
        df = pd.concat(frames, ignore_index=True)[COLUMNS]
        df["Slot"] = df["Slot"].astype(int)

        # An empty result usually means a failed login or a site hiccup, so the known and empty
        # ID lists are only updated after a scrape that found rows.
        if not df.empty:
            self._known_ids |= set(found)
            self._empty_ids = newly_empty if full_scan else self._empty_ids | newly_empty
            self._successful_scrapes += 1
        return df
