import unittest

import numpy as np
import pandas as pd

from speechwire_live.ui.grid_rows import to_grid_rows

NUMERIC = frozenset({"Rank", "Seconds"})


class GridRowsTests(unittest.TestCase):
    def test_nan_becomes_null_and_numeric_text_becomes_numbers(self):
        df = pd.DataFrame(
            {"Event": ["IMP", "EXT"], "Rank": ["1", ""], "Seconds": [330.0, np.nan]}
        )
        rows = to_grid_rows(df, NUMERIC)
        self.assertEqual(rows[0], {"Event": "IMP", "Rank": 1, "Seconds": 330.0})
        self.assertEqual(rows[1], {"Event": "EXT", "Rank": None, "Seconds": None})

    def test_text_in_a_numeric_column_is_kept_rather_than_dropped(self):
        df = pd.DataFrame({"Rank": ["1", "DQ"], "Seconds": [1.0, 2.0]})
        rows = to_grid_rows(df, NUMERIC)
        self.assertEqual([row["Rank"] for row in rows], ["1", "DQ"])

    def test_original_frame_is_not_modified(self):
        df = pd.DataFrame({"Rank": ["1"], "Seconds": [1.0]})
        to_grid_rows(df, NUMERIC)
        self.assertEqual(df["Rank"].tolist(), ["1"])


if __name__ == "__main__":
    unittest.main()
