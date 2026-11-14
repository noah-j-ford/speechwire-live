import unittest

from speechwire_live.scrapers.results import COLUMNS, PAGE, PARAMS, ResultsScraper, parse_page

PAGE_HTML = """
<html><body>
<p><span>Voice of the Vista</span><span>IMP</span></p>
<table class="ddprint">
  <tr><th>Rank</th><th>Entry</th><th>Team</th></tr>
  <tr><td>1</td><td>101 Ann Lee</td><td>North High</td></tr>
</table>
<p><span>Voice of the Vista</span><span>Extemporaneous</span></p>
<table class="ddprint">
  <tr><th>Rank</th><th>Speaker</th></tr>
  <tr><td>2</td><td>102 Bo Ray</td></tr>
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


class ResultsScraperTests(unittest.TestCase):
    def test_extracts_event_labels_and_each_table_shape(self):
        result = parse_page(PAGE_HTML)

        self.assertEqual(list(result.columns), COLUMNS)
        self.assertEqual(result["Event"].tolist(), ["IMP", "Extemporaneous"])
        self.assertEqual(result.iloc[0]["Headers"], ("Rank", "Entry", "Team"))
        self.assertEqual(result.iloc[0]["Rows"], ((1, "101 Ann Lee", "North High"),))
        self.assertEqual(result.iloc[1]["Headers"], ("Rank", "Speaker"))

    def test_ignores_tournament_name_and_non_results_tables(self):
        html = PAGE_HTML.replace('<table class="ddprint">', '<table class="other">', 1)
        result = parse_page(html)

        self.assertEqual(result["Event"].tolist(), ["Extemporaneous"])

    def test_first_row_is_used_for_headings_when_cells_are_not_th(self):
        html = PAGE_HTML.replace("<th>", "<td>").replace("</th>", "</td>")
        result = parse_page(html)

        self.assertEqual(result.iloc[0]["Headers"], ("Rank", "Entry", "Team"))
        self.assertEqual(result.iloc[0]["Rows"], (("1", "101 Ann Lee", "North High"),))

    def test_drops_a_repeated_header_row_before_results(self):
        html = PAGE_HTML.replace(
            '<tr><td>1</td><td>101 Ann Lee</td><td>North High</td></tr>',
            '<tr><td>Rank</td><td>Entry</td><td>Team</td></tr>'
            '<tr><td>1</td><td>101 Ann Lee</td><td>North High</td></tr>',
        )

        result = parse_page(html)

        self.assertEqual(result.iloc[0]["Rows"], (("1", "101 Ann Lee", "North High"),))

    def test_preserves_grouped_header_parts(self):
        html = """
        <p><span>Tournament</span><span>Speech</span></p>
        <table class="ddprint">
          <tr><th rowspan="2">Code</th><th colspan="3">Prelims</th></tr>
          <tr><th>1</th><th>2</th><th>3</th></tr>
          <tr><td>A01</td><td>1</td><td>2</td><td>3</td></tr>
        </table>
        """

        result = parse_page(html)

        self.assertEqual(
            result.iloc[0]["Headers"],
            (("Code", "Code"), ("Prelims", "1"), ("Prelims", "2"), ("Prelims", "3")),
        )
        self.assertEqual(result.iloc[0]["Rows"], (("A01", 1, 2, 3),))

    def test_missing_event_heading_is_an_error(self):
        html = '<html><body><table class="ddprint"><tr><th>Rank</th></tr></table></body></html>'
        with self.assertRaisesRegex(ValueError, "missing its event heading"):
            parse_page(html)

    def test_scraper_requests_the_print_results_page(self):
        client = FakeClient(PAGE_HTML)

        ResultsScraper().fetch(client)

        self.assertEqual(client.requests, [(PAGE, PARAMS)])


if __name__ == "__main__":
    unittest.main()
