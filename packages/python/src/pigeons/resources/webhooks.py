from __future__ import annotations

from urllib.parse import urlencode

from .._http import HttpClient
from .._types import Webhook, CreateWebhookParams, UpdateWebhookParams, ListWebhooksParams, PaginatedResponse


class Webhooks:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, params: CreateWebhookParams) -> Webhook:
        return self._http.post("/v1/webhooks", json=dict(params))

    def list(self, params: ListWebhooksParams | None = None) -> PaginatedResponse[Webhook]:
        qs: dict[str, str] = {}
        if params:
            if "cursor" in params:
                qs["cursor"] = params["cursor"]
            if "limit" in params:
                qs["limit"] = str(params["limit"])
        path = f"/v1/webhooks?{urlencode(qs)}" if qs else "/v1/webhooks"
        return self._http.get(path)

    def get(self, id: str) -> Webhook:
        return self._http.get(f"/v1/webhooks/{id}")

    def update(self, id: str, params: UpdateWebhookParams) -> Webhook:
        return self._http.patch(f"/v1/webhooks/{id}", json=dict(params))

    def delete(self, id: str) -> dict:
        return self._http.delete(f"/v1/webhooks/{id}")
