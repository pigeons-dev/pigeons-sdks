import os

import httpx
import pytest
from pytest_httpx import HTTPXMock

from pigeons import (
    Pigeons,
    PigeonsError,
    ValidationError,
    AuthError,
    NotFoundError,
    RateLimitError,
)


class TestConstructor:
    def test_raises_when_base_url_missing(self):
        os.environ.pop("PIGEONS_URL", None)
        with pytest.raises(ValueError, match="base_url is required"):
            Pigeons(api_key="pgn_test")

    def test_raises_when_api_key_missing(self):
        os.environ.pop("PIGEONS_API_KEY", None)
        with pytest.raises(ValueError, match="api_key is required"):
            Pigeons(base_url="http://localhost:3891")

    def test_creates_instance_with_explicit_config(self):
        p = Pigeons(base_url="http://localhost:3891", api_key="pgn_test")
        assert p.emails is not None
        assert p.domains is not None
        assert p.api_keys is not None
        assert p.templates is not None
        assert p.contacts is not None
        assert p.inboxes is not None
        assert p.webhooks is not None
        assert p.campaigns is not None
        assert p.sequences is not None
        assert p.topics is not None
        assert p.stats is not None
        p.close()

    def test_reads_from_env_vars(self):
        os.environ["PIGEONS_URL"] = "http://localhost:3891"
        os.environ["PIGEONS_API_KEY"] = "pgn_test"
        try:
            p = Pigeons()
            assert p.emails is not None
            p.close()
        finally:
            del os.environ["PIGEONS_URL"]
            del os.environ["PIGEONS_API_KEY"]

    def test_strips_trailing_slashes(self):
        p = Pigeons(base_url="http://localhost:3891///", api_key="pgn_test")
        assert p.emails is not None
        p.close()

    def test_context_manager(self):
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            assert p.emails is not None


class TestErrors:
    def test_validation_error(self):
        err = ValidationError("bad input", "invalid_field")
        assert isinstance(err, PigeonsError)
        assert err.type == "validation_error"
        assert err.status_code == 400
        assert err.code == "invalid_field"
        assert str(err) == "bad input"

    def test_auth_error(self):
        err = AuthError()
        assert isinstance(err, PigeonsError)
        assert err.status_code == 401
        assert err.code == "unauthorized"

    def test_not_found_error(self):
        err = NotFoundError()
        assert isinstance(err, PigeonsError)
        assert err.status_code == 404

    def test_rate_limit_error(self):
        err = RateLimitError()
        assert isinstance(err, PigeonsError)
        assert err.status_code == 429


class TestEmails:
    def test_send(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails",
            method="POST",
            json={"id": "msg_123", "to": ["a@b.com"], "subject": "Hi", "status": "queued", "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            email = p.emails.send({"to": "a@b.com", "subject": "Hi", "html": "<p>Hello</p>"})
            assert email["id"] == "msg_123"
            assert email["status"] == "queued"

    def test_send_with_idempotency_key(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails",
            method="POST",
            json={"id": "msg_123", "to": ["a@b.com"], "subject": "Hi", "status": "queued", "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            email = p.emails.send({"to": "a@b.com", "subject": "Hi"}, idempotency_key="idem-1")
            assert email["id"] == "msg_123"
            request = httpx_mock.get_request()
            assert request.headers["idempotency-key"] == "idem-1"

    def test_get(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails/msg_123",
            json={"id": "msg_123", "to": ["a@b.com"], "subject": "Hi", "status": "sent", "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            email = p.emails.get("msg_123")
            assert email["id"] == "msg_123"

    def test_list(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails?status=sent&limit=10",
            json={"data": [], "has_more": False, "next_cursor": None},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            result = p.emails.list({"status": "sent", "limit": 10})
            assert result["data"] == []
            assert result["has_more"] is False

    def test_cancel(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails/msg_123/cancel",
            method="POST",
            json={"id": "msg_123", "to": ["a@b.com"], "subject": "Hi", "status": "failed", "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            email = p.emails.cancel("msg_123")
            assert email["status"] == "failed"

    def test_batch(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails/batch",
            method="POST",
            json=[{"id": "msg_1", "to": ["a@b.com"], "subject": "A", "status": "queued", "createdAt": "2024-01-01", "updatedAt": "2024-01-01"}],
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            emails = p.emails.batch([{"to": "a@b.com", "subject": "A"}])
            assert len(emails) == 1


class TestDomains:
    def test_add(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/domains",
            method="POST",
            json={"id": "dom_1", "domain": "example.com", "verificationStatus": "pending", "spfVerified": False, "dmarcVerified": False, "region": "us-east-1", "capabilities": {"sending": True, "receiving": False}, "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            domain = p.domains.add({"domain": "example.com"})
            assert domain["id"] == "dom_1"

    def test_verify(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/domains/dom_1/verify",
            json={"id": "dom_1", "domain": "example.com", "verificationStatus": "verified", "spfVerified": True, "dmarcVerified": True, "region": "us-east-1", "capabilities": {"sending": True, "receiving": False}, "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            domain = p.domains.verify("dom_1")
            assert domain["verificationStatus"] == "verified"

    def test_stats(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/domains/dom_1/stats",
            json={"domainId": "dom_1", "domain": "example.com", "last24h": {"sent": 10, "delivered": 9, "opened": 3, "bounced": 1, "complained": 0, "failed": 0, "deliveryRate": 0.9, "bounceRate": 0.1, "complaintRate": 0.0, "openRate": 0.3}, "last7d": {"sent": 0, "delivered": 0, "opened": 0, "bounced": 0, "complained": 0, "failed": 0, "deliveryRate": 0, "bounceRate": 0, "complaintRate": 0, "openRate": 0}, "last30d": {"sent": 0, "delivered": 0, "opened": 0, "bounced": 0, "complained": 0, "failed": 0, "deliveryRate": 0, "bounceRate": 0, "complaintRate": 0, "openRate": 0}, "warmup": {"phase": "new", "dailyLimit": 50, "recommendation": "Start slow"}},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            stats = p.domains.stats("dom_1")
            assert stats["warmup"]["phase"] == "new"

    def test_delete(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/domains/dom_1",
            method="DELETE",
            json={"id": "dom_1", "deleted": True},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            result = p.domains.delete("dom_1")
            assert result["deleted"] is True


class TestApiKeys:
    def test_create(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/api-keys",
            method="POST",
            json={"id": "key_1", "name": "test", "prefix": "pgn_abc", "key": "pgn_abc123full", "createdAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            key = p.api_keys.create({"name": "test"})
            assert key["key"] == "pgn_abc123full"

    def test_revoke(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/api-keys/key_1",
            method="DELETE",
            json={"id": "key_1", "deleted": True},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            result = p.api_keys.revoke("key_1")
            assert result["deleted"] is True


class TestContacts:
    def test_create(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/contacts",
            method="POST",
            json={"id": "ctc_1", "email": "a@b.com", "unsubscribed": False, "bounced": False, "complained": False, "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            contact = p.contacts.create({"email": "a@b.com"})
            assert contact["email"] == "a@b.com"

    def test_get_by_email(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/contacts/a%40b.com",
            json={"id": "ctc_1", "email": "a@b.com", "unsubscribed": False, "bounced": False, "complained": False, "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            contact = p.contacts.get("a@b.com")
            assert contact["id"] == "ctc_1"

    def test_unsubscribe(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/contacts/ctc_1/unsubscribe",
            method="POST",
            json={"id": "ctc_1", "email": "a@b.com", "unsubscribed": True, "bounced": False, "complained": False, "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            contact = p.contacts.unsubscribe("ctc_1")
            assert contact["unsubscribed"] is True


class TestTemplates:
    def test_create(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/templates",
            method="POST",
            json={"id": "tpl_1", "slug": "welcome", "name": "Welcome", "subject": "Hi", "body": "<p>Hi</p>", "version": 1, "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            tpl = p.templates.create({"slug": "welcome", "name": "Welcome", "subject": "Hi", "body": "<p>Hi</p>"})
            assert tpl["slug"] == "welcome"

    def test_preview(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/templates/welcome/preview",
            method="POST",
            json={"subject": "Hi John", "html": "<p>Hi John</p>", "text": "Hi John"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            preview = p.templates.preview("welcome", {"name": "John"})
            assert preview["subject"] == "Hi John"


class TestInboxes:
    def test_create(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/inboxes",
            method="POST",
            json={"id": "inb_1", "name": "Support", "emailAddress": "support@example.com", "autoReplyEnabled": False, "status": "active", "catchAll": False, "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            inbox = p.inboxes.create({"name": "Support"})
            assert inbox["name"] == "Support"

    def test_pause(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/inboxes/inb_1/pause",
            method="POST",
            json={"id": "inb_1", "name": "Support", "emailAddress": "support@example.com", "autoReplyEnabled": False, "status": "paused", "catchAll": False, "createdAt": "2024-01-01", "updatedAt": "2024-01-01"},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            inbox = p.inboxes.pause("inb_1")
            assert inbox["status"] == "paused"

    def test_messages_list(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/inboxes/inb_1/messages",
            json={"data": [], "has_more": False, "next_cursor": None},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            result = p.inboxes.messages.list("inb_1")
            assert result["data"] == []

    def test_threads_list(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/inboxes/inb_1/threads",
            json={"data": [], "has_more": False, "next_cursor": None},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            result = p.inboxes.threads.list("inb_1")
            assert result["data"] == []


class TestHttpErrors:
    def test_400_raises_validation_error(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails",
            method="POST",
            status_code=400,
            json={"error": {"type": "validation_error", "message": "Missing subject", "code": "missing_field"}},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            with pytest.raises(ValidationError, match="Missing subject") as exc_info:
                p.emails.send({"to": "a@b.com"})
            assert exc_info.value.code == "missing_field"

    def test_401_raises_auth_error(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails",
            status_code=401,
            json={"error": {"type": "authentication_error", "message": "Bad key"}},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_bad") as p:
            with pytest.raises(AuthError):
                p.emails.list()

    def test_404_raises_not_found_error(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails/msg_nope",
            status_code=404,
            json={"error": {"type": "not_found", "message": "Not found"}},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            with pytest.raises(NotFoundError):
                p.emails.get("msg_nope")

    def test_429_raises_rate_limit_error(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails",
            status_code=429,
            json={"error": {"type": "rate_limit_error", "message": "Slow down"}},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            with pytest.raises(RateLimitError):
                p.emails.list()

    def test_500_raises_pigeons_error(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails",
            status_code=500,
            json={"error": {"type": "internal_error", "message": "Server error", "code": "internal"}},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_test") as p:
            with pytest.raises(PigeonsError) as exc_info:
                p.emails.list()
            assert exc_info.value.status_code == 500


class TestAuthHeader:
    def test_sends_x_api_key_header(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:3891/v1/emails",
            json={"data": [], "has_more": False, "next_cursor": None},
        )
        with Pigeons(base_url="http://localhost:3891", api_key="pgn_secret") as p:
            p.emails.list()
            request = httpx_mock.get_request()
            assert request.headers["x-api-key"] == "pgn_secret"
