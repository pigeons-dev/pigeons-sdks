from __future__ import annotations

from .._http import HttpClient
from .._types import Domain, AddDomainParams, DomainStats


class Domains:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def add(self, params: AddDomainParams) -> Domain:
        return self._http.post("/v1/domains", json=dict(params))

    def list(self) -> dict:
        return self._http.get("/v1/domains")

    def verify(self, id: str) -> Domain:
        return self._http.get(f"/v1/domains/{id}/verify")

    def stats(self, id: str) -> DomainStats:
        return self._http.get(f"/v1/domains/{id}/stats")

    def delete(self, id: str) -> dict:
        return self._http.delete(f"/v1/domains/{id}")
