export class PigeonsError extends Error {
  constructor(
    public readonly type: string,
    message: string,
    public readonly code: string,
    public readonly statusCode: number,
  ) {
    super(message)
    this.name = 'PigeonsError'
  }
}

export class ValidationError extends PigeonsError {
  constructor(message: string, code: string = 'validation_error') {
    super('validation_error', message, code, 400)
    this.name = 'ValidationError'
  }
}

export class AuthError extends PigeonsError {
  constructor(message: string = 'Invalid or missing API key') {
    super('authentication_error', message, 'unauthorized', 401)
    this.name = 'AuthError'
  }
}

export class NotFoundError extends PigeonsError {
  constructor(message: string = 'Resource not found') {
    super('not_found', message, 'not_found', 404)
    this.name = 'NotFoundError'
  }
}

export class RateLimitError extends PigeonsError {
  constructor(message: string = 'Rate limit exceeded') {
    super('rate_limit_error', message, 'rate_limited', 429)
    this.name = 'RateLimitError'
  }
}
