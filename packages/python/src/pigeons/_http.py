from __future__ import annotations

from typing import Any

import httpx

from ._errors import PigeonsError, ValidationError, AuthError, NotFoundError, RateLimitError


class HttpClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            headers={"Content-Type": "application/json", "x-api-key": api_key},
            timeout=30.0,
        )

    def request(self, method: str, path: str, *, json: Any = None, headers: dict[str, str] | None = None) -> Any:
        response = self._client.request(method, path, json=json, headers=headers)
        data = response.json() if response.content else None

        if not response.is_success:
            error = (data or {}).get("error", {})
            message = error.get("message", f"HTTP {response.status_code}")
            error_type = error.get("type", "unknown_error")
            code = error.get("code", "unknown")

            match response.status_code:
                case 400:
                    raise ValidationError(message, code)
                case 401:
                    raise AuthError(message)
                case 404:
                    raise NotFoundError(message)
                case 429:
                    raise RateLimitError(message)
                case _:
                    raise PigeonsError(error_type, message, code, response.status_code)

        return data

    def get(self, path: str) -> Any:
        return self.request("GET", path)

    def post(self, path: str, json: Any = None, headers: dict[str, str] | None = None) -> Any:
        return self.request("POST", path, json=json, headers=headers)

    def patch(self, path: str, json: Any) -> Any:
        return self.request("PATCH", path, json=json)

    def delete(self, path: str) -> Any:
        return self.request("DELETE", path)

    def close(self) -> None:
        self._client.close()
