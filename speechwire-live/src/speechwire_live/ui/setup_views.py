from nicegui import run, ui

from ..client.tournament_lookup import list_todays_tournaments
from ..session import Session


async def build_tournament_picker(session: Session) -> None:
    with ui.card().classes("w-full max-w-xl mx-auto mt-8 gap-3"):
        ui.label("Select a tournament").classes("text-xl font-medium")
        listing = ui.column().classes("w-full gap-2")

        async def load():
            listing.clear()
            with listing:
                ui.spinner()
            try:
                tournaments = await run.io_bound(list_todays_tournaments, session.config.season_id)
            except Exception as error:
                listing.clear()
                with listing:
                    ui.label(f"Could not load the tournament calendar: {error}").classes("text-negative")
                return
            listing.clear()
            with listing:
                if not tournaments:
                    ui.label("No tournaments are listed for today.")
                    ui.label("Set tournament_id in config.toml to skip this step.").classes(
                        "text-sm text-slate-500"
                    )
                for tournament in tournaments:
                    button = ui.button(on_click=lambda t=tournament: session.choose_tournament(t))
                    button.props("outline no-caps align=left").classes("w-full")
                    with button:
                        with ui.column().classes("items-start gap-0"):
                            ui.label(tournament.name).classes("font-medium")
                            if tournament.location:
                                ui.label(tournament.location).classes("text-xs text-slate-500")

        ui.button("Refresh list", on_click=load).props("flat")
        await load()


def build_login_form(session: Session) -> None:
    with ui.card().classes("w-full max-w-md mx-auto mt-8 gap-3"):
        ui.label("Log in to Speechwire").classes("text-xl font-medium")
        ui.label(session.tournament.name).classes("text-slate-500")
        username = ui.input("Username").props("outlined").classes("w-full")
        password = ui.input("Password", password=True, password_toggle_button=True)
        password.props("outlined").classes("w-full")
        ui.label("Your login is sent to Speechwire and kept in memory only.").classes(
            "text-xs text-slate-500"
        )

        def submit():
            if not username.value or not password.value:
                ui.notify("Enter both a username and a password.", type="warning")
                return
            session.log_in(username.value, password.value)

        password.on("keydown.enter", submit)
        with ui.row():
            ui.button("Log in", on_click=submit)
            ui.button("Back", on_click=session.clear_tournament).props("flat")
