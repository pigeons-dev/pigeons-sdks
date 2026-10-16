import type { HttpClient } from '../http.js'
import type {
  Email,
  SendEmailParams,
  ListEmailsParams,
  PaginatedResponse,
} from '../types.js'

export class EmailsResource {
  constructor(private readonly http: HttpClient) {}

  async send(params: SendEmailParams, options?: { idempotencyKey?: string }): Promise<Email> {
    const headers: Record<string, string> = {}
    if (options?.idempotencyKey) {
      headers['Idempotency-Key'] = options.idempotencyKey
    }
    return this.http.post<Email>('/api/v1/emails', params, headers)
  }

  async get(id: string): Promise<Email> {
    return this.http.get<Email>(`/api/v1/emails/${id}`)
  }

  async list(params?: ListEmailsParams): Promise<PaginatedResponse<Email>> {
    const searchParams = new URLSearchParams()
    if (params?.cursor) searchParams.set('cursor', params.cursor)
    if (params?.limit) searchParams.set('limit', String(params.limit))
    if (params?.status) searchParams.set('status', params.status)

    const query = searchParams.toString()
    const path = query ? `/api/v1/emails?${query}` : '/api/v1/emails'
    return this.http.get<PaginatedResponse<Email>>(path)
  }

  async cancel(id: string): Promise<Email> {
    return this.http.post<Email>(`/api/v1/emails/${id}/cancel`, {})
  }

  async batch(emails: SendEmailParams[]): Promise<Email[]> {
    return this.http.post<Email[]>('/api/v1/emails/batch', emails)
  }
}
