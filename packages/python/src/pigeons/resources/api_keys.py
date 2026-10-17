from __future__ import annotations

from .._http import HttpClient
from .._types import ApiKey, CreateApiKeyParams


class ApiKeys:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, params: CreateApiKeyParams) -> ApiKey:
        return self._http.post("/v1/api-keys", json=dict(params))

    def list(self) -> dict:
        return self._http.get("/v1/api-keys")

    def revoke(self, id: str) -> dict:
        return self._http.delete(f"/v1/api-keys/{id}")
