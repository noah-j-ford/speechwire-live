import unittest

import numpy as np
import pandas as pd

from speechwire_live.cleaning.sweepstakes import COLUMNS, clean_sweepstakes


class CleanSweepstakesTests(unittest.TestCase):
    def test_converts_missing_cells_to_empty_strings(self):
        raw = pd.DataFrame(
            [{"Headers": ("Rank", "Team"), "Rows": ((1, "Lincoln East"), (2, np.nan))}]
        )

        cleaned = clean_sweepstakes(raw)

        self.assertEqual(list(cleaned.columns), COLUMNS)
        self.assertEqual(cleaned.iloc[0]["Rows"], ((1, "Lincoln East"), (2, "")))

    def test_empty_standings_remain_empty(self):
        raw = pd.DataFrame([{"Headers": ("Rank",), "Rows": ()}])

        self.assertTrue(clean_sweepstakes(raw).empty)


if __name__ == "__main__":
    unittest.main()
