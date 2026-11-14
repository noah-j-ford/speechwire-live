import unittest

from speechwire_live.ui.results_view import _results_column_defs


class ResultsColumnTests(unittest.TestCase):
    def test_formats_prelim_columns_and_two_line_headers(self):
        headers = (
            ("Prelims", "1"),
            ("Prelims", "2"),
            ("Prelims", "3"),
            "Opp. Avg. Rank",
            "Head to head",
            "Prelim result",
            "Rank total",
            "Final result",
            "Finals ranks",
            "Judges pref.",
        )

        columns = _results_column_defs(headers)

        self.assertEqual([column["headerName"] for column in columns[:3]], ["P1", "P2", "P3"])
        self.assertEqual([column["width"] for column in columns[:3]], [32, 32, 32])
        self.assertEqual(
            [column["headerName"] for column in columns[3:]],
            [
                "Opp. Avg.\nRank",
                "Head to\nhead",
                "Prelim\nresult",
                "Rank\ntotal",
                "Final\nresult",
                "Finals\nranks",
                "Judges\npref.",
            ],
        )
        self.assertEqual(columns[5]["cellStyle"]["fontWeight"], "bold")
        self.assertEqual(columns[7]["cellStyle"]["fontWeight"], "bold")
        self.assertTrue(all(column["headerClass"] == "centered-header" for column in columns))

    def test_numbers_two_prelim_columns_sequentially(self):
        columns = _results_column_defs((("Prelims", "1"), ("Prelims", "2")))

        self.assertEqual([column["headerName"] for column in columns], ["P1", "P2"])


if __name__ == "__main__":
    unittest.main()
