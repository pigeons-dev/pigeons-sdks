from __future__ import annotations

from urllib.parse import urlencode

from .._http import HttpClient
from .._types import (
    Inbox,
    CreateInboxParams,
    UpdateInboxParams,
    ListInboxesParams,
    InboxMessage,
    SendInboxMessageParams,
    ListInboxMessagesParams,
    Thread,
    UpdateThreadParams,
    ListThreadsParams,
    PaginatedResponse,
)


class InboxMessages:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, inbox_id: str, params: ListInboxMessagesParams | None = None) -> PaginatedResponse[InboxMessage]:
        qs: dict[str, str] = {}
        if params:
            if "cursor" in params:
                qs["cursor"] = params["cursor"]
            if "limit" in params:
                qs["limit"] = str(params["limit"])
            if "direction" in params:
                qs["direction"] = params["direction"]
            if "threadId" in params:
                qs["threadId"] = params["threadId"]
            if "labels" in params:
                qs["labels"] = ",".join(params["labels"])
        path = f"/v1/inboxes/{inbox_id}/messages"
        if qs:
            path += f"?{urlencode(qs)}"
        return self._http.get(path)

    def get(self, inbox_id: str, message_id: str) -> InboxMessage:
        return self._http.get(f"/v1/inboxes/{inbox_id}/messages/{message_id}")

    def create(self, inbox_id: str, params: SendInboxMessageParams) -> InboxMessage:
        return self._http.post(f"/v1/inboxes/{inbox_id}/messages", json=dict(params))


class InboxThreads:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, inbox_id: str, params: ListThreadsParams | None = None) -> PaginatedResponse[Thread]:
        qs: dict[str, str] = {}
        if params:
            if "cursor" in params:
                qs["cursor"] = params["cursor"]
            if "limit" in params:
                qs["limit"] = str(params["limit"])
            if "status" in params:
                qs["status"] = params["status"]
        path = f"/v1/inboxes/{inbox_id}/threads"
        if qs:
            path += f"?{urlencode(qs)}"
        return self._http.get(path)

    def get(self, inbox_id: str, thread_id: str) -> Thread:
        return self._http.get(f"/v1/inboxes/{inbox_id}/threads/{thread_id}")

    def update(self, inbox_id: str, thread_id: str, params: UpdateThreadParams) -> Thread:
        return self._http.patch(f"/v1/inboxes/{inbox_id}/threads/{thread_id}", json=dict(params))


class Inboxes:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self.messages = InboxMessages(http)
        self.threads = InboxThreads(http)

    def create(self, params: CreateInboxParams) -> Inbox:
        return self._http.post("/v1/inboxes", json=dict(params))

    def list(self, params: ListInboxesParams | None = None) -> PaginatedResponse[Inbox]:
        qs: dict[str, str] = {}
        if params:
            if "cursor" in params:
                qs["cursor"] = params["cursor"]
            if "limit" in params:
                qs["limit"] = str(params["limit"])
            if "status" in params:
                qs["status"] = params["status"]
            if "labels" in params:
                qs["labels"] = ",".join(params["labels"])
        path = f"/v1/inboxes?{urlencode(qs)}" if qs else "/v1/inboxes"
        return self._http.get(path)

    def get(self, id: str) -> Inbox:
        return self._http.get(f"/v1/inboxes/{id}")

    def update(self, id: str, params: UpdateInboxParams) -> Inbox:
        return self._http.patch(f"/v1/inboxes/{id}", json=dict(params))

    def delete(self, id: str) -> dict:
        return self._http.delete(f"/v1/inboxes/{id}")

    def pause(self, id: str) -> Inbox:
        return self._http.post(f"/v1/inboxes/{id}/pause", json={})

    def resume(self, id: str) -> Inbox:
        return self._http.post(f"/v1/inboxes/{id}/resume", json={})

    def set_catch_all(self, id: str) -> Inbox:
        return self._http.post(f"/v1/inboxes/{id}/catch-all", json={})
