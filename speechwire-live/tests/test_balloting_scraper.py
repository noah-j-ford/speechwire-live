import unittest

from speechwire_live.scrapers.balloting import (
    COLUMNS,
    SLOT_IDS,
    BallotingScraper,
    parse_page,
)

NO_TABLE = "<html><body><p>Nothing here</p></body></html>"


def table(rows, header_tag="th"):
    head = "".join(f"<{header_tag}>{name}</{header_tag}>" for name in ["Section", "Rm", "Judge", "Status"])
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    return f"<table><tr>{head}</tr>{body}</table>"


def page(rows, before="", header_tag="th"):
    return f"<html><body>{before}{table(rows, header_tag)}</body></html>"


ROWS = [
    ("1", "101", "Pat  Kim", "IN"),
    ("2", "102", "Lee Ray", "NOT STARTED"),
]


class ParsePageTests(unittest.TestCase):
    def test_reads_rows_with_normalized_whitespace(self):
        result = parse_page(page(ROWS))
        self.assertEqual(result.rows[0], ["1", "101", "Pat Kim", "IN"])
        self.assertEqual(len(result.rows), 2)

    def test_header_may_be_th_or_td_cells(self):
        self.assertEqual(len(parse_page(page(ROWS, header_tag="td")).rows), 2)

    def test_page_without_a_table_returns_none(self):
        self.assertIsNone(parse_page(NO_TABLE))
        self.assertIsNone(parse_page(""))

    def test_table_not_directly_under_body_is_ignored(self):
        html = f"<html><body><div>{table(ROWS)}</div></body></html>"
        self.assertIsNone(parse_page(html))

    def test_table_with_only_a_header_has_no_rows(self):
        self.assertEqual(parse_page(page([])).rows, [])

    def test_rows_with_the_wrong_number_of_cells_are_skipped(self):
        result = parse_page(page(ROWS + [("Spacer",)]))
        self.assertEqual(len(result.rows), 2)

    def test_unexpected_header_raises_a_clear_error(self):
        html = "<html><body><table><tr><td>Foo</td><td>Bar</td></tr></table></body></html>"
        with self.assertRaises(ValueError) as raised:
            parse_page(html)
        self.assertIn("Foo", str(raised.exception))

    def test_short_text_outside_the_table_becomes_the_heading(self):
        self.assertEqual(parse_page(page(ROWS, before="<h2>Round 1 - 9:00 AM</h2>")).heading, "Round 1 - 9:00 AM")
        self.assertEqual(parse_page(page(ROWS)).heading, "")

    def test_long_text_outside_the_table_is_not_used_as_a_heading(self):
        self.assertEqual(parse_page(page(ROWS, before="<p>" + "x" * 300 + "</p>")).heading, "")


class FakeClient:
    def __init__(self, pages):
        self.pages = pages
        self.requests = []

    def get_html(self, page_name, params=None):
        slot_id = int(params["selslotid"])
        self.requests.append((page_name, slot_id, params["sortmode"]))
        return self.pages.get(slot_id, NO_TABLE)


class BallotingScraperTests(unittest.TestCase):
    def setUp(self):
        self.pages = {
            9: page(ROWS, before="<h2>Finals</h2>"),
            3: page(ROWS[:1], before="<h2>Round 1</h2>"),
        }

    def test_first_scrape_probes_every_id_and_orders_slots_ascending(self):
        client = FakeClient(self.pages)
        df = BallotingScraper().fetch(client)
        self.assertEqual(len(client.requests), len(SLOT_IDS))
        self.assertEqual(client.requests[0], ("ballots-byslot.php", 1, "status"))
        self.assertEqual(list(df.columns), COLUMNS)
        self.assertEqual(df["Slot"].tolist(), [3, 9, 9])
        self.assertEqual(df["Title"].tolist(), ["Round 1", "Finals", "Finals"])

    def test_later_scrapes_only_request_known_slots(self):
        scraper = BallotingScraper()
        scraper.fetch(FakeClient(self.pages))
        client = FakeClient(self.pages)
        scraper.fetch(client)
        self.assertEqual({slot for _, slot, _ in client.requests}, {3, 9})

    def test_a_round_that_appears_later_is_found_on_the_next_full_rescan(self):
        scraper = BallotingScraper()
        scraper.fetch(FakeClient(self.pages))
        later = dict(self.pages)
        later[5] = page(ROWS, before="<h2>Round 2</h2>")
        scraper.fetch(FakeClient(later))
        scraper.fetch(FakeClient(later))
        df = scraper.fetch(FakeClient(later))
        self.assertIn(5, df["Slot"].tolist())

    def test_a_known_slot_that_loses_its_table_is_an_error_not_a_removed_round(self):
        scraper = BallotingScraper()
        scraper.fetch(FakeClient(self.pages))
        broken = dict(self.pages)
        del broken[9]
        with self.assertRaises(RuntimeError) as raised:
            scraper.fetch(FakeClient(broken))
        self.assertIn("slot 9", str(raised.exception))

    def test_scrape_with_no_tables_returns_empty_and_does_not_poison_the_skip_list(self):
        scraper = BallotingScraper()
        self.assertTrue(scraper.fetch(FakeClient({})).empty)
        client = FakeClient(self.pages)
        self.assertFalse(scraper.fetch(client).empty)
        self.assertEqual(len(client.requests), len(SLOT_IDS))


if __name__ == "__main__":
    unittest.main()
