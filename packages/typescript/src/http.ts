import { PigeonsError, ValidationError, AuthError, NotFoundError, RateLimitError } from './errors.js'

export class HttpClient {
  constructor(
    private readonly baseUrl: string,
    private readonly apiKey: string,
  ) {}

  async request<T>(method: string, path: string, body?: unknown, headers?: Record<string, string>): Promise<T> {
    const url = `${this.baseUrl}${path}`

    const res = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.apiKey}`,
        ...headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    })

    const data = await res.json().catch(() => null)

    if (!res.ok) {
      const error = (data as any)?.error
      const message = error?.message ?? `HTTP ${res.status}`
      const type = error?.type ?? 'unknown_error'
      const code = error?.code ?? 'unknown'

      switch (res.status) {
        case 400:
          throw new ValidationError(message, code)
        case 401:
          throw new AuthError(message)
        case 404:
          throw new NotFoundError(message)
        case 429:
          throw new RateLimitError(message)
        default:
          throw new PigeonsError(type, message, code, res.status)
      }
    }

    return data as T
  }

  get<T>(path: string): Promise<T> {
    return this.request<T>('GET', path)
  }

  post<T>(path: string, body: unknown, headers?: Record<string, string>): Promise<T> {
    return this.request<T>('POST', path, body, headers)
  }

  patch<T>(path: string, body: unknown): Promise<T> {
    return this.request<T>('PATCH', path, body)
  }

  delete<T>(path: string): Promise<T> {
    return this.request<T>('DELETE', path)
  }
}
