# Pigeons Python SDK

Python SDK for [Pigeons](https://pigeons.dev) — open-source, self-hosted email infrastructure for developers and AI agents.

## Install

```bash
pip install pigeons-py
```

## Usage

```python
from pigeons import Pigeons

p = Pigeons(base_url="http://localhost:3891", api_key="pgn_...")

email = p.emails.send({
    "to": "user@example.com",
    "subject": "Hello from Pigeons",
    "html": "<p>Welcome!</p>",
})

print(email["id"])  # msg_...
```

## Configuration

The SDK reads from constructor args or environment variables:

```bash
export PIGEONS_URL=http://localhost:3891
export PIGEONS_API_KEY=pgn_...
```

```python
from pigeons import Pigeons

p = Pigeons()  # reads from env
```

## Resources

- `p.emails` — send, get, list, cancel, batch
- `p.domains` — add, list, verify, stats, delete
- `p.api_keys` — create, list, revoke
- `p.templates` — create, get, list, update, delete, preview
- `p.contacts` — create, get, list, update, delete, batch, unsubscribe, resubscribe
- `p.inboxes` — create, get, list, update, delete, pause, resume, set_catch_all
  - `p.inboxes.messages` — list, get, create
  - `p.inboxes.threads` — list, get, update
- `p.webhooks` — create, get, list, update, delete
- `p.campaigns` — create, get, list, update, send, cancel, pause, resume
- `p.sequences` — create, get, list, update, activate, pause, enroll, enrollments
- `p.topics` — create, get, list, update, delete
- `p.stats` — get (global stats)

## License

MIT
