from __future__ import annotations

import os

from ._http import HttpClient
from .resources import Emails, Domains, ApiKeys, Templates, Contacts, Inboxes, Webhooks, Campaigns, Sequences, Topics, Stats


class Pigeons:
    def __init__(self, *, base_url: str | None = None, api_key: str | None = None) -> None:
        resolved_url = base_url or os.environ.get("PIGEONS_URL")
        resolved_key = api_key or os.environ.get("PIGEONS_API_KEY")

        if not resolved_url:
            raise ValueError(
                "Pigeons base_url is required. Pass it in the constructor or set PIGEONS_URL environment variable."
            )
        if not resolved_key:
            raise ValueError(
                "Pigeons api_key is required. Pass it in the constructor or set PIGEONS_API_KEY environment variable."
            )

        self._http = HttpClient(resolved_url.rstrip("/"), resolved_key)

        self.emails = Emails(self._http)
        self.domains = Domains(self._http)
        self.api_keys = ApiKeys(self._http)
        self.templates = Templates(self._http)
        self.contacts = Contacts(self._http)
        self.inboxes = Inboxes(self._http)
        self.webhooks = Webhooks(self._http)
        self.campaigns = Campaigns(self._http)
        self.sequences = Sequences(self._http)
        self.topics = Topics(self._http)
        self.stats = Stats(self._http)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Pigeons:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
