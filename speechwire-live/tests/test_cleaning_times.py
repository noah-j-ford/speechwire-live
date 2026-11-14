import unittest

import numpy as np
import pandas as pd

from speechwire_live.cleaning.times import (
    add_overtime_column,
    convert_time_to_seconds,
    process_time,
)


class ProcessTimeTests(unittest.TestCase):
    def test_normalizes_common_entry_mistakes(self):
        cases = {
            "5:30": "5:30",
            "530": "5:30",
            "5.30": "5:30",
            "5;30": "5:30",
            "7": "7:00",
            "10": "10:00",
            "5:30ish": "5:30",
            "3:15.4": "3:15",
            "": "",
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(process_time(raw), expected)


class ConvertTimeTests(unittest.TestCase):
    def test_minutes_and_seconds(self):
        self.assertEqual(convert_time_to_seconds("5:30"), 330)

    def test_bare_55_means_55_seconds(self):
        self.assertEqual(convert_time_to_seconds("55"), 55)

    def test_unparseable_values_are_nan(self):
        self.assertTrue(np.isnan(convert_time_to_seconds("")))
        self.assertTrue(np.isnan(convert_time_to_seconds("abc")))
        self.assertTrue(np.isnan(convert_time_to_seconds(None)))


class OvertimeTests(unittest.TestCase):
    def test_flags_only_times_over_limit_plus_grace(self):
        df = pd.DataFrame(
            {"Event": ["IMP", "IMP", "IMP"], "Time": ["5:30", "5:31", ""]}
        )
        result = add_overtime_column(df)
        self.assertEqual(result["Overtime"].tolist(), ["", "X", ""])
        self.assertEqual(result["Seconds"].iloc[:2].tolist(), [330, 331])

    def test_unknown_event_is_never_flagged(self):
        df = pd.DataFrame({"Event": ["ZZZ"], "Time": ["59:59"]})
        self.assertEqual(add_overtime_column(df)["Overtime"].tolist(), [""])


if __name__ == "__main__":
    unittest.main()
