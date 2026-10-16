import type { HttpClient } from '../http.js'
import type {
  Campaign,
  CreateCampaignParams,
  UpdateCampaignParams,
  ListCampaignsParams,
  PaginatedResponse,
} from '../types.js'

export class CampaignsResource {
  constructor(private readonly http: HttpClient) {}

  async create(params: CreateCampaignParams): Promise<Campaign> {
    return this.http.post<Campaign>('/v1/campaigns', params)
  }

  async get(id: string): Promise<Campaign> {
    return this.http.get<Campaign>(`/v1/campaigns/${id}`)
  }

  async list(params?: ListCampaignsParams): Promise<PaginatedResponse<Campaign>> {
    const searchParams = new URLSearchParams()
    if (params?.cursor) searchParams.set('cursor', params.cursor)
    if (params?.limit) searchParams.set('limit', String(params.limit))
    if (params?.status) searchParams.set('status', params.status)

    const query = searchParams.toString()
    const path = query ? `/v1/campaigns?${query}` : '/v1/campaigns'
    return this.http.get<PaginatedResponse<Campaign>>(path)
  }

  async update(id: string, params: UpdateCampaignParams): Promise<Campaign> {
    return this.http.patch<Campaign>(`/v1/campaigns/${id}`, params)
  }

  async send(id: string, opts?: { scheduledAt?: string }): Promise<Campaign> {
    return this.http.post<Campaign>(`/v1/campaigns/${id}/send`, opts ?? {})
  }

  async cancel(id: string): Promise<Campaign> {
    return this.http.post<Campaign>(`/v1/campaigns/${id}/cancel`, {})
  }

  async pause(id: string): Promise<Campaign> {
    return this.http.post<Campaign>(`/v1/campaigns/${id}/pause`, {})
  }

  async resume(id: string): Promise<Campaign> {
    return this.http.post<Campaign>(`/v1/campaigns/${id}/resume`, {})
  }
}
