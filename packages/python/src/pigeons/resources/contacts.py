from __future__ import annotations

from urllib.parse import quote, urlencode

from .._http import HttpClient
from .._types import Contact, CreateContactParams, UpdateContactParams, BatchCreateContactsResult, ListContactsParams, PaginatedResponse


class Contacts:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, params: CreateContactParams) -> Contact:
        return self._http.post("/v1/contacts", json=dict(params))

    def get(self, id_or_email: str) -> Contact:
        return self._http.get(f"/v1/contacts/{quote(id_or_email, safe='')}")

    def list(self, params: ListContactsParams | None = None) -> PaginatedResponse[Contact]:
        qs: dict[str, str] = {}
        if params:
            if "cursor" in params:
                qs["cursor"] = params["cursor"]
            if "limit" in params:
                qs["limit"] = str(params["limit"])
            if "tag" in params:
                qs["tag"] = params["tag"]
        path = f"/v1/contacts?{urlencode(qs)}" if qs else "/v1/contacts"
        return self._http.get(path)

    def update(self, id_or_email: str, params: UpdateContactParams) -> Contact:
        return self._http.patch(f"/v1/contacts/{quote(id_or_email, safe='')}", json=dict(params))

    def delete(self, id_or_email: str) -> dict:
        return self._http.delete(f"/v1/contacts/{quote(id_or_email, safe='')}")

    def batch(self, contacts: list[CreateContactParams]) -> BatchCreateContactsResult:
        return self._http.post("/v1/contacts/batch", json=[dict(c) for c in contacts])

    def unsubscribe(self, id_or_email: str) -> Contact:
        return self._http.post(f"/v1/contacts/{quote(id_or_email, safe='')}/unsubscribe", json={})

    def resubscribe(self, id_or_email: str) -> Contact:
        return self._http.post(f"/v1/contacts/{quote(id_or_email, safe='')}/resubscribe", json={})
