export interface Email {
  id: string
  from: string
  to: string[]
  cc?: string[]
  bcc?: string[]
  subject: string
  html?: string
  text?: string
  status: 'queued' | 'sending' | 'sent' | 'delivered' | 'bounced' | 'complained' | 'failed'
  sesMessageId?: string
  tags?: string[]
  headers?: Record<string, string>
  scheduledAt?: string
  createdAt: string
  updatedAt: string
}

export interface SendEmailParams {
  from?: string
  to: string | string[]
  cc?: string[]
  bcc?: string[]
  subject?: string
  html?: string
  text?: string
  templateId?: string
  data?: Record<string, unknown>
  tags?: string[]
  headers?: Record<string, string>
  scheduledAt?: string
}

export interface ListEmailsParams {
  cursor?: string
  limit?: number
  status?: Email['status']
}

export type BatchSendParams = SendEmailParams[]

export interface Domain {
  id: string
  domain: string
  verificationStatus: 'pending' | 'verified' | 'failed'
  dkimTokens?: string[]
  spfVerified: boolean
  dmarcVerified: boolean
  region: string
  capabilities: { sending: boolean; receiving: boolean }
  records?: DomainRecord[]
  createdAt: string
  updatedAt: string
}

export interface DomainRecord {
  type: string
  name: string
  value: string
  ttl: number
  status: string
  purpose: string
}

export interface AddDomainParams {
  domain: string
  capabilities?: { sending?: boolean; receiving?: boolean }
}

export interface ApiKey {
  id: string
  name: string
  prefix: string
  key?: string
  scopes?: string[]
  expiresAt?: string
  lastUsedAt?: string
  createdAt: string
}

export interface CreateApiKeyParams {
  name: string
  scopes?: string[]
  expiresAt?: string
}

export interface Template {
  id: string
  slug: string
  name: string
  subject: string
  body: string
  sampleData?: Record<string, unknown>
  version: number
  createdAt: string
  updatedAt: string
}

export interface CreateTemplateParams {
  slug: string
  name: string
  subject: string
  body: string
  sampleData?: Record<string, unknown>
}

export interface UpdateTemplateParams {
  name?: string
  subject?: string
  body?: string
  sampleData?: Record<string, unknown>
}

export interface TemplatePreview {
  subject: string
  html: string
  text: string
}

export interface Contact {
  id: string
  email: string
  firstName?: string
  lastName?: string
  tags?: string[]
  properties?: Record<string, unknown>
  unsubscribed: boolean
  unsubscribedAt?: string
  bounced: boolean
  bouncedAt?: string
  complained: boolean
  complainedAt?: string
  createdAt: string
  updatedAt: string
}

export interface CreateContactParams {
  email: string
  firstName?: string
  lastName?: string
  tags?: string[]
  properties?: Record<string, unknown>
}

export interface UpdateContactParams {
  firstName?: string
  lastName?: string
  tags?: string[]
  properties?: Record<string, unknown>
}

export interface BatchCreateContactsResult {
  created: number
  skipped: number
  contacts: Array<{ id: string; email: string }>
}

export interface ListContactsParams {
  cursor?: string
  limit?: number
  tag?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  has_more: boolean
  next_cursor: string | null
}
