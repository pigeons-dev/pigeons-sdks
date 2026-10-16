import type { HttpClient } from '../http.js'
import type {
  Inbox,
  CreateInboxParams,
  UpdateInboxParams,
  ListInboxesParams,
  InboxMessage,
  SendInboxMessageParams,
  ListInboxMessagesParams,
  Thread,
  UpdateThreadParams,
  ListThreadsParams,
  PaginatedResponse,
} from '../types.js'

export class InboxMessagesResource {
  constructor(private readonly http: HttpClient) {}

  async list(inboxId: string, params?: ListInboxMessagesParams): Promise<PaginatedResponse<InboxMessage>> {
    const searchParams = new URLSearchParams()
    if (params?.cursor) searchParams.set('cursor', params.cursor)
    if (params?.limit) searchParams.set('limit', String(params.limit))
    if (params?.direction) searchParams.set('direction', params.direction)
    if (params?.threadId) searchParams.set('threadId', params.threadId)
    if (params?.labels) searchParams.set('labels', params.labels.join(','))

    const query = searchParams.toString()
    const path = query
      ? `/v1/inboxes/${inboxId}/messages?${query}`
      : `/v1/inboxes/${inboxId}/messages`
    return this.http.get<PaginatedResponse<InboxMessage>>(path)
  }

  async get(inboxId: string, messageId: string): Promise<InboxMessage> {
    return this.http.get<InboxMessage>(`/v1/inboxes/${inboxId}/messages/${messageId}`)
  }

  async create(inboxId: string, params: SendInboxMessageParams): Promise<InboxMessage> {
    return this.http.post<InboxMessage>(`/v1/inboxes/${inboxId}/messages`, params)
  }
}

export class InboxThreadsResource {
  constructor(private readonly http: HttpClient) {}

  async list(inboxId: string, params?: ListThreadsParams): Promise<PaginatedResponse<Thread>> {
    const searchParams = new URLSearchParams()
    if (params?.cursor) searchParams.set('cursor', params.cursor)
    if (params?.limit) searchParams.set('limit', String(params.limit))
    if (params?.status) searchParams.set('status', params.status)

    const query = searchParams.toString()
    const path = query
      ? `/v1/inboxes/${inboxId}/threads?${query}`
      : `/v1/inboxes/${inboxId}/threads`
    return this.http.get<PaginatedResponse<Thread>>(path)
  }

  async get(inboxId: string, threadId: string): Promise<Thread> {
    return this.http.get<Thread>(`/v1/inboxes/${inboxId}/threads/${threadId}`)
  }

  async update(inboxId: string, threadId: string, params: UpdateThreadParams): Promise<Thread> {
    return this.http.patch<Thread>(`/v1/inboxes/${inboxId}/threads/${threadId}`, params)
  }
}

export class InboxesResource {
  public readonly messages: InboxMessagesResource
  public readonly threads: InboxThreadsResource

  constructor(private readonly http: HttpClient) {
    this.messages = new InboxMessagesResource(http)
    this.threads = new InboxThreadsResource(http)
  }

  async create(params: CreateInboxParams): Promise<Inbox> {
    return this.http.post<Inbox>('/v1/inboxes', params)
  }

  async list(params?: ListInboxesParams): Promise<PaginatedResponse<Inbox>> {
    const searchParams = new URLSearchParams()
    if (params?.cursor) searchParams.set('cursor', params.cursor)
    if (params?.limit) searchParams.set('limit', String(params.limit))
    if (params?.status) searchParams.set('status', params.status)
    if (params?.labels) searchParams.set('labels', params.labels.join(','))

    const query = searchParams.toString()
    const path = query ? `/v1/inboxes?${query}` : '/v1/inboxes'
    return this.http.get<PaginatedResponse<Inbox>>(path)
  }

  async get(id: string): Promise<Inbox> {
    return this.http.get<Inbox>(`/v1/inboxes/${id}`)
  }

  async update(id: string, params: UpdateInboxParams): Promise<Inbox> {
    return this.http.patch<Inbox>(`/v1/inboxes/${id}`, params)
  }

  async delete(id: string): Promise<{ id: string; deleted: boolean }> {
    return this.http.delete<{ id: string; deleted: boolean }>(`/v1/inboxes/${id}`)
  }

  async pause(id: string): Promise<Inbox> {
    return this.http.post<Inbox>(`/v1/inboxes/${id}/pause`, {})
  }

  async resume(id: string): Promise<Inbox> {
    return this.http.post<Inbox>(`/v1/inboxes/${id}/resume`, {})
  }

  async setCatchAll(id: string): Promise<Inbox> {
    return this.http.post<Inbox>(`/v1/inboxes/${id}/catch-all`, {})
  }
}
