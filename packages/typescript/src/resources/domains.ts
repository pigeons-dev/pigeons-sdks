import type { HttpClient } from '../http.js'
import type { Domain, AddDomainParams, PaginatedResponse } from '../types.js'

export class DomainsResource {
  constructor(private readonly http: HttpClient) {}

  async add(params: AddDomainParams): Promise<Domain> {
    return this.http.post<Domain>('/v1/domains', params)
  }

  async list(): Promise<{ data: Domain[] }> {
    return this.http.get<{ data: Domain[] }>('/v1/domains')
  }

  async verify(id: string): Promise<Domain> {
    return this.http.get<Domain>(`/v1/domains/${id}/verify`)
  }

  async delete(id: string): Promise<{ id: string; deleted: boolean }> {
    return this.http.delete<{ id: string; deleted: boolean }>(`/v1/domains/${id}`)
  }
}
