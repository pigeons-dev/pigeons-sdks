# Pigeons SDKs

Official SDKs for [Pigeons](https://github.com/pigeons-dev/pigeons) - open source, self-hosted email infrastructure for developers and AI agents.

## TypeScript SDK

```bash
npm install @pigeons/pigeons-ts
```

### Setup

```typescript
import { Pigeons } from '@pigeons/pigeons-ts'

const pigeons = new Pigeons({
  baseUrl: 'http://localhost:3891', // your self-hosted instance
  apiKey: 'pgn_...',
})
```

`baseUrl` falls back to the `PIGEONS_URL` environment variable. `apiKey` falls back to `PIGEONS_API_KEY`.

### Send email

```typescript
const email = await pigeons.emails.send({
  to: 'user@example.com',
  subject: 'Welcome aboard',
  html: '<h1>Welcome!</h1>',
})
console.log(email.id) // msg_...
```

### Batch send

```typescript
const emails = await pigeons.emails.batch([
  { to: 'alice@example.com', subject: 'Hello', html: '<p>Hi Alice</p>' },
  { to: 'bob@example.com', subject: 'Hello', html: '<p>Hi Bob</p>' },
])
```

### Inboxes

```typescript
const inbox = await pigeons.inboxes.create({
  address: 'support',
  domain: 'yourapp.com',
  webhookUrl: 'https://yourapp.com/hooks/email',
})

const { data: messages } = await pigeons.inboxes.messages.list(inbox.id)

const { data: threads } = await pigeons.inboxes.threads.list(inbox.id)
```

### Templates

```typescript
const template = await pigeons.templates.create({
  name: 'welcome',
  subject: 'Welcome, {{name}}!',
  html: '<h1>Hello {{name}}</h1>',
})

await pigeons.emails.send({
  to: 'user@example.com',
  templateId: template.id,
  templateData: { name: 'Alice' },
})
```

### Contacts

```typescript
const contact = await pigeons.contacts.create({
  email: 'alice@example.com',
  name: 'Alice',
  tags: ['beta'],
})

const { data: contacts } = await pigeons.contacts.list({ tag: 'beta' })
```

### Campaigns and sequences

```typescript
const campaign = await pigeons.campaigns.create({
  name: 'Product launch',
  fromEmail: 'hi@yourapp.com',
  subject: 'Introducing Pigeons',
  html: '<h1>Big news</h1>',
  tags: ['beta'],
})
await pigeons.campaigns.send(campaign.id)

const sequence = await pigeons.sequences.create({
  name: 'Onboarding',
  steps: [
    { type: 'email', templateId: 'tpl_...', delayDuration: '0m' },
    { type: 'delay', delayDuration: '1d' },
    { type: 'email', templateId: 'tpl_...', delayDuration: '0m' },
  ],
})
```

### Webhooks

```typescript
const webhook = await pigeons.webhooks.create({
  url: 'https://yourapp.com/hooks/pigeons',
  events: ['email.delivered', 'email.bounced', 'inbox.message.received'],
})
console.log(webhook.secret) // whsec_...
```

### Domains and stats

```typescript
const domain = await pigeons.domains.add({ domain: 'yourapp.com' })
console.log(domain.records) // DKIM, SPF, DMARC records

const stats = await pigeons.stats.global()
console.log(stats.sent, stats.delivered, stats.bounced)
```

### API keys

```typescript
const key = await pigeons.apiKeys.create({ name: 'production' })
console.log(key.key) // pgn_... (shown once)
```

### Idempotency

Pass an idempotency key on mutating requests to safely retry:

```typescript
const email = await pigeons.emails.send(
  { to: 'user@example.com', subject: 'Receipt', html: '...' },
  { idempotencyKey: 'order-4821-receipt' },
)
```

### Error handling

```typescript
import { AuthError, RateLimitError, ValidationError } from '@pigeons/pigeons-ts'

try {
  await pigeons.emails.send({ to: 'bad', subject: 'Test', html: '...' })
} catch (err) {
  if (err instanceof ValidationError) console.log(err.message)
  if (err instanceof RateLimitError) console.log('Slow down')
  if (err instanceof AuthError) console.log('Bad API key')
}
```

## Python SDK

```bash
pip install pigeons-py
```

```python
from pigeons import Pigeons

pigeons = Pigeons(
    base_url="http://localhost:3891",
    api_key="pgn_...",
)

# Send an email
email = pigeons.emails.send(
    to="user@example.com",
    subject="Welcome aboard",
    html="<h1>Welcome!</h1>",
)

# List emails
emails = pigeons.emails.list(status="delivered", limit=25)

# Inboxes
inbox = pigeons.inboxes.create(
    address="support",
    domain="yourapp.com",
    webhook_url="https://yourapp.com/hooks/email",
)
messages = pigeons.inboxes.messages.list(inbox.id)
```

`base_url` falls back to the `PIGEONS_URL` environment variable. `api_key` falls back to `PIGEONS_API_KEY`.

## All Resources

Both SDKs expose the same resources:

| Resource | Description |
|---|---|
| `emails` | Send, get, list, cancel, batch |
| `inboxes` | Create agent inboxes, manage messages and threads |
| `templates` | Create and manage reusable email templates |
| `contacts` | Manage contacts with tags |
| `campaigns` | Create and send one-off campaigns |
| `sequences` | Multi-step drip sequences |
| `topics` | Subscription topics for unsubscribe management |
| `webhooks` | Register webhook endpoints for events |
| `domains` | Add and verify sending/receiving domains |
| `apiKeys` | Create and revoke API keys |
| `stats` | Deliverability stats (global and per-domain) |

## Packages

| Package | Language | Install |
|---|---|---|
| [`@pigeons/pigeons-ts`](packages/typescript) | TypeScript | `npm install @pigeons/pigeons-ts` |
| [`pigeons-py`](packages/python) | Python | `pip install pigeons-py` |

## Development

```bash
git clone https://github.com/pigeons-dev/pigeons-sdks.git
cd pigeons-sdks
pnpm install
pnpm build
pnpm test
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT - see [LICENSE](LICENSE).
