import unittest

import pandas as pd

from speechwire_live.scrapers.times import EVENT_IDS, TimesScraper, parse_page

HEADER = (
    "<tr><td>Section</td><td>Spkr Pos.</td><td>Entry</td><td>Team</td>"
    "<td>Time</td><td>Rank</td><td>Judge</td></tr>"
)


def grouping_page(event, rows=()):
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    table = f"<table class='dd'>{HEADER}{body}</table>" if rows else ""
    return (
        f"<html><body>Selected grouping: {event}"
        f"Please select a round to view performance times for:{table}</body></html>"
    )


NOT_A_GROUPING = "<html><body>Nothing here</body></html>"
ROW_A = ("1", "1", "101 Ann Lee", "North High School", "5:10", "2", "J1 Pat Kim")
ROW_B = ("1", "2", "102 Bo Ray", "South High School", "4:55", "1", "J1 Pat Kim")


class FakeClient:
    def __init__(self, pages):
        self.pages = pages
        self.requests = []

    def get_html(self, page, params=None):
        key = (int(params["groupingid"]), params["selround"])
        self.requests.append(key)
        return self.pages.get(key, NOT_A_GROUPING)


class ParsePageTests(unittest.TestCase):
    def test_returns_event_and_table_with_event_and_round_columns(self):
        event, table = parse_page(grouping_page("IMP", [ROW_A, ROW_B]), "2")
        self.assertEqual(event, "IMP")
        self.assertEqual(len(table), 2)
        self.assertEqual(table["Event"].tolist(), ["IMP", "IMP"])
        self.assertEqual(table["Rd"].tolist(), ["2", "2"])

    def test_team_filter_keeps_only_matching_team(self):
        _, table = parse_page(grouping_page("IMP", [ROW_A, ROW_B]), "1", "South High School")
        self.assertEqual(table["Entry"].tolist(), ["102 Bo Ray"])

    def test_page_without_grouping_returns_none_event(self):
        self.assertEqual(parse_page(NOT_A_GROUPING, "1"), (None, None))

    def test_grouping_without_table_returns_event_only(self):
        self.assertEqual(parse_page(grouping_page("IMP"), "1"), ("IMP", None))


class TimesScraperTests(unittest.TestCase):
    def setUp(self):
        self.pages = {
            (1, "1"): grouping_page("IMP", [ROW_A, ROW_B]),
            (1, "2"): grouping_page("IMP"),
            (1, "3"): grouping_page("IMP"),
            (1, "F"): grouping_page("IMP"),
        }

    def test_first_scrape_probes_every_id_and_returns_expected_columns(self):
        client = FakeClient(self.pages)
        df = TimesScraper().fetch(client)
        self.assertEqual(len(client.requests), 4 + (len(EVENT_IDS) - 1))
        self.assertEqual(
            list(df.columns),
            ["Event", "Section", "Spkr Pos.", "Rd", "Entry", "Team", "Time", "Rank", "Judge"],
        )
        self.assertEqual(len(df), 2)

    def test_later_scrapes_skip_ids_that_returned_nothing(self):
        scraper = TimesScraper()
        scraper.fetch(FakeClient(self.pages))
        client = FakeClient(self.pages)
        scraper.fetch(client)
        self.assertEqual({event_id for event_id, _ in client.requests}, {1})

    def test_event_that_starts_late_is_found_on_the_next_full_rescan(self):
        scraper = TimesScraper()
        scraper.fetch(FakeClient(self.pages))
        late = dict(self.pages)
        late[(2, "1")] = grouping_page("EXT", [ROW_A])
        for _ in range(9):
            scraper.fetch(FakeClient(self.pages))
        df = scraper.fetch(FakeClient(late))
        self.assertIn("EXT", df["Event"].tolist())

    def test_scrape_with_no_data_returns_empty_and_does_not_poison_skip_list(self):
        scraper = TimesScraper()
        self.assertTrue(scraper.fetch(FakeClient({})).empty)
        client = FakeClient(self.pages)
        df = scraper.fetch(client)
        self.assertFalse(df.empty)
        self.assertEqual(len(client.requests), 4 + (len(EVENT_IDS) - 1))


if __name__ == "__main__":
    unittest.main()
