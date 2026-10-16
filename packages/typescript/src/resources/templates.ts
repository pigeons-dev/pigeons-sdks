import type { HttpClient } from '../http.js'
import type {
  Template,
  CreateTemplateParams,
  UpdateTemplateParams,
  TemplatePreview,
  PaginatedResponse,
} from '../types.js'

export class TemplatesResource {
  constructor(private readonly http: HttpClient) {}

  async create(params: CreateTemplateParams): Promise<Template> {
    return this.http.post<Template>('/v1/templates', params)
  }

  async get(idOrSlug: string): Promise<Template> {
    return this.http.get<Template>(`/v1/templates/${idOrSlug}`)
  }

  async list(params?: { cursor?: string; limit?: number }): Promise<PaginatedResponse<Template>> {
    const searchParams = new URLSearchParams()
    if (params?.cursor) searchParams.set('cursor', params.cursor)
    if (params?.limit) searchParams.set('limit', String(params.limit))

    const query = searchParams.toString()
    const path = query ? `/v1/templates?${query}` : '/v1/templates'
    return this.http.get<PaginatedResponse<Template>>(path)
  }

  async update(idOrSlug: string, params: UpdateTemplateParams): Promise<Template> {
    return this.http.patch<Template>(`/v1/templates/${idOrSlug}`, params)
  }

  async delete(idOrSlug: string): Promise<{ id: string; deleted: boolean }> {
    return this.http.delete<{ id: string; deleted: boolean }>(`/v1/templates/${idOrSlug}`)
  }

  async preview(idOrSlug: string, data?: Record<string, unknown>): Promise<TemplatePreview> {
    return this.http.post<TemplatePreview>(`/v1/templates/${idOrSlug}/preview`, { data })
  }
}
