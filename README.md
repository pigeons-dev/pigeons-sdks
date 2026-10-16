# Pigeons SDKs

Official SDKs for [Pigeons](https://github.com/pigeons-dev/pigeons) — open-source, self-hosted email infrastructure for developers and AI agents.

## TypeScript SDK

```bash
npm install @pigeons/sdk
```

### Setup

```typescript
import { Pigeons } from '@pigeons/sdk'

const pigeons = new Pigeons({
  baseUrl: 'https://mail.yourapp.com', // your self-hosted instance
  apiKey: 'pgn_...',
})
```

`baseUrl` falls back to the `PIGEONS_URL` environment variable. `apiKey` falls back to `PIGEONS_API_KEY`.

### Send an email

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

### List emails

```typescript
const { data, has_more, next_cursor } = await pigeons.emails.list({
  status: 'delivered',
  limit: 25,
})
```

### Domains

```typescript
// Add a domain and get DNS records to configure
const domain = await pigeons.domains.add({ domain: 'yourapp.com' })
console.log(domain.records) // DKIM, SPF, DMARC records

// Check verification status
const verified = await pigeons.domains.verify(domain.id)
```

### API keys

```typescript
const key = await pigeons.apiKeys.create({ name: 'production' })
console.log(key.key) // pgn_... (shown once)

const keys = await pigeons.apiKeys.list()
await pigeons.apiKeys.revoke(key.id)
```

### Error handling

```typescript
import { AuthError, RateLimitError, ValidationError } from '@pigeons/sdk'

try {
  await pigeons.emails.send({ to: 'bad', subject: 'Test', html: '...' })
} catch (err) {
  if (err instanceof ValidationError) console.log(err.message)
  if (err instanceof RateLimitError) console.log('Slow down')
  if (err instanceof AuthError) console.log('Bad API key')
}
```

### Idempotency

Pass an idempotency key on mutating requests to safely retry:

```typescript
const email = await pigeons.emails.send(
  { to: 'user@example.com', subject: 'Receipt', html: '...' },
  { idempotencyKey: 'order-4821-receipt' },
)
```

## Packages

| Package | Description | Status |
|---|---|---|
| [`@pigeons/sdk`](packages/typescript) | TypeScript SDK | Available |
| Python SDK | Python SDK | Planned |

## Development

```bash
pnpm install
pnpm build
pnpm test
```

## License

MIT — see [LICENSE](LICENSE).
