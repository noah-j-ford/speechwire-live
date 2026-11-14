import tempfile
import unittest
import zipfile

import pandas as pd

from speechwire_live.export.xlsx import save_times


def workbook_xml(path):
    with zipfile.ZipFile(path) as archive:
        return archive.read("xl/workbook.xml").decode()


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({"Event": ["IMP"], "Seconds": [330]})

    def test_writes_a_valid_xlsx_file_with_the_tournament_name(self):
        with tempfile.TemporaryDirectory() as directory:
            path = save_times(self.df, "Demo", directory)
            self.assertTrue(path.name.startswith("Demo ") and path.name.endswith(" Times.xlsx"))
            self.assertIn('name="Demo"', workbook_xml(path))

    def test_calendar_style_names_are_made_safe_for_excel_and_the_filesystem(self):
        name = "Alpha/Beta: Spring [Varsity] Invitational Speech Tournament"
        with tempfile.TemporaryDirectory() as directory:
            path = save_times(self.df, name, directory)
            self.assertNotIn("/", path.name)
            sheet = workbook_xml(path).split('<sheet name="')[1].split('"')[0]
            self.assertLessEqual(len(sheet), 31)
            self.assertFalse(set(sheet) & set("[]:*?/\\"))


if __name__ == "__main__":
    unittest.main()
