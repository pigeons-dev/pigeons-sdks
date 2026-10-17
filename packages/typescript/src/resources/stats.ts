import type { HttpClient } from '../http.js'
import type { GlobalStats } from '../types.js'

export class StatsResource {
  constructor(private readonly http: HttpClient) {}

  async get(): Promise<GlobalStats> {
    return this.http.get<GlobalStats>('/v1/stats')
  }
}
