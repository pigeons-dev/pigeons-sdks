import type { HttpClient } from '../http.js'
import type {
  SubscriptionTopic,
  CreateTopicParams,
  UpdateTopicParams,
  ListTopicsParams,
  PaginatedResponse,
} from '../types.js'

export class TopicsResource {
  constructor(private readonly http: HttpClient) {}

  async create(params: CreateTopicParams): Promise<SubscriptionTopic> {
    return this.http.post<SubscriptionTopic>('/v1/topics', params)
  }

  async get(id: string): Promise<SubscriptionTopic> {
    return this.http.get<SubscriptionTopic>(`/v1/topics/${id}`)
  }

  async list(params?: ListTopicsParams): Promise<PaginatedResponse<SubscriptionTopic>> {
    const searchParams = new URLSearchParams()
    if (params?.cursor) searchParams.set('cursor', params.cursor)
    if (params?.limit) searchParams.set('limit', String(params.limit))

    const query = searchParams.toString()
    const path = query ? `/v1/topics?${query}` : '/v1/topics'
    return this.http.get<PaginatedResponse<SubscriptionTopic>>(path)
  }

  async update(id: string, params: UpdateTopicParams): Promise<SubscriptionTopic> {
    return this.http.patch<SubscriptionTopic>(`/v1/topics/${id}`, params)
  }

  async delete(id: string): Promise<void> {
    return this.http.delete(`/v1/topics/${id}`)
  }
}
