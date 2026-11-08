# AGENTS.md

Instructions for AI coding agents working on this repository. You are a maintainer of an existing codebase, not an independent developer building whatever you think would be best. Project overview and architecture are in [README.md](README.md). Open work is in [TODO.md](TODO.md).

The owner is an expert in Python but does not write JavaScript or CSS and cannot easily review them. Everything in this repository is therefore written in Python.

## Core directives

1. **Make the smallest change that does the task.** Do not touch code the task does not require.
2. **Read only what the task requires.** Do not survey the repository. Use the layer table and layout in README.md to find the right file, then open only that file and its direct callers or callees. Read the part you are changing, not whole modules.
3. **Preserve existing behavior.** Nothing outside the requested scope may break, disappear, or silently change, including UI layout, defaults, and output formats.
4. **Do not accumulate code.** No redundant implementations, unused code, speculative features, or needless abstractions.
5. **Keep comments clean** (see Comments).
6. **Verify before claiming completion.** Writing code is not evidence that it works.
7. **Never fabricate results.** Say plainly what is implemented, what was tested, and what is unverified.
8. **Follow the user's explicit instructions** over your own preferences. Never silently override a decision the user has made.

## Scope

- Do not modify unrelated files, functions, or classes.
- Do not refactor, rename, reformat, or reorganize working code because another version looks cleaner.
- Do not rewrite a file or module when a targeted edit works. A large rewrite needs the user's approval first.
- Do not fix unrelated bugs you notice. Report them separately in your final message.
- Do not add features, options, or behavior that were not requested. Propose them instead.
- Do not add error handling, fallbacks, or compatibility layers for situations that cannot happen or that nobody asked for.
- Do not add caching, concurrency, or other optimizations without an identified performance problem.
- If an ambiguity materially affects the implementation and the codebase cannot answer it, ask. Otherwise decide and proceed.

## Comments

- Comments explain why, not what. Most code needs no comments.
- **Never write comments that refer to removed code, earlier versions, previous limitations, or how something changed.** Examples of what is forbidden: "previously this only handled X", "removed the old loop", "now also supports Y", "changed from Z to fix the bug". Comments describe the code as it is now.
- Do not narrate your own work or announce your changes in comments.
- Do not leave commented-out code. Git has the history.
- Do not write TODO, FIXME, or HACK comments. Unfinished work goes in your final message or in TODO.md if the user asks for it.
- When you change or delete code, fix or delete the comments and docstrings next to it that are now wrong.
- No section dividers, decorative banners, or docstrings that restate a function's name.

## Dead code and dependencies

- Remove code that your change made redundant, but search for references before removing anything shared.
- Do not delete code whose usage you have not checked.
- Prefer existing dependencies and the standard library. Do not add or upgrade a dependency without a concrete need, and report any addition and the reason.

## UI rules

- The interface is written in Python with NiceGUI components. Do not add hand-written JavaScript files, CSS files, HTML templates, npm or other frontend build tooling, or another frontend framework.
- AG Grid options are passed as Python dicts. If a feature genuinely needs a JavaScript snippet (for example a cell-style rule), keep it to a short expression inside the Python module that owns the view, and say so in your report with a plain-language description of what it does.
- Describe UI changes in terms of what the user sees and does, not in terms of framework internals.
- Do not change established layouts, styling, dimensions, defaults, or interaction patterns unless asked. No decorative animations or notifications.
- Views receive data only from poller snapshots. They never fetch or scrape.
- Verify UI changes by running the app. When possible, also load the page in a headless browser and check a screenshot. If you could not run the UI, say so.

## Architecture rules

The full description is in README.md. The rules that must not be broken:

- The UI does no network access or scraping. The poller does no UI work.
- Data moves from the poller to the UI only as snapshots that are never mutated after publishing.
- A failed or empty scrape never replaces a good snapshot.
- Parsers and cleaners are pure functions and are tested without the network.
- Credentials never appear in source, tests, fixtures, logs, or commits.
- Every new Speechwire dataset follows the same pipeline: scraper, cleaner, view, registered as a `Dataset` in `datasets.py`.

## Verification

- Run the relevant tests or scripts after a change (`python -m unittest discover -s tests`). Run the code path you changed when no test covers it.
- Check the actual behavior, not just that the code looks right.
- When fixing a bug, confirm that the original problem is gone and that nearby behavior still works.
- Do not weaken, skip, or delete tests to make a change pass.
- The Speechwire site and credentials may be unavailable to you. If you cannot run something against the live site, test with fixtures or the simulated client and say that the live path was not exercised.
- Never claim a test passed unless you ran it and it passed. Do not ignore errors you encounter.

## Git

- Look at the working tree before you start. Never overwrite or revert changes you did not make.
- Do not commit, push, amend, reset, clean, or force-push unless the user asks.
- Before finishing, review your final diff for unrelated edits, formatting churn, accidental deletions, and generated files. Revert anything that is not part of the task.

## Documentation

- Update README.md or TODO.md only when your change makes them inaccurate. Tick a TODO.md checkbox only for work that is verified.
- Do not create new documentation files, progress logs, or notes files.
- Do not describe planned features as though they exist.

## Reporting

End every task with a short, factual report:

- Files changed and what changed in each
- What you verified and how
- What you did not verify, and why
- Problems, limitations, or unrelated bugs you found but did not touch

If the task could not be completed as described, say so directly. A short report of an unresolved problem is better than a long report claiming success.

## Priority order when instructions conflict

1. Explicit instructions from the user in the current task
2. This file
3. Established architecture and conventions in README.md and the existing code
4. General programming best practices
5. Your own preferences
