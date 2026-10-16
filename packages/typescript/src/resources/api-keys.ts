import type { HttpClient } from '../http.js'
import type { ApiKey, CreateApiKeyParams } from '../types.js'

export class ApiKeysResource {
  constructor(private readonly http: HttpClient) {}

  async create(params: CreateApiKeyParams): Promise<ApiKey & { key: string }> {
    return this.http.post<ApiKey & { key: string }>('/v1/api-keys', params)
  }

  async list(): Promise<{ data: ApiKey[] }> {
    return this.http.get<{ data: ApiKey[] }>('/v1/api-keys')
  }

  async revoke(id: string): Promise<{ id: string; deleted: boolean }> {
    return this.http.delete<{ id: string; deleted: boolean }>(`/v1/api-keys/${id}`)
  }
}
