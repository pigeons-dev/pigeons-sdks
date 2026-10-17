from __future__ import annotations

from urllib.parse import urlencode

from .._http import HttpClient
from .._types import (
    Sequence,
    CreateSequenceParams,
    UpdateSequenceParams,
    ListSequencesParams,
    SequenceEnrollment,
    PaginatedResponse,
)


class Sequences:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, params: CreateSequenceParams) -> Sequence:
        return self._http.post("/v1/sequences", json=dict(params))

    def get(self, id: str) -> Sequence:
        return self._http.get(f"/v1/sequences/{id}")

    def list(self, params: ListSequencesParams | None = None) -> PaginatedResponse[Sequence]:
        qs: dict[str, str] = {}
        if params:
            if "cursor" in params:
                qs["cursor"] = params["cursor"]
            if "limit" in params:
                qs["limit"] = str(params["limit"])
            if "status" in params:
                qs["status"] = params["status"]
        path = f"/v1/sequences?{urlencode(qs)}" if qs else "/v1/sequences"
        return self._http.get(path)

    def update(self, id: str, params: UpdateSequenceParams) -> Sequence:
        return self._http.patch(f"/v1/sequences/{id}", json=dict(params))

    def activate(self, id: str) -> Sequence:
        return self._http.post(f"/v1/sequences/{id}/activate", json={})

    def pause(self, id: str) -> Sequence:
        return self._http.post(f"/v1/sequences/{id}/pause", json={})

    def enroll(self, id: str, contact_id: str) -> SequenceEnrollment:
        return self._http.post(f"/v1/sequences/{id}/enroll", json={"contactId": contact_id})

    def enrollments(
        self,
        id: str,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        status: str | None = None,
    ) -> PaginatedResponse[SequenceEnrollment]:
        qs: dict[str, str] = {}
        if cursor:
            qs["cursor"] = cursor
        if limit is not None:
            qs["limit"] = str(limit)
        if status:
            qs["status"] = status
        path = f"/v1/sequences/{id}/enrollments"
        if qs:
            path += f"?{urlencode(qs)}"
        return self._http.get(path)
