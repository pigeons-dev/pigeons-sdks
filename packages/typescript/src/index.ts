export { Pigeons } from './pigeons.js'
export type { PigeonsConfig } from './pigeons.js'
export { EmailsResource } from './resources/emails.js'
export { DomainsResource } from './resources/domains.js'
export { ApiKeysResource } from './resources/api-keys.js'
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
  PaginatedResponse,
} from './types.js'
export { PigeonsError, ValidationError, AuthError, NotFoundError, RateLimitError } from './errors.js'
