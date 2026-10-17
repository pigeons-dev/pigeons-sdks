from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from .._http import HttpClient
from .._types import Template, CreateTemplateParams, UpdateTemplateParams, TemplatePreview, PaginatedResponse


class Templates:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, params: CreateTemplateParams) -> Template:
        return self._http.post("/v1/templates", json=dict(params))

    def get(self, id_or_slug: str) -> Template:
        return self._http.get(f"/v1/templates/{id_or_slug}")

    def list(self, *, cursor: str | None = None, limit: int | None = None) -> PaginatedResponse[Template]:
        qs: dict[str, str] = {}
        if cursor:
            qs["cursor"] = cursor
        if limit is not None:
            qs["limit"] = str(limit)
        path = f"/v1/templates?{urlencode(qs)}" if qs else "/v1/templates"
        return self._http.get(path)

    def update(self, id_or_slug: str, params: UpdateTemplateParams) -> Template:
        return self._http.patch(f"/v1/templates/{id_or_slug}", json=dict(params))

    def delete(self, id_or_slug: str) -> dict:
        return self._http.delete(f"/v1/templates/{id_or_slug}")

    def preview(self, id_or_slug: str, data: dict[str, Any] | None = None) -> TemplatePreview:
        return self._http.post(f"/v1/templates/{id_or_slug}/preview", json={"data": data})
