import { HttpClient } from './http.js'
import { EmailsResource } from './resources/emails.js'
import { DomainsResource } from './resources/domains.js'
import { ApiKeysResource } from './resources/api-keys.js'

export interface PigeonsConfig {
  baseUrl: string
  apiKey: string
}

export class Pigeons {
  private readonly http: HttpClient

  public readonly emails: EmailsResource
  public readonly domains: DomainsResource
  public readonly apiKeys: ApiKeysResource

  constructor(config?: Partial<PigeonsConfig>) {
    const baseUrl = config?.baseUrl ?? process.env.PIGEONS_URL
    const apiKey = config?.apiKey ?? process.env.PIGEONS_API_KEY

    if (!baseUrl) {
      throw new Error(
        'Pigeons baseUrl is required. Pass it in the constructor or set PIGEONS_URL environment variable.',
      )
    }

    if (!apiKey) {
      throw new Error(
        'Pigeons apiKey is required. Pass it in the constructor or set PIGEONS_API_KEY environment variable.',
      )
    }

    this.http = new HttpClient(baseUrl.replace(/\/+$/, ''), apiKey)

    this.emails = new EmailsResource(this.http)
    this.domains = new DomainsResource(this.http)
    this.apiKeys = new ApiKeysResource(this.http)
  }
}
