from __future__ import annotations


class PigeonsError(Exception):
    def __init__(self, type: str, message: str, code: str, status_code: int) -> None:
        super().__init__(message)
        self.type = type
        self.code = code
        self.status_code = status_code


class ValidationError(PigeonsError):
    def __init__(self, message: str, code: str = "validation_error") -> None:
        super().__init__("validation_error", message, code, 400)


class AuthError(PigeonsError):
    def __init__(self, message: str = "Invalid or missing API key") -> None:
        super().__init__("authentication_error", message, "unauthorized", 401)


class NotFoundError(PigeonsError):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__("not_found", message, "not_found", 404)


class RateLimitError(PigeonsError):
    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__("rate_limit_error", message, "rate_limited", 429)
