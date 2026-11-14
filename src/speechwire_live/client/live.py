from collections.abc import Mapping

import requests

BASE_URL = "https://manage.speechwire.com/tabroom/"
REQUEST_TIMEOUT_SECONDS = 30


class LiveClient:
    def __init__(self, username: str, password: str, tournament_id: str):
        self._session = requests.Session()
        self._session.post(
            f"{BASE_URL}login.php?tournid={tournament_id}",
            data={
                "username": username,
                "password": password,
                "tournid": tournament_id,
                "Submit": "Log in",
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

    def get_html(self, page: str, params: Mapping[str, str] | None = None) -> str:
        response = self._session.get(
            f"{BASE_URL}{page}", params=params, timeout=REQUEST_TIMEOUT_SECONDS
        )
        return response.text
