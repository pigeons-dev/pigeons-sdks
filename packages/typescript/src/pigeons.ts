import { HttpClient } from './http.js'
import { EmailsResource } from './resources/emails.js'
import { DomainsResource } from './resources/domains.js'
import { ApiKeysResource } from './resources/api-keys.js'
import { TemplatesResource } from './resources/templates.js'
import { ContactsResource } from './resources/contacts.js'
import { InboxesResource } from './resources/inboxes.js'
import { WebhooksResource } from './resources/webhooks.js'
import { CampaignsResource } from './resources/campaigns.js'
import { SequencesResource } from './resources/sequences.js'
import { TopicsResource } from './resources/topics.js'

export interface PigeonsConfig {
  baseUrl: string
  apiKey: string
}

export class Pigeons {
  private readonly http: HttpClient

  public readonly emails: EmailsResource
  public readonly domains: DomainsResource
  public readonly apiKeys: ApiKeysResource
  public readonly templates: TemplatesResource
  public readonly contacts: ContactsResource
  public readonly inboxes: InboxesResource
  public readonly webhooks: WebhooksResource
  public readonly campaigns: CampaignsResource
  public readonly sequences: SequencesResource
  public readonly topics: TopicsResource

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
    this.templates = new TemplatesResource(this.http)
    this.contacts = new ContactsResource(this.http)
    this.inboxes = new InboxesResource(this.http)
    this.webhooks = new WebhooksResource(this.http)
    this.campaigns = new CampaignsResource(this.http)
    this.sequences = new SequencesResource(this.http)
    this.topics = new TopicsResource(this.http)
  }
}
