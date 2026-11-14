import time
import unittest

import pandas as pd

from speechwire_live.polling.poller import EmptyScrape, Poller
from speechwire_live.polling.snapshot import Dataset


def make_dataset(results, name="t", title="Test data"):
    results = list(results)

    def fetch(client):
        return results.pop(0) if len(results) > 1 else results[0]

    return Dataset(name, title, ("a",), frozenset(), fetch)


def failing_dataset(name, title, error):
    def fetch(client):
        raise error

    return Dataset(name, title, ("a",), frozenset(), fetch)


def frame(*values):
    return pd.DataFrame({"a": list(values)})


def wait_for(condition, timeout=3.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if condition():
            return True
        time.sleep(0.01)
    return False


class ScrapeTests(unittest.TestCase):
    def test_new_data_publishes_a_new_version_and_identical_data_does_not(self):
        dataset = make_dataset([frame(1), frame(1), frame(2)])
        poller = Poller(lambda: object(), [dataset], 60)
        self.assertFalse(poller._poll_once(None))
        self.assertEqual(poller.snapshot("t").version, 1)
        self.assertFalse(poller._poll_once(None))
        self.assertEqual(poller.snapshot("t").version, 1)
        self.assertIn("no changes", poller.status)
        self.assertFalse(poller._poll_once(None))
        self.assertEqual(poller.snapshot("t").version, 2)
        self.assertNotIn("no changes", poller.status)

    def test_empty_scrape_raises_and_keeps_the_last_good_snapshot(self):
        dataset = make_dataset([frame(1), pd.DataFrame()])
        poller = Poller(lambda: object(), [dataset], 60)
        poller._scrape(None, dataset)
        with self.assertRaises(EmptyScrape):
            poller._scrape(None, dataset)
        self.assertEqual(poller.snapshot("t").df["a"].tolist(), [1])

    def test_a_failing_dataset_does_not_stop_the_others(self):
        broken = failing_dataset("bad", "Broken data", RuntimeError("boom"))
        healthy = make_dataset([frame(7)], name="good", title="Good data")
        poller = Poller(lambda: object(), [broken, healthy], 60)
        self.assertTrue(poller._poll_once(None))
        self.assertEqual(poller.snapshot("good").df["a"].tolist(), [7])
        self.assertIsNone(poller.snapshot("bad"))
        self.assertTrue(poller.status.startswith("Error"))
        self.assertIn("Broken data: RuntimeError: boom", poller.status)

    def test_interval_has_a_floor(self):
        poller = Poller(lambda: object(), [], 1)
        self.assertEqual(poller.interval_seconds, 5)
        poller.set_interval(2)
        self.assertEqual(poller.interval_seconds, 5)
        poller.set_interval(90)
        self.assertEqual(poller.interval_seconds, 90)


class ThreadTests(unittest.TestCase):
    def test_failure_is_reported_then_recovers_with_a_fresh_login(self):
        logins = []

        def factory():
            logins.append(1)
            if len(logins) == 1:
                raise RuntimeError("login failed")
            return object()

        poller = Poller(factory, [make_dataset([frame(1)])], 60)
        poller.start()
        try:
            self.assertTrue(wait_for(lambda: poller.status.startswith("Error")))
            self.assertIn("login failed", poller.status)
            poller.refresh_now()
            self.assertTrue(wait_for(lambda: poller.snapshot("t") is not None))
            self.assertEqual(len(logins), 2)
        finally:
            poller.stop()

    def test_a_failed_scrape_triggers_a_fresh_login_on_the_next_cycle(self):
        logins = []

        def factory():
            logins.append(1)
            return object()

        poller = Poller(factory, [failing_dataset("bad", "Broken data", RuntimeError("boom"))], 60)
        poller.start()
        try:
            self.assertTrue(wait_for(lambda: poller.status.startswith("Error")))
            poller.refresh_now()
            self.assertTrue(wait_for(lambda: len(logins) == 2))
        finally:
            poller.stop()


if __name__ == "__main__":
    unittest.main()
