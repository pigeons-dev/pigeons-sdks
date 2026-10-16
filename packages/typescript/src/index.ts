export { Pigeons } from './pigeons.js'
export type { PigeonsConfig } from './pigeons.js'
export { EmailsResource } from './resources/emails.js'
export { DomainsResource } from './resources/domains.js'
export { ApiKeysResource } from './resources/api-keys.js'
export { TemplatesResource } from './resources/templates.js'
export { ContactsResource } from './resources/contacts.js'
export type {
  Email,
  SendEmailParams,
  ListEmailsParams,
  BatchSendParams,
  Domain,
  AddDomainParams,
  DomainRecord,
  ApiKey,
  CreateApiKeyParams,
  Template,
  CreateTemplateParams,
  UpdateTemplateParams,
  TemplatePreview,
  Contact,
  CreateContactParams,
  UpdateContactParams,
  BatchCreateContactsResult,
  ListContactsParams,
  PaginatedResponse,
} from './types.js'
export { PigeonsError, ValidationError, AuthError, NotFoundError, RateLimitError } from './errors.js'
