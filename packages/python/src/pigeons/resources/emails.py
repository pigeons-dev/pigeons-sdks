from __future__ import annotations

from urllib.parse import urlencode

from .._http import HttpClient
from .._types import Email, SendEmailParams, ListEmailsParams, PaginatedResponse


class Emails:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def send(self, params: SendEmailParams, *, idempotency_key: str | None = None) -> Email:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return self._http.post("/v1/emails", json=dict(params), headers=headers or None)

    def get(self, id: str) -> Email:
        return self._http.get(f"/v1/emails/{id}")

    def list(self, params: ListEmailsParams | None = None) -> PaginatedResponse[Email]:
        qs: dict[str, str] = {}
        if params:
            if "cursor" in params:
                qs["cursor"] = params["cursor"]
            if "limit" in params:
                qs["limit"] = str(params["limit"])
            if "status" in params:
                qs["status"] = params["status"]
        path = f"/v1/emails?{urlencode(qs)}" if qs else "/v1/emails"
        return self._http.get(path)

    def cancel(self, id: str) -> Email:
        return self._http.post(f"/v1/emails/{id}/cancel", json={})

    def batch(self, emails: list[SendEmailParams]) -> list[Email]:
        return self._http.post("/v1/emails/batch", json=[dict(e) for e in emails])
