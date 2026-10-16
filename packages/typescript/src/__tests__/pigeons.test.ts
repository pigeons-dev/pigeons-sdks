import { describe, it, expect } from 'vitest'
import { Pigeons } from '../pigeons.js'
import { PigeonsError, ValidationError, AuthError, NotFoundError, RateLimitError } from '../errors.js'

describe('Pigeons constructor', () => {
  it('throws when baseUrl is missing', () => {
    delete process.env.PIGEONS_URL
    expect(() => new Pigeons({ apiKey: 'pgn_test' })).toThrow('baseUrl is required')
  })

  it('throws when apiKey is missing', () => {
    delete process.env.PIGEONS_API_KEY
    expect(() => new Pigeons({ baseUrl: 'http://localhost:3891' })).toThrow('apiKey is required')
  })

  it('creates instance with explicit config', () => {
    const p = new Pigeons({ baseUrl: 'http://localhost:3891', apiKey: 'pgn_test' })
    expect(p.emails).toBeDefined()
    expect(p.domains).toBeDefined()
    expect(p.apiKeys).toBeDefined()
  })

  it('reads from env vars', () => {
    process.env.PIGEONS_URL = 'http://localhost:3891'
    process.env.PIGEONS_API_KEY = 'pgn_test'
    const p = new Pigeons()
    expect(p.emails).toBeDefined()
    delete process.env.PIGEONS_URL
    delete process.env.PIGEONS_API_KEY
  })

  it('strips trailing slashes from baseUrl', () => {
    const p = new Pigeons({ baseUrl: 'http://localhost:3891///', apiKey: 'pgn_test' })
    expect(p.emails).toBeDefined()
  })
})

describe('error classes', () => {
  it('ValidationError has correct properties', () => {
    const err = new ValidationError('bad input', 'invalid_field')
    expect(err).toBeInstanceOf(PigeonsError)
    expect(err.name).toBe('ValidationError')
    expect(err.type).toBe('validation_error')
    expect(err.statusCode).toBe(400)
    expect(err.code).toBe('invalid_field')
  })

  it('AuthError has correct properties', () => {
    const err = new AuthError()
    expect(err).toBeInstanceOf(PigeonsError)
    expect(err.name).toBe('AuthError')
    expect(err.statusCode).toBe(401)
  })

  it('NotFoundError has correct properties', () => {
    const err = new NotFoundError()
    expect(err).toBeInstanceOf(PigeonsError)
    expect(err.name).toBe('NotFoundError')
    expect(err.statusCode).toBe(404)
  })

  it('RateLimitError has correct properties', () => {
    const err = new RateLimitError()
    expect(err).toBeInstanceOf(PigeonsError)
    expect(err.name).toBe('RateLimitError')
    expect(err.statusCode).toBe(429)
  })
})
