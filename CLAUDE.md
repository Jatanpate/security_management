# NodeGoat (OWASP NodeJS Goat) — Project Reference

## Overview
Deliberately vulnerable Node.js web application built by OWASP for learning the OWASP Top 10 security vulnerabilities. Used here as a target for DAST (ZAP) scanning and security hardening.

- **Version:** 1.3.0
- **Entry point:** `server.js`
- **Framework:** Express 4, MongoDB (driver v2), Swig templates
- **Branch under fix:** `fix_dast` → PR into `master` on `github.com/Jatanpate/security_management`

## Running the App
```bash
# Start MongoDB (Docker)
npm run start-infra

# Start app (dev, port 5000)
npm run dev

# Start app (prod, default port)
npm start
```

## Running E2E Tests
```bash
# Full local run — spins up MongoDB in Docker, seeds DB, starts app, runs Cypress, tears down Mongo
npm run test:local

# CI run — requires MongoDB already running on localhost:27017; starts app automatically
npm run test:ci

# Interactive Cypress UI — requires app already running on port 4000
npm run test:e2e
```

## Key File Map
| Path | Purpose |
|------|---------|
| `server.js` | Express app setup, middleware, session config |
| `app/routes/index.js` | All route definitions and middleware wiring |
| `app/routes/session.js` | Login, signup, logout, session handling |
| `app/routes/profile.js` | Profile display and update |
| `app/routes/contributions.js` | Contributions update |
| `app/routes/allocations.js` | Allocations display |
| `app/routes/memos.js` | Memos display and insert |
| `app/routes/research.js` | Research / SSRF-vulnerable endpoint |
| `app/routes/benefits.js` | Admin benefits management |
| `app/data/user-dao.js` | User DB operations (add, validate, lookup) |
| `app/data/allocations-dao.js` | Allocations DB operations |
| `app/data/memos-dao.js` | Memos DB operations |
| `config/` | Environment-specific config (port, db, cookieSecret) |

---

## Security Issues — Status Tracker

### Fixed
| # | Category | File | Description |
|---|----------|------|-------------|
| 1 | A1 — NoSQL Injection | `allocations-dao.js` | Replaced `$where` JS expression with structured MongoDB query (`userId` + `$gt`) |
| 2 | A1 — NoSQL Injection | `user-dao.js` | `validateLogin` and `getUserByUserName` now reject non-string and non-alphanumeric usernames |
| 3 | A1 — Log Injection (CRLF) | `session.js` | Failed login now encodes `userName` via `node-esapi` before logging |
| 4 | A1 — SSJS Injection | `contributions.js` | Replaced unsafe `parseint` call with `parseInt` (built-in) |
| 5 | A2 — Plaintext passwords | `user-dao.js` | Passwords hashed with `bcrypt` on signup (`bcrypt.hashSync`) |
| 6 | A2 — Plaintext comparison | `user-dao.js` | Login uses `bcrypt.compareSync` instead of `===` |
| 7 | A2 — Weak password policy | `session.js` | Signup regex strengthened to `/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/` |
| 8 | A2 — Session fixation | `session.js` | Login calls `req.session.regenerate()` and sets `userId` inside the callback |
| 9 | A2 — Username enumeration | `session.js` | Both invalid-user and invalid-password login paths now return the same generic error message |
| 10 | A3 — XSS (template) | `server.js` | Swig `autoescape` set to `true` |
| 11 | A3 — XSS (cookie) | `server.js` | Session cookie now has `httpOnly: true` and `secure: true` |
| 12 | A3 — XSS (wrong encoding) | `profile.js` | `doc.website` now encoded with `encodeForURL` instead of `encodeForHTML` |
| 13 | A4 — Insecure DOR | `allocations.js` | `userId` now read from `req.session` instead of `req.params` |
| 14 | A5 — Security misconfig | `server.js` | Enabled `helmet` (frameguard, noCache, CSP, HSTS, XSS filter), `nosniff`, and `x-powered-by` disabled |
| 15 | A5 — Session cookie name | `server.js` | Cookie key renamed to `sessionId` (not default `connect.sid`) |
| 16 | A7 — Missing access control | `index.js` | `/benefits` routes now require `isAdmin` middleware |
| 17 | A9 — ReDoS | `profile.js` | Bank routing regex changed from `/([0-9]+)+\#/` to `/([0-9])+\#/` to eliminate catastrophic backtracking |
| 18 | Rate limiting | `index.js` | `express-rate-limit` wired in (100 req / 15 min) |
| 19 | Bug — `RateLimit` undefined | `index.js` | Fixed import casing (`RateLimit` vs `rateLimit`) |
| 20 | Bug — `genuuid` undefined | `server.js` | Removed undefined `genid` block; `express-session` generates secure IDs by default |
| 21 | Bug — Login broken | `session.js` | `req.session.userId` was commented out; moved inside `regenerate()` callback so session is populated before redirect |

### Open
| # | Category | File | Description |
|---|----------|------|-------------|
| 22 | A6 — Sensitive data (HTTPS) | `server.js` | App still runs over HTTP; HTTPS block is commented out (requires cert setup) |
| 23 | A8 — CSRF | `server.js` | `csurf` middleware still commented out |
| 24 | A10 — SSRF fix incomplete | `research.js` | Allowlist contains placeholder URLs (`https://xyz.com`, `https://abc.com`) — no real stock API URL added |
| 25 | Broken auth (memos) | `memos.js` / `memos-dao.js` | `getAllMemos()` returns every user's memos with no ownership filter |

---

## E2E Pipeline Issues — Status Tracker

### Fixed
| # | File | Description |
|---|------|-------------|
| E1 | `test/e2e/integration/login_spec.js` | Error message assertions updated from `"Invalid password"` / `"Invalid username"` to generic `"Invalid username and/or password"` to match the username-enumeration fix |
| E2 | `test/e2e/fixtures/users/new_user.json` | Signup fixture password changed from `"123456"` to `"NewGoat1!"` to satisfy the strong password policy (`/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/`) |
| E3 | `.github/workflows/e2e-test.yml` | Updated `actions/checkout` and `actions/setup-node` from non-existent `@v6` to `@v4` |
| E4 | `.github/workflows/e2e-test.yml` | Removed EOL Node versions `10.x` and `12.x`; matrix is now `18.x`, `20.x`, `22.x` |
| E5 | `.github/workflows/e2e-test.yml` | Updated `actions/upload-artifact` from deprecated `@v2` to `@v4` |
| E6 | `server.js` | Removed `helmet.noCache()` and `helmet.iexss()` (not available in helmet v8); removed deprecated `setOnOldIE` option from `helmet.xssFilter()` |
| E7 | `package.json` | Added missing `express-rate-limit` dependency |
| E8 | `cypress.json` → `cypress.config.js` | Upgraded Cypress 3.3.1 → 13.x (3.3.1 requires `libgconf-2.so.4` which is removed in Ubuntu 22.04+); migrated config to Cypress 10+ format (`specPattern`, `blockHosts`, `setupNodeEvents`) |
| E9 | `server.js` | `secure: true` on session cookie blocked cookie transmission over HTTP — tests could never stay logged in; changed to `secure: process.env.NODE_ENV === "production"` |
| E10 | `artifacts/db-reset.js` | Seed data had plaintext passwords; `bcrypt.compareSync` threw "Not a valid BCrypt hash" — switched to pre-hashed values already in the file comments |
| E11 | `app/routes/index.js` | Rate limiter (100 req/15 min) triggered `429` on almost every Cypress spec — added `skip: () => NODE_ENV === "test"` so rate limiting stays active in production but is bypassed during tests |

---

## Notes
- `express-rate-limit` is imported as `RateLimit` (capital R) in `index.js` — keep consistent.
- `bcrypt-nodejs` is deprecated; consider migrating to `bcryptjs` or `bcrypt` in future.
- `marked 0.3.5` is pinned old; `sanitize: true` option was removed in later versions — do not upgrade without replacing the sanitization approach.
- HTTPS fix requires generating certs under `artifacts/cert/server.key` and `artifacts/cert/server.crt` before uncommenting the HTTPS block in `server.js`.
