# Contributing to Pigeons SDKs

Thanks for your interest in contributing to the Pigeons SDKs. This guide covers how to set up the project, make changes, and submit a pull request.

## Getting Started

```bash
git clone https://github.com/pigeons-dev/pigeons-sdks.git
cd pigeons-sdks
pnpm install
pnpm build
pnpm test
```

## Project Structure

```
packages/
  typescript/   @pigeons/pigeons-ts   TypeScript SDK
  python/       pigeons-py            Python SDK
```

## TypeScript SDK

The SDK is a thin typed wrapper around the Pigeons HTTP API. It has no business logic.

```bash
pnpm --filter @pigeons/pigeons-ts build
pnpm --filter @pigeons/pigeons-ts test
```

Key files:

- `src/pigeons.ts` - main client class, instantiates resource classes
- `src/resources/` - one file per API resource (emails, inboxes, etc.)
- `src/http.ts` - fetch-based HTTP client with auth and error mapping
- `src/types.ts` - all TypeScript types
- `src/errors.ts` - error classes

### Adding a new resource

1. Add the resource class in `src/resources/`.
2. Add types in `src/types.ts`.
3. Instantiate it in `src/pigeons.ts`.
4. Export it from `src/index.ts`.
5. Add tests.

## Python SDK

```bash
cd packages/python
pip install -e ".[dev]"
pytest
```

## Making Changes

1. Fork the repo and create a branch from `main`.
2. Make your changes. Add tests for new behavior.
3. Run `pnpm test` and `pnpm build` to verify.
4. Commit with a short, descriptive message (e.g., `feat: add sequences resource`).
5. Open a pull request against `main`.

### Commit messages

Use single-line semantic commit messages:

```
feat: add campaigns resource
fix: handle empty response body
docs: add idempotency example
test: add batch send tests
```

## License

By contributing, you agree that your contributions will be licensed under MIT.
