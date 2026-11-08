import tempfile
import unittest
import zipfile

import pandas as pd

from speechwire_live.export.xlsx import save_times


class ExportTests(unittest.TestCase):
    def test_writes_a_valid_xlsx_file_with_the_tournament_name(self):
        df = pd.DataFrame({"Event": ["IMP"], "Seconds": [330]})
        with tempfile.TemporaryDirectory() as directory:
            path = save_times(df, "Demo", directory)
            self.assertTrue(path.name.startswith("Demo ") and path.name.endswith(" Times.xlsx"))
            with zipfile.ZipFile(path) as archive:
                self.assertIn("xl/workbook.xml", archive.namelist())
                self.assertIn("Demo", archive.read("xl/workbook.xml").decode())


if __name__ == "__main__":
    unittest.main()
