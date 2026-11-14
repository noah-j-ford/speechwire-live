import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from speechwire_live.config import load_config


def write(directory, text):
    path = Path(directory) / "config.toml"
    path.write_text(text)
    return path


class ConfigTests(unittest.TestCase):
    def test_reads_file_and_applies_types_and_defaults(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {}, clear=True):
            path = write(d, 'username = "u"\npassword = "p"\ntournament_id = 123\npoll_seconds = "30"\n')
            config = load_config(path)
        self.assertEqual((config.username, config.tournament_id, config.poll_seconds), ("u", "123", 30))
        self.assertEqual(config.port, 8080)

    def test_credentials_and_tournament_are_optional(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {}, clear=True):
            config = load_config(Path(d) / "missing.toml")
        self.assertEqual((config.username, config.password, config.tournament_id), ("", "", ""))

    def test_environment_overrides_file(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.dict(
            os.environ, {"SPEECHWIRE_PASSWORD": "from-env"}, clear=True
        ):
            config = load_config(write(d, 'username = "u"\npassword = "from-file"\n'))
        self.assertEqual(config.password, "from-env")

    def test_unknown_setting_is_rejected(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit):
                load_config(write(d, 'typo_setting = 1\n'))


if __name__ == "__main__":
    unittest.main()
