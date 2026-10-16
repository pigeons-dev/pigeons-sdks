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

export interface Inbox {
  id: string
  name: string
  emailAddress: string
  description?: string
  webhookUrl?: string
  metadata?: Record<string, unknown>
  autoReplyEnabled: boolean
  labels?: string[]
  status: 'active' | 'paused' | 'archived'
  catchAll: boolean
  createdAt: string
  updatedAt: string
}

export interface CreateInboxParams {
  name: string
  emailAddress?: string
  description?: string
  webhookUrl?: string
  metadata?: Record<string, unknown>
  autoReplyEnabled?: boolean
  labels?: string[]
}

export interface UpdateInboxParams {
  name?: string
  description?: string
  webhookUrl?: string
  metadata?: Record<string, unknown>
  autoReplyEnabled?: boolean
  labels?: string[]
}

export interface ListInboxesParams {
  cursor?: string
  limit?: number
  status?: Inbox['status']
  labels?: string[]
}

export interface InboxMessage {
  id: string
  inboxId: string
  direction: 'inbound' | 'outbound'
  from: string
  to: string[]
  subject: string
  html?: string
  text?: string
  extractedHtml?: string
  extractedText?: string
  threadId: string
  inReplyTo?: string
  labels?: string[]
  attachments?: InboxMessageAttachment[]
  sesMessageId?: string
  createdAt: string
}

export interface InboxMessageAttachment {
  filename: string
  contentType: string
  size: number
  url: string
}

export interface SendInboxMessageParams {
  to: string | string[]
  subject?: string
  html?: string
  text?: string
  inReplyTo?: string
  labels?: string[]
}

export interface ListInboxMessagesParams {
  cursor?: string
  limit?: number
  direction?: InboxMessage['direction']
  threadId?: string
  labels?: string[]
}

export interface Thread {
  id: string
  inboxId: string
  subject: string
  lastMessageAt: string
  messageCount: number
  participants: string[]
  status: 'open' | 'closed' | 'snoozed'
  metadata?: Record<string, unknown>
  createdAt: string
  updatedAt: string
}

export interface UpdateThreadParams {
  status?: Thread['status']
  metadata?: Record<string, unknown>
}

export interface ListThreadsParams {
  cursor?: string
  limit?: number
  status?: Thread['status']
}

export interface Webhook {
  id: string
  url: string
  events: string[]
  secret?: string
  status: 'active' | 'disabled'
  failureCount: number
  lastTriggeredAt?: string
  createdAt: string
  updatedAt: string
}

export interface CreateWebhookParams {
  url: string
  events: string[]
  secret?: string
}

export interface UpdateWebhookParams {
  url?: string
  events?: string[]
  secret?: string
  status?: Webhook['status']
}

export interface ListWebhooksParams {
  cursor?: string
  limit?: number
}

export interface PaginatedResponse<T> {
  data: T[]
  has_more: boolean
  next_cursor: string | null
}
