import type { HttpClient } from '../http.js'
import type {
  Webhook,
  CreateWebhookParams,
  UpdateWebhookParams,
  ListWebhooksParams,
  PaginatedResponse,
} from '../types.js'

export class WebhooksResource {
  constructor(private readonly http: HttpClient) {}

  async create(params: CreateWebhookParams): Promise<Webhook> {
    return this.http.post<Webhook>('/v1/webhooks', params)
  }

  async list(params?: ListWebhooksParams): Promise<PaginatedResponse<Webhook>> {
    const searchParams = new URLSearchParams()
    if (params?.cursor) searchParams.set('cursor', params.cursor)
    if (params?.limit) searchParams.set('limit', String(params.limit))

    const query = searchParams.toString()
    const path = query ? `/v1/webhooks?${query}` : '/v1/webhooks'
    return this.http.get<PaginatedResponse<Webhook>>(path)
  }

  async get(id: string): Promise<Webhook> {
    return this.http.get<Webhook>(`/v1/webhooks/${id}`)
  }

  async update(id: string, params: UpdateWebhookParams): Promise<Webhook> {
    return this.http.patch<Webhook>(`/v1/webhooks/${id}`, params)
  }

  async delete(id: string): Promise<{ id: string; deleted: boolean }> {
    return this.http.delete<{ id: string; deleted: boolean }>(`/v1/webhooks/${id}`)
  }
}
