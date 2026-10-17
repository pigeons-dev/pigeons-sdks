from __future__ import annotations

from urllib.parse import urlencode

from .._http import HttpClient
from .._types import Campaign, CreateCampaignParams, UpdateCampaignParams, ListCampaignsParams, PaginatedResponse


class Campaigns:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, params: CreateCampaignParams) -> Campaign:
        return self._http.post("/v1/campaigns", json=dict(params))

    def get(self, id: str) -> Campaign:
        return self._http.get(f"/v1/campaigns/{id}")

    def list(self, params: ListCampaignsParams | None = None) -> PaginatedResponse[Campaign]:
        qs: dict[str, str] = {}
        if params:
            if "cursor" in params:
                qs["cursor"] = params["cursor"]
            if "limit" in params:
                qs["limit"] = str(params["limit"])
            if "status" in params:
                qs["status"] = params["status"]
        path = f"/v1/campaigns?{urlencode(qs)}" if qs else "/v1/campaigns"
        return self._http.get(path)

    def update(self, id: str, params: UpdateCampaignParams) -> Campaign:
        return self._http.patch(f"/v1/campaigns/{id}", json=dict(params))

    def send(self, id: str, *, scheduled_at: str | None = None) -> Campaign:
        body = {"scheduledAt": scheduled_at} if scheduled_at else {}
        return self._http.post(f"/v1/campaigns/{id}/send", json=body)

    def cancel(self, id: str) -> Campaign:
        return self._http.post(f"/v1/campaigns/{id}/cancel", json={})

    def pause(self, id: str) -> Campaign:
        return self._http.post(f"/v1/campaigns/{id}/pause", json={})

    def resume(self, id: str) -> Campaign:
        return self._http.post(f"/v1/campaigns/{id}/resume", json={})
