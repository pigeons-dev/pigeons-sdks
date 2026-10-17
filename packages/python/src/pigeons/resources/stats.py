from __future__ import annotations

from .._http import HttpClient
from .._types import GlobalStats


class Stats:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self) -> GlobalStats:
        return self._http.get("/v1/stats")
