import time
import unittest

import pandas as pd

from speechwire_live.polling.poller import EmptyScrape, Poller
from speechwire_live.polling.snapshot import Dataset


def make_dataset(results):
    results = list(results)

    def fetch(client):
        return results.pop(0) if len(results) > 1 else results[0]

    return Dataset("t", "Test data", ("a",), frozenset(), fetch)


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
        poller._scrape(None, dataset)
        self.assertEqual(poller.snapshot("t").version, 1)
        poller._scrape(None, dataset)
        self.assertEqual(poller.snapshot("t").version, 1)
        self.assertIn("no changes", poller.status)
        poller._scrape(None, dataset)
        self.assertEqual(poller.snapshot("t").version, 2)

    def test_empty_scrape_raises_and_keeps_the_last_good_snapshot(self):
        dataset = make_dataset([frame(1), pd.DataFrame()])
        poller = Poller(lambda: object(), [dataset], 60)
        poller._scrape(None, dataset)
        with self.assertRaises(EmptyScrape):
            poller._scrape(None, dataset)
        self.assertEqual(poller.snapshot("t").df["a"].tolist(), [1])

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


if __name__ == "__main__":
    unittest.main()
