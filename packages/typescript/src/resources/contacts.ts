import type { HttpClient } from '../http.js'
import type {
  Contact,
  CreateContactParams,
  UpdateContactParams,
  BatchCreateContactsResult,
  ListContactsParams,
  PaginatedResponse,
} from '../types.js'

export class ContactsResource {
  constructor(private readonly http: HttpClient) {}

  async create(params: CreateContactParams): Promise<Contact> {
    return this.http.post<Contact>('/v1/contacts', params)
  }

  async get(idOrEmail: string): Promise<Contact> {
    return this.http.get<Contact>(`/v1/contacts/${encodeURIComponent(idOrEmail)}`)
  }

  async list(params?: ListContactsParams): Promise<PaginatedResponse<Contact>> {
    const searchParams = new URLSearchParams()
    if (params?.cursor) searchParams.set('cursor', params.cursor)
    if (params?.limit) searchParams.set('limit', String(params.limit))
    if (params?.tag) searchParams.set('tag', params.tag)

    const query = searchParams.toString()
    const path = query ? `/v1/contacts?${query}` : '/v1/contacts'
    return this.http.get<PaginatedResponse<Contact>>(path)
  }

  async update(idOrEmail: string, params: UpdateContactParams): Promise<Contact> {
    return this.http.patch<Contact>(`/v1/contacts/${encodeURIComponent(idOrEmail)}`, params)
  }

  async delete(idOrEmail: string): Promise<{ id: string; deleted: boolean }> {
    return this.http.delete<{ id: string; deleted: boolean }>(`/v1/contacts/${encodeURIComponent(idOrEmail)}`)
  }

  async batch(contacts: CreateContactParams[]): Promise<BatchCreateContactsResult> {
    return this.http.post<BatchCreateContactsResult>('/v1/contacts/batch', contacts)
  }

  async unsubscribe(idOrEmail: string): Promise<Contact> {
    return this.http.post<Contact>(`/v1/contacts/${encodeURIComponent(idOrEmail)}/unsubscribe`, {})
  }

  async resubscribe(idOrEmail: string): Promise<Contact> {
    return this.http.post<Contact>(`/v1/contacts/${encodeURIComponent(idOrEmail)}/resubscribe`, {})
  }
}
