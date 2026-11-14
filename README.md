# Speechwire Live

A live dashboard for Speechwire tournament managers. It logs in with a manager session, polls Speechwire in the background, and consolidates data that Speechwire spreads across many pages into a web dashboard that updates on its own.

## Why this exists

Speechwire shows tournament data one page at a time. Performance times, for example, live on a separate page for every event and round combination, and ballot status, results, and sweepstakes each have their own pages. Getting a whole-tournament picture means opening dozens of pages and refreshing them by hand. Speechwire Live does that work continuously and shows the result in one place.

## Goals

- See all of a tournament's data in one place, live, with no manual refreshing
- Keep data usable outside the app (`.xlsx` export)
- Make adding a new Speechwire page cheap: one scraper, one cleaner, one view
- Be viewable from any device on the network, not just the machine running the scraper
- Be testable without a running tournament (simulated tournament, saved HTML fixtures)
- Stay polite to Speechwire's servers

## Non-goals

- Changing anything on Speechwire. The app only logs in and reads pages.
- A hosted service. It runs locally with the tournament manager's own credentials.
- A JavaScript or CSS codebase. The interface is written in Python (see UI approach).

## Status

Early development. The performance-times dashboard is implemented and its non-UI logic is unit-tested, but the web interface has not yet been run against a real tournament. Planned work and open verification items are in [TODO.md](TODO.md). Rules for AI coding agents working on this repo are in [AGENTS.md](AGENTS.md).

## UI approach

The interface is a local web app built with [NiceGUI](https://nicegui.io), so every page is written in Python. Tables use AG Grid (bundled with NiceGUI), which provides sorting, per-column filters, and resizable columns without custom code. There is no JavaScript or CSS file in this repository, no npm, and no build step. The one exception is a one-line expression in `ui/balloting_view.py` that tells the grid to use the status colors Python computed for each row. Because the dashboard is served over HTTP, other devices on the network can open it when `host` is set to `0.0.0.0` in the config.

## Architecture

```
Speechwire ──HTTP──▶ Client ──HTML──▶ Scraper ──raw──▶ Cleaner ──DataFrame──▶ Poller ──Snapshot──▶ UI view
                       ▲                                                                       └──▶ Export (.xlsx)
              live | simulated
```

| Layer | Responsibility | Must not |
|---|---|---|
| **Client** | Authenticated session; fetches a Speechwire page by name and parameters. Live and simulated implementations share one interface. | Parse HTML or know about the UI |
| **Scrapers** | One module per Speechwire page type. Use the client to fetch a dataset's pages and parse them into a raw DataFrame. Page parsing is a pure function (HTML in, DataFrame out). | Clean data or touch the UI |
| **Cleaning** | Standardize names, split codes, derive columns (seconds, overtime). Pure functions. | Do network access or touch the UI |
| **Poller** | Background thread. Runs each dataset's fetch → clean pipeline on an interval and publishes snapshots. | Touch the UI |
| **UI** | NiceGUI pages. Each page reads the latest snapshots from the poller on a short timer and renders them. | Do network access or scraping |
| **Export** | Writes snapshots to `.xlsx`. | Fetch or modify data |
| **Simulation** | Implements the client interface with fake data (see [TODO.md](TODO.md), item 3). | Differ from the live client's interface |

## Design conventions

These keep every feature consistent. New code follows them unless there is a strong reason not to.

1. **One pipeline for every dataset.** Adding a dataset means adding a scraper, a cleaner, and a view, then registering a `Dataset` in `datasets.py`. It should not require changes to unrelated layers.
2. **Threading boundary.** Network access happens only on the poller thread. The UI only reads snapshots from the poller. Snapshots are never mutated after they are published.
3. **One shared session.** The poller owns the client. On any failure it discards the client and logs in again on the next cycle.
4. **Keep the last good data.** A failed or empty scrape never replaces a good snapshot. An empty result counts as a failure. A failing dataset does not stop the others. Errors are shown in the status line.
5. **Polite polling.** The interval is measured from the end of a scrape, with a minimum floor. Event IDs that returned nothing are skipped on later polls, with a periodic full rescan so late-starting events are still found.
6. **Schema in one place.** Each `Dataset` declares its columns once. The UI and the export both read from that declaration.
7. **Shared table behavior.** Every table view supports sorting, per-column filtering, and resizable columns, and keeps the user's sort, filters, and column widths across refreshes by replacing only the row data.
8. **Python-only UI.** Interface code uses NiceGUI components and passes AG Grid options as Python dicts. See AGENTS.md for the rules on the rare cases that need a JavaScript snippet.
9. **One URL per view.** Each view is its own page (for example `/times`, `/results`, `/sweepstakes`) with a shared navigation bar, so people can bookmark a view or keep different views open on different devices at once. Per viewer: sort, filters, column widths, and which page is open. Shared by everyone: the data (one poller feeds every viewer, so extra viewers add no load on Speechwire), the refresh interval, and the selected tournament and login. `/` is a landing page with a button for each view, `/times` and `/balloting` are built, and `/results` and `/sweepstakes` are placeholders. To add a view: write its builder, add it to `BUILDERS` in `ui/app.py`, and set `built=True` for its entry in `ui/pages.py`.
10. **Configuration, not constants.** Defaults, polling settings, and optional presets for the tournament and login come from `config.toml` or `SPEECHWIRE_*` environment variables. Credentials typed into the login form are kept in memory only. Nothing sensitive is committed.
11. **Tests use fixtures.** Parsers and cleaners are tested without the network.

## Repository layout

```
speechwire-live/
├── README.md
├── TODO.md
├── AGENTS.md
├── pyproject.toml
├── config.example.toml
├── src/speechwire_live/
│   ├── __main__.py            # entry point
│   ├── config.py              # config.toml + SPEECHWIRE_* environment variables
│   ├── session.py             # selected tournament + logged-in poller (server-wide state)
│   ├── datasets.py            # registers datasets (columns, fetch pipeline)
│   ├── client/
│   │   ├── base.py            # client interface
│   │   ├── live.py            # login + session against Speechwire
│   │   └── tournament_lookup.py   # today's tournaments from the Speechwire calendar
│   ├── scrapers/
│   │   ├── times.py           # performance times
│   │   └── balloting.py       # ballot status tables (planned: print results, sweepstakes)
│   ├── cleaning/
│   │   ├── standardization.py # Standardizer class (not included; add your existing file here)
│   │   └── times.py
│   ├── polling/
│   │   ├── snapshot.py        # Dataset and Snapshot
│   │   └── poller.py
│   ├── ui/
│   │   ├── app.py             # registers every page and starts the app
│   │   ├── pages.py           # list of views: title, URL, description, built or not
│   │   ├── page_shell.py      # header and navigation bar, picker/login until logged in
│   │   ├── setup_views.py     # tournament picker and login form
│   │   ├── landing_view.py    # home page with a button for each view
│   │   ├── times_view.py      # the times page: toolbar and table
│   │   ├── balloting_view.py  # the ballot status page: one table per round
│   │   ├── ballot_rows.py     # status colors and per-round row grouping
│   │   ├── placeholder_view.py    # stand-in for views that are not built yet
│   │   ├── table_view.py      # shared AG Grid table
│   │   └── grid_rows.py       # DataFrame → grid rows
│   ├── export/
│   │   └── xlsx.py
│   └── sim/                   # planned: simulated client
└── tests/
```

## Performance times dataset

Columns, in order: `Event`, `Section`, `Spkr Pos.`, `Rd`, `Speaker Code`, `Entry`, `Team`, `Time`, `Seconds`, `Rank`, `Overtime`, `Judge Code`, `Judge`.

`Seconds` is derived from `Time`. `Overtime` is `X` when `Seconds` exceeds the event's time limit plus a 30-second grace period; events with an unknown limit are never flagged.

## Ballot status dataset

Columns, in order: `Slot`, `Title`, `Section`, `Rm`, `Judge`, `Status`. One row per table row, for every round or final that has a table. `Slot` is Speechwire's slot ID, and `Title` is any short text found outside the table on that page.

The `/balloting` page shows one separate table per slot, in slot ID order. A `Status` cell is dark green with white text when it is `IN`, dark gray with white text when it is `NOT STARTED`, and bright green (`#00ff00`) with black text for anything else.

A slot that has had a table and then returns none is treated as a failed fetch, so the previous data stays on screen.

## Notes on Speechwire

Observed behavior the code depends on:

- Manager pages live under `https://manage.speechwire.com/tabroom/`. Login is a POST to `login.php?tournid=<id>`.
- Performance times are at `comps-perftimes.php`, selected by round and grouping ID.
- Grouping (event) IDs change from tournament to tournament, so the scraper probes IDs 1 to 29.
- Rounds are `1`, `2`, `3`, and `F`.
- The tournament picker reads the public calendar at `postings.speechwire.com/p-calendar.php` and lists tournaments dated today.
- Ballot status tables are at `ballots-byslot.php?selslotid=<id>&sortmode=status`, one page per round, with the table at `/html/body/table` and the columns Section, Rm, Judge, Status. Slot IDs are small integers (under 30, as far as observed) that do not follow the round order, so the scraper probes 1 to 29.

## Setup and running

Requires Python 3.11 or newer.

```
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -e .
```

Copy your existing `standardization.py` (the file containing the `Standardizer` class) to `src/speechwire_live/cleaning/standardization.py`.

Start the app:

```
speechwire-live
```

It opens in your browser at `http://127.0.0.1:8080` and walks you through two steps:

1. **Select a tournament** from the list of tournaments dated today.
2. **Log in** by typing your Speechwire username and password. They are sent to Speechwire and kept in memory only.

A landing page then appears with a button for each view, and polling starts. The navigation bar on every page links between views. **Switch tournament**, also in the navigation bar, saves the current data to `.xlsx` and returns to step 1.

Settings are optional. To change defaults, or to skip a step by presetting the tournament or login, copy `config.example.toml` to `config.toml` (git-ignored). If `tournament_id` is set the picker is skipped; if `username` and `password` are set the login form is skipped.

The dashboard has no login of its own, and the login form sends your credentials over plain HTTP. Keep `host = "127.0.0.1"` unless you are on a network you trust. Anyone who can open the dashboard can also switch tournaments.

The latest data is saved as `{tournament_name} {HH-MM} Times.xlsx` in the working directory when you press Save .xlsx and when the app shuts down (Ctrl+C in the console).

## Tests

```
python -m unittest discover -s tests
```

The tests need `standardization.py` in place because the cleaning module imports it.
