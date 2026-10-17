from __future__ import annotations

from urllib.parse import urlencode

from .._http import HttpClient
from .._types import SubscriptionTopic, CreateTopicParams, UpdateTopicParams, ListTopicsParams, PaginatedResponse


class Topics:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, params: CreateTopicParams) -> SubscriptionTopic:
        return self._http.post("/v1/topics", json=dict(params))

    def get(self, id: str) -> SubscriptionTopic:
        return self._http.get(f"/v1/topics/{id}")

    def list(self, params: ListTopicsParams | None = None) -> PaginatedResponse[SubscriptionTopic]:
        qs: dict[str, str] = {}
        if params:
            if "cursor" in params:
                qs["cursor"] = params["cursor"]
            if "limit" in params:
                qs["limit"] = str(params["limit"])
        path = f"/v1/topics?{urlencode(qs)}" if qs else "/v1/topics"
        return self._http.get(path)

    def update(self, id: str, params: UpdateTopicParams) -> SubscriptionTopic:
        return self._http.patch(f"/v1/topics/{id}", json=dict(params))

    def delete(self, id: str) -> None:
        self._http.delete(f"/v1/topics/{id}")
