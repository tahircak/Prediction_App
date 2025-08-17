import os
from typing import Optional

import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


class ApiClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token: Optional[str] = None

    def set_token(self, token: Optional[str]):
        self.token = token

    def _headers(self):
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def register(self, email: str, password: str):
        r = requests.post(
            f"{self.base_url}/auth/register",
            json={"email": email, "password": password},
            headers=self._headers(),
            timeout=15,
        )
        r.raise_for_status()
        return r.json()

    def login(self, email: str, password: str) -> str:
        r = requests.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password},
            headers=self._headers(),
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        return data["access_token"]

    def list_matches(self):
        r = requests.get(f"{self.base_url}/matches", headers=self._headers(), timeout=15)
        r.raise_for_status()
        return r.json()
