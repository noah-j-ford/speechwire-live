import unittest

from speechwire_live.ui.pages import FEATURES, HOME


class PagesTests(unittest.TestCase):
    def test_paths_and_titles_are_unique_and_absolute(self):
        pages = (HOME, *FEATURES)
        paths = [page.path for page in pages]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(len({page.title for page in pages}), len(pages))
        self.assertTrue(all(path.startswith("/") for path in paths))


if __name__ == "__main__":
    unittest.main()
