# TODO

Roadmap and open tasks. Architecture and conventions are in [README.md](README.md); rules for AI coding agents are in [AGENTS.md](AGENTS.md).

Each dataset below follows the same pipeline (scraper → cleaner → poller → view), so every feature is "one scraper, one cleaner, one view, registered in `datasets.py`."

## Done (covered by unit tests)

- [x] Client interface and live client (login and page fetching)
- [x] Performance-times scraper and cleaner, moved into their own modules
- [x] Skip event IDs that returned nothing, with a periodic full rescan
- [x] Poller that keeps the last good snapshot, re-logs in after failures, and enforces a minimum interval
- [x] Poller keeps going when one dataset fails, so a broken scrape no longer blocks the others
- [x] `.xlsx` export with the original column formatting
- [x] Config from `config.toml` or `SPEECHWIRE_*` environment variables (credentials out of source)
- [x] Tournament picker and login form in the UI, with credentials held in memory only; a configured tournament or login skips the matching step
- [x] Session flow: pick tournament → log in → dashboard → switch tournament (logic only; the screens are unverified)
- [x] `pyproject.toml`, `.gitignore`, `config.example.toml`

## Needs verification

These are implemented but have not been run for real.

- [ ] Run the NiceGUI dashboard and confirm the table renders (the UI modules were only checked with a mocked NiceGUI)
- [ ] Confirm sort, filters, and column widths survive a data refresh (relies on AG Grid's `setGridOption('rowData', ...)` through NiceGUI's `run_grid_method`)
- [ ] Confirm columns auto-size on first load
- [ ] Balloting scrape against real pages: slot IDs 1 to 29 are probed, the table is at `/html/body/table`, and its header cells read Section, Rm, Judge, Status (unit tests use hand-written pages)
- [ ] What Speechwire returns for a slot ID that does not exist (assumed: a page with no table at `/html/body/table`)
- [ ] Whether the ballot pages say which round and time a slot is. Tables are labeled "Slot N" plus any short text found outside the table, which may be empty or noisy.
- [ ] `/balloting` rendering: separate tables, the status colors, and the table height (grid auto-height)
- [ ] Log in and scrape a real tournament through the new client and scraper
- [ ] Tournament picker against the real Speechwire calendar page (the unit test uses a hand-built page that mirrors the old parsing code)
- [ ] Log in through the form with real credentials and confirm the dashboard fills
- [ ] Switch tournament saves the file and returns to the picker
- [ ] Confirm the file is saved on shutdown (Ctrl+C) and from the Save .xlsx button
- [ ] Open the dashboard from a second device with `host = "0.0.0.0"`
- [ ] Confirm `pip install -e .` pulls a NiceGUI version that supports these calls
- [ ] Landing page, navigation bar, `/times`, and the placeholder pages render and link correctly (only checked against a mocked NiceGUI, so layout is unseen, including the table height under the new toolbar)

## Housekeeping

- [ ] Add your existing `standardization.py` to `src/speechwire_live/cleaning/`
- [ ] Save real Speechwire HTML pages as test fixtures (current tests use small hand-written pages)
- [ ] Make sure no credentials exist anywhere in the Git history before the repository is pushed to GitHub (rotate them if they ever did)
- [ ] Add a license
- [ ] Show a clear error on the login form when Speechwire rejects the credentials (today it only appears as an empty-scrape error in the dashboard status; how Speechwire signals a failed login is not yet known)
- [ ] Add authentication to the dashboard before exposing it beyond localhost

## Roadmap

### 1. Balloting status: all rounds at once `major`
- [x] Scrape the balloting status page for every round (unit-tested with hand-written pages)
- [x] Parse the tables into a consistent data structure
- [ ] Replace the placeholder at `/balloting` with a view displaying every table separately on one screen (built; awaiting verification)
- [x] Auto-refresh with the same polling mechanism as the times view
- [ ] Color the Status cells: IN dark green, NOT STARTED dark gray, anything else bright green (built; awaiting verification)

### 2. Global balloting progress bar `minor`
- [ ] Compute overall balloting completion across all rounds (ballots in / ballots expected)
- [ ] Small global progress bar in the page header, visible from every view
- [ ] Optional: per-round breakdown on hover or click

### 3. Simulated tournament for testing `major · low priority`
Goal: exercise the UI and features when no tournament is running, and jump ahead to later stages (e.g. finals) instead of waiting hours in real time. Three candidate approaches, which are not mutually exclusive:

- [ ] **A. Skeleton tournament:** a tiny hand-built tournament (a few events, teams, and rounds) for unit tests and quick UI checks
- [ ] **B. Record and replay with time travel:** capture the Speechwire responses across a full tournament, then replay them through a fake client that can fast-forward to any point in time
- [ ] **C. Drip-fed results:** take the static end-of-tournament data from a real tournament and release it gradually over a few minutes

Design notes:
- [ ] Implement the simulation as another implementation of the client interface (`client/base.py`), so A, B, and C plug in the same way as the live client
- [ ] Controls for the simulation: speed multiplier, jump to round, pause/reset

### 4. Live "Print Results" view `major`
- [ ] Scrape the print results page
- [ ] Replace the placeholder at `/results` with the real view
- [ ] Display tournament ranks as they come in
- [ ] Constant polling, no manual refresh needed
- [ ] Highlight rows that changed since the last poll

### 5. Live team sweepstakes view `major`
- [ ] Scrape the team sweepstakes results page
- [ ] Replace the placeholder at `/sweepstakes` with the real view
- [ ] Display standings with the same live-polling behavior as item 4
- [ ] Highlight rank changes between polls
