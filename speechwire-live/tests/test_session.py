import time
import unittest

from speechwire_live.client.tournament_lookup import Tournament
from speechwire_live.config import Config
from speechwire_live.session import Session

CALENDAR_PICK = Tournament("Alpha Invitational", "111")


class RecordingClient:
    created = []

    def __init__(self, username, password, tournament_id):
        RecordingClient.created.append((username, password, tournament_id))

    def get_html(self, page, params=None):
        return "<html></html>"


class SessionTests(unittest.TestCase):
    def make_session(self, **config_values):
        RecordingClient.created = []
        session = Session(Config(**config_values), client_factory=RecordingClient)
        self.addCleanup(session.end)
        return session

    def test_default_flow_picks_a_tournament_then_logs_in_with_typed_credentials(self):
        session = self.make_session()
        self.assertEqual(session.stage, "tournament")
        session.choose_tournament(CALENDAR_PICK)
        self.assertEqual(session.stage, "login")
        session.log_in("typed-user", "typed-pass")
        self.assertEqual(session.stage, "dashboard")
        self.assertEqual(session.tournament.name, "Alpha Invitational")
        self.assertIn("times", session.datasets)

    def test_poller_logs_in_with_the_typed_credentials_and_selected_tournament(self):
        session = self.make_session()
        session.choose_tournament(CALENDAR_PICK)
        session.log_in("typed-user", "typed-pass")
        deadline = time.monotonic() + 3
        while not RecordingClient.created and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertEqual(RecordingClient.created[0], ("typed-user", "typed-pass", "111"))

    def test_back_returns_to_the_tournament_picker(self):
        session = self.make_session()
        session.choose_tournament(CALENDAR_PICK)
        session.clear_tournament()
        self.assertEqual(session.stage, "tournament")

    def test_end_stops_the_poller_and_returns_to_the_picker(self):
        session = self.make_session()
        session.choose_tournament(CALENDAR_PICK)
        session.log_in("u", "p")
        poller = session.poller
        session.end()
        self.assertEqual(session.stage, "tournament")
        self.assertTrue(poller._stop.is_set())

    def test_configured_tournament_skips_the_picker(self):
        session = self.make_session(tournament_id="999", tournament_name="Configured Cup")
        self.assertEqual(session.stage, "login")
        self.assertEqual(session.tournament.name, "Configured Cup")

    def test_configured_credentials_skip_the_login_form(self):
        session = self.make_session(username="cfg-user", password="cfg-pass")
        session.choose_tournament(CALENDAR_PICK)
        self.assertEqual(session.stage, "dashboard")

    def test_fully_configured_app_logs_in_on_startup(self):
        session = self.make_session(tournament_id="999", username="u", password="p")
        session.start_from_config()
        self.assertEqual(session.stage, "dashboard")

    def test_start_from_config_does_nothing_without_a_full_configuration(self):
        session = self.make_session(username="u", password="p")
        session.start_from_config()
        self.assertEqual(session.stage, "tournament")

    def test_save_latest_returns_none_without_data(self):
        session = self.make_session()
        self.assertIsNone(session.save_latest())
        session.choose_tournament(CALENDAR_PICK)
        session.log_in("u", "p")
        self.assertIsNone(session.save_latest())


if __name__ == "__main__":
    unittest.main()
