import unittest

import pandas as pd

from speechwire_live.ui.ballot_rows import split_into_slot_tables, status_style


class StatusStyleTests(unittest.TestCase):
    def test_in_is_dark_green_with_white_text(self):
        self.assertEqual(status_style("IN"), {"backgroundColor": "#006400", "color": "#ffffff"})

    def test_not_started_is_dark_gray_with_white_text(self):
        self.assertEqual(status_style("NOT STARTED"), {"backgroundColor": "#4a4a4a", "color": "#ffffff"})

    def test_anything_else_is_bright_green_with_black_text(self):
        for status in ["", "STARTED", "Judge Late", "in"]:
            with self.subTest(status=status):
                self.assertEqual(status_style(status), {"backgroundColor": "#00ff00", "color": "#000000"})

    def test_surrounding_whitespace_is_ignored(self):
        self.assertEqual(status_style(" IN ")["backgroundColor"], "#006400")


class SplitTests(unittest.TestCase):
    def test_one_table_per_slot_in_slot_order_with_row_order_kept(self):
        df = pd.DataFrame(
            {
                "Slot": [9, 3, 9],
                "Title": ["Finals", "Round 1", "Finals"],
                "Section": ["1", "1", "2"],
                "Rm": ["101", "201", "102"],
                "Judge": ["A", "B", "C"],
                "Status": ["IN", "NOT STARTED", "OTHER"],
            }
        )
        tables = split_into_slot_tables(df)
        self.assertEqual([(t.slot, t.title) for t in tables], [(3, "Round 1"), (9, "Finals")])
        self.assertEqual([row["Judge"] for row in tables[1].rows], ["A", "C"])
        self.assertEqual(tables[0].rows[0]["statusStyle"]["backgroundColor"], "#4a4a4a")
        self.assertEqual(tables[1].rows[1]["statusStyle"]["backgroundColor"], "#00ff00")


if __name__ == "__main__":
    unittest.main()
