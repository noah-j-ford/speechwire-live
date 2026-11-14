import unittest

from speechwire_live.scrapers.sweepstakes import (
    COLUMNS,
    PAGE,
    PARAMS,
    SweepstakesScraper,
    parse_page,
)

PAGE_HTML = """
<html><body>
<table class="ddprint">
  <tr><th>Place</th><th>Team</th><th>Points</th></tr>
  <tr><td>1</td><td>Lincoln East</td><td>42.5</td></tr>
  <tr><td>2</td><td>Lincoln Southwest</td><td>37</td></tr>
</table>
</body></html>
"""


class FakeClient:
    def __init__(self, html):
        self.html = html
        self.requests = []

    def get_html(self, page, params=None):
        self.requests.append((page, params))
        return self.html


class SweepstakesScraperTests(unittest.TestCase):
    def test_extracts_the_sweepstakes_table(self):
        result = parse_page(PAGE_HTML)

        self.assertEqual(list(result.columns), COLUMNS)
        self.assertEqual(result.iloc[0]["Headers"], ("Place", "Team", "Points"))
        self.assertEqual(
            result.iloc[0]["Rows"],
            ((1, "Lincoln East", 42.5), (2, "Lincoln Southwest", 37)),
        )

    def test_uses_first_row_as_headers_when_th_cells_are_absent(self):
        html = PAGE_HTML.replace("<th>", "<td>").replace("</th>", "</td>")

        result = parse_page(html)

        self.assertEqual(result.iloc[0]["Headers"], ("Place", "Team", "Points"))
        self.assertEqual(result.iloc[0]["Rows"][0], ("1", "Lincoln East", "42.5"))

    def test_requires_one_sweepstakes_table(self):
        with self.assertRaisesRegex(ValueError, "Expected one sweepstakes table, found 0"):
            parse_page("<html><body></body></html>")

    def test_scraper_requests_the_team_print_page(self):
        client = FakeClient(PAGE_HTML)

        SweepstakesScraper().fetch(client)

        self.assertEqual(client.requests, [(PAGE, PARAMS)])


if __name__ == "__main__":
    unittest.main()
