import type { HttpClient } from '../http.js'
import type {
  Sequence,
  CreateSequenceParams,
  UpdateSequenceParams,
  ListSequencesParams,
  SequenceEnrollment,
  PaginatedResponse,
} from '../types.js'

export class SequencesResource {
  constructor(private readonly http: HttpClient) {}

  async create(params: CreateSequenceParams): Promise<Sequence> {
    return this.http.post<Sequence>('/v1/sequences', params)
  }

  async get(id: string): Promise<Sequence> {
    return this.http.get<Sequence>(`/v1/sequences/${id}`)
  }

  async list(params?: ListSequencesParams): Promise<PaginatedResponse<Sequence>> {
    const searchParams = new URLSearchParams()
    if (params?.cursor) searchParams.set('cursor', params.cursor)
    if (params?.limit) searchParams.set('limit', String(params.limit))
    if (params?.status) searchParams.set('status', params.status)

    const query = searchParams.toString()
    const path = query ? `/v1/sequences?${query}` : '/v1/sequences'
    return this.http.get<PaginatedResponse<Sequence>>(path)
  }

  async update(id: string, params: UpdateSequenceParams): Promise<Sequence> {
    return this.http.patch<Sequence>(`/v1/sequences/${id}`, params)
  }

  async activate(id: string): Promise<Sequence> {
    return this.http.post<Sequence>(`/v1/sequences/${id}/activate`, {})
  }

  async pause(id: string): Promise<Sequence> {
    return this.http.post<Sequence>(`/v1/sequences/${id}/pause`, {})
  }

  async enroll(id: string, contactId: string): Promise<SequenceEnrollment> {
    return this.http.post<SequenceEnrollment>(`/v1/sequences/${id}/enroll`, { contactId })
  }

  async enrollments(id: string, params?: { cursor?: string; limit?: number; status?: string }): Promise<PaginatedResponse<SequenceEnrollment>> {
    const searchParams = new URLSearchParams()
    if (params?.cursor) searchParams.set('cursor', params.cursor)
    if (params?.limit) searchParams.set('limit', String(params.limit))
    if (params?.status) searchParams.set('status', params.status)

    const query = searchParams.toString()
    const path = query ? `/v1/sequences/${id}/enrollments?${query}` : `/v1/sequences/${id}/enrollments`
    return this.http.get<PaginatedResponse<SequenceEnrollment>>(path)
  }
}
