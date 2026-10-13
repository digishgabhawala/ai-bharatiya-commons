# AI Bharatiyaa platform deployment plan

Status: implementation in progress. The parent web project, Task Queue path
migration, and LinkedIn path deployment are live on the temporary Vercel
hostname. The custom domain, parent-owned login, and multi-user authorization
remain future work.

This document describes how Task Queue and LinkedIn Content Agent can remain
independent codebases and deployments while appearing as one AI Bharatiyaa
product family:

```text
https://aibharatiya.com/
https://aibharatiya.com/queue
https://aibharatiya.com/linkedin
```

It records the smallest useful path toward that result. It is not a commitment
to build a general platform, component framework, or seamless multi-product
experience before a second product is ready for public use.

## Decision summary

1. Keep `task-queue` and `linkedin-content-agent` as separate repositories and
   independently deployable applications.
2. Use the separate `ai-bharatiya-web` runtime parent project. Do not turn
   `ai-bharatiya-commons` into the runtime gateway.
3. Let the parent project own `aibharatiya.com` and route product paths to the
   corresponding Vercel deployments.
4. Use the existing Supabase project as the first shared production backend:
   one Auth user pool, shared user IDs, and separate application schemas.
5. Use one human Supabase session across the common browser origin, but keep
   machine-to-machine credentials separate from human sessions.
6. Preserve direct service URLs for workers and backend integrations. The
   friendly path-based domain is primarily the human-facing surface.
7. Migrate incrementally: make both apps path-aware, protect LinkedIn data,
   then add the parent router. Do not combine repositories as a prerequisite.

## Target topology

```text
Browser
  |
  v
aibharatiya.com  (ai-bharatiya-web: shell, login, navigation, routing)
  |
  +-- /                      -> portfolio / product launcher
  +-- /login                 -> shared Supabase sign-in
  +-- /queue/*               -> Task Queue human UI
  +-- /linkedin/*            -> LinkedIn Content Agent frontend
  +-- /api/queue/*           -> Task Queue browser API
  +-- /api/linkedin/*        -> LinkedIn Content Agent backend API

Independent service traffic
  |
  +-- LinkedIn backend ------> Task Queue service URL + X-API-Key
  +-- Local/hosted workers --> Task Queue service URL + worker credentials

Shared Supabase project
  |
  +-- auth.users             -> common human identities
  +-- public.profiles        -> shared profile fields
  +-- public.app_memberships -> per-product access and role
  +-- linkedin.*             -> LinkedIn application data
  +-- task queue tables      -> current queue data; schema migration optional
  +-- Storage buckets        -> application-owned objects
```

The parent project can initially use Vercel rewrites as a lightweight reverse
proxy. Vercel Microfrontends remains an option if routing, preview coordination,
or independent product teams later justify the additional machinery.

## Public route contract

| Public path | Owner | Purpose |
| --- | --- | --- |
| `/` | Parent | AI Bharatiyaa portfolio and product launcher |
| `/login` | Parent | Common sign-in and sign-out |
| `/queue` and `/queue/*` | Task Queue | Human operations interface |
| `/linkedin` and `/linkedin/*` | LinkedIn frontend | Writing and illustration workflow |
| `/api/queue/*` | Task Queue backend | Browser-facing queue operations |
| `/api/linkedin/*` | LinkedIn backend | Browser-facing LinkedIn operations |

API namespaces are deliberately outside the product page paths. This avoids
collisions between static assets, SPA fallbacks, and backend routes.

Machine clients do not need to call through the parent domain. Initially they
should continue using the stable Task Queue deployment URL directly. A branded
service hostname can be introduced later without coupling worker availability
to the portfolio shell.

## Authentication and identity flow

```text
1. Browser opens /login.
2. Parent signs in against the shared Supabase project.
3. Supabase returns an access token and refresh token.
4. Apps under the aibharatiya.com origin reuse that session.
5. Browser sends the access token to /api/queue or /api/linkedin.
6. Each backend verifies the token and authorizes access to its own records.
```

All browser applications must use the same Supabase URL, publishable key, and
session-storage convention. The publishable key is intentionally browser-safe.
Database URLs, Supabase secret/service keys, task-queue service keys, and worker
credentials remain server-side deployment secrets.

Shared authentication does not imply shared authorization. A user can exist in
`auth.users` without being allowed into every product. `app_memberships` should
eventually record product access and role, for example:

| user_id | app | role |
| --- | --- | --- |
| Supabase UUID | `queue` | `admin` |
| Supabase UUID | `linkedin` | `member` |

For the current single-user phase, the existing Task Queue administrator
allow-list is sufficient. The membership model becomes necessary before
inviting other users.

## Current state

### Task Queue

- Deployed on Vercel and backed by the shared Supabase project.
- Supabase email/password authentication protects the admin identity and broad
  worker/task listing routes.
- A revocable `X-API-Key` mechanism exists for an application such as LinkedIn
  Content Agent to read worker status without borrowing a human session.
- The canonical suite entry point is `/queue`; `/admin` remains as a backwards-
  compatible direct-service route.
- Browser assets use `/queue/admin-assets/*` and browser API requests use
  `/api/queue/*`.
- The parent deployment at `ai-bharatiya-web.vercel.app` currently proxies
  `/queue/*` and `/api/queue/*` to the independent Task Queue deployment.
- Machine clients retain the stable direct-service `/api/*` contract.
- Task submission, task lookup, worker operations, and artifacts still use the
  MVP access model and are not ready for untrusted multi-user traffic.

### LinkedIn Content Agent

- Remains a local-first React/Vite and FastAPI application, but now also has a
  single-project Vercel deployment contract.
- The frontend and backend use the shared-domain paths `/linkedin/*` and
  `/api/linkedin/*`.
- Vite builds with a `/linkedin/` production base and FastAPI serves the built
  frontend, including deep-link fallbacks.
- The backend supports SQLite locally and already supports a dedicated
  `linkedin` schema in shared Supabase Postgres.
- Supabase email/password authentication and an allow-list protect hosted
  browser routes; multi-user record ownership is still pending.
- The parent deployment currently proxies `/linkedin/*` and
  `/api/linkedin/*` to the independent LinkedIn deployment.
- Posts, drafts, feedback, and scene assets are not scoped to a user.
- `characters.owner_id` exists but is nullable and is not yet enforced.
- `user_profile.md` is a single application-wide profile rather than a
  per-user record.
- The backend already knows how to call Task Queue with its own
  `TASK_QUEUE_API_KEY` for protected worker reads.

## Required Task Queue changes

### Required for path-based hosting

1. Introduce explicit settings for the browser-visible application and API
   bases, for example `APP_BASE_PATH=/queue` and
   `BROWSER_API_BASE=/api/queue`.
2. Replace hard-coded `/admin`, `/admin-assets/*`, and `/api/*` browser URLs
   with values derived from those settings.
3. Make `/queue` the public product entry point while retaining `/admin` on the
   direct service hostname during migration and rollback.
4. Ensure generated redirects, links, stylesheets, scripts, and fetch calls all
   work behind a reverse proxy without leaking the child deployment hostname.
5. Add tests for both direct-service mode and prefixed mode.

### Required before LinkedIn is public

1. Extend Task Queue service authentication beyond `GET /api/workers` to the
   producer operations LinkedIn uses: submit task and read its result.
2. Give each producer a revocable machine credential. Store only its hash in
   Task Queue; store the raw key only in the producer's deployment secrets.
3. Attach a producer identity and, where appropriate, the initiating user ID
   to each task.
4. Enforce that a producer can read only tasks and artifacts it owns.
5. Introduce worker enrollment or revocable worker credentials for register,
   heartbeat, claim, completion, failure, and artifact-upload operations.
6. Replace public artifact access with authorized delivery or short-lived
   signed URLs before artifacts contain private user content.

The admin allow-list can remain for operations staff. Human browser sessions
must not be copied into LinkedIn's backend or long-running workers.

## Required LinkedIn Content Agent changes

### Deployment foundation

1. Define production deployments for the Vite frontend and FastAPI backend.
   They may be two Vercel projects sourced from the same repository initially.
2. Configure Vite with a `/linkedin/` base so JavaScript, CSS, and image assets
   resolve correctly under the parent path.
3. Replace the fixed frontend `BASE = '/api'` with a build-time API base,
   using `/api/linkedin` in the shared-domain deployment.
4. Configure an SPA fallback for `/linkedin/*` routes.
5. Add explicit health checks and deployment documentation.
6. If previews use separate frontend and backend origins, configure CORS with
   an explicit preview allow-list. Production traffic through the parent
   domain should remain same-origin.

### Shared human authentication

1. Initialize the frontend with the same Supabase URL and publishable key as
   Task Queue and the future parent login.
2. Send the Supabase access token as `Authorization: Bearer` on every LinkedIn
   API request.
3. Add a backend authentication dependency that verifies the token and returns
   the stable Supabase user ID.
4. Return `401` for missing/invalid sessions and `403` for authenticated users
   without LinkedIn access.
5. Provide loading, signed-out, expired-session, forbidden, and identity-service
   failure states using the Commons UI guidance.

### Ownership and data migration

1. Add a non-null `owner_id` to `posts` and `scene_assets`.
2. Associate drafts and feedback with their post owner; add direct owner IDs
   only where they materially simplify authorization or cleanup.
3. Make `characters.owner_id` enforced for user-owned mascots, while allowing
   an explicitly shared system mascot if desired.
4. Backfill all existing rows to the current administrator's Supabase user UUID
   before making ownership non-null.
5. Scope every list, lookup, update, delete, retry, and generation operation by
   the authenticated owner. Looking up a record by ID alone is insufficient.
6. Add indexes for the common `(owner_id, created_at)` and ownership lookup
   paths.
7. Replace the single `user_profile.md` assumption with a per-user profile
   record before supporting multiple people. It can remain a seeded default
   during the single-user transition.

### Task Queue integration

1. Keep LinkedIn's backend-to-Task-Queue call server-side.
2. Use LinkedIn's raw `TASK_QUEUE_API_KEY`; never send it to the browser.
3. Include producer and user correlation metadata when submitting tasks.
4. Treat task results as untrusted until Task Queue confirms that they belong
   to the requesting producer/user.
5. Keep worker credentials entirely separate from both human sessions and the
   LinkedIn producer key.

## Parent project responsibilities

`ai-bharatiya-web` now exists and owns the temporary Vercel suite hostname. It
currently provides the portfolio launcher and routes both products. Its scope
should remain limited to the following:

- own the `aibharatiya.com` domain;
- render the portfolio/product launcher at `/`;
- provide shared sign-in/sign-out at `/login`;
- show a small, consistent suite header and product navigation;
- route `/queue`, `/linkedin`, and their browser API namespaces;
- provide a useful unavailable state when a child application is unhealthy;
- keep routing configuration small, explicit, and covered by smoke tests.

Do not place product business logic, application database models, worker code,
or deployment secrets in the parent. Do not make the parent a required hop for
machine-to-machine queue traffic.

`ai-bharatiya-commons` continues to own standards, tokens, architectural
contracts, and later genuinely reusable packages. It should not become the
deployed parent application.

## Environment-variable ownership

| Variable | Parent | Task Queue | LinkedIn frontend | LinkedIn backend |
| --- | --- | --- | --- | --- |
| Supabase URL | Publishable | Server + browser config | Publishable | Server |
| Supabase publishable key | Publishable | Browser config | Publishable | Token verification |
| Supabase secret/service key | No | Server secret | Never | Only if truly required |
| Database URL | No | Server secret | Never | Server secret |
| Task Queue producer key | No | Stores hash only | Never | Raw server secret |
| Worker credentials | No | Verifies them | Never | Never |
| Product route destinations | Server config | No | No | No |

Use separate Vercel Preview and Production values. A change to an environment
variable affects new deployments only, so redeploy before verification. Never
commit `.env`, `.env.local`, database credentials, service keys, or worker
credentials.

## Recommended delivery sequence

### Phase 1: secure LinkedIn data before hosting

- Add Supabase session handling to the frontend and backend.
- Add and backfill ownership columns.
- Scope every LinkedIn operation by owner.
- Protect the Task Queue producer routes LinkedIn needs.
- Add focused authorization and cross-user isolation tests.

### Phase 2: deploy LinkedIn independently

- Deploy its frontend and backend on their native Vercel URLs.
- Configure Preview secrets first.
- Verify the full brief-to-draft-to-image workflow against the hosted queue.
- Add Production secrets and verify again before public routing.

### Phase 3: make both products path-aware

- Add `/queue` support to Task Queue without removing direct `/admin` access.
- Add the `/linkedin/` Vite base and `/api/linkedin` client base.
- Test assets, refresh/deep links, authentication, and API errors under prefixes.

### Phase 4: introduce the parent domain

- Create and deploy `ai-bharatiya-web`.
- Attach `aibharatiya.com` to the parent project.
- Add rewrites for both products and APIs.
- Add the suite header and shared login entry point.
- Run production smoke tests before advertising the common URLs.

### Phase 5: improve, only after real use

- Add product memberships and roles.
- Move repeated authentication code into a small shared package after both apps
  validate the same contract.
- Consider Vercel Microfrontends if preview coordination or routing complexity
  outgrows simple rewrites.
- Add Google as another Supabase provider without changing application user IDs.
- Consider a branded Supabase API domain only if OAuth branding or portability
  justifies its cost.

## Minimum acceptance criteria

The first shared-domain release is ready when:

- `/queue` and `/linkedin` work on desktop and mobile, including hard refreshes;
- one Supabase login can be recognized by both applications;
- signed-out API calls return `401` without exposing application data;
- one user cannot read or mutate another user's LinkedIn records;
- LinkedIn can submit and read only its own queue tasks;
- worker credentials cannot be used as human or producer credentials;
- no secret appears in browser configuration, bundled JavaScript, Git, or logs;
- direct worker/producer traffic remains operational if the parent site fails;
- each child application can still be deployed and rolled back independently;
- the parent has automated route and health smoke tests.

## Risks and deliberate tradeoffs

- **Shared-origin blast radius:** JavaScript running under any product path is
  within the same browser origin. An XSS flaw in one product can threaten the
  shared session. Content security policy, dependency hygiene, output escaping,
  and review standards therefore apply to every child application.
- **Shared Supabase blast radius:** quotas, outages, and configuration changes
  affect all applications. This is acceptable for the portfolio/MVP stage but
  should be revisited for a higher-risk or independently scaled product.
- **Routing collisions:** absolute asset paths and generic `/api` routes collide
  unless every product owns a documented namespace.
- **Cross-product navigation:** independently deployed zones may perform a full
  page navigation. Consistent shell styling matters more initially than forcing
  SPA-style transitions between products.
- **Migration coupling:** shared database changes need explicit ownership and
  ordering. Shared identity migrations belong in a platform-owned location;
  product schema migrations remain with the product repository.

## Deferred decisions

- Final parent repository name and framework.
- Whether simple rewrites or Vercel Microfrontends should implement routing.
- Whether Task Queue tables should move from their current schema.
- Final role taxonomy beyond `queue:admin` and `linkedin:member`.
- Paid Supabase custom domain.
- Google authentication.
- A packaged shared UI or authentication SDK.

## References

- [Vercel rewrites](https://vercel.com/docs/routing/rewrites)
- [Vercel Microfrontends](https://vercel.com/docs/microfrontends/quickstart)
- [Next.js Multi-Zones](https://nextjs.org/docs/app/guides/multi-zones)
- [Supabase Auth sessions](https://supabase.com/docs/guides/auth/sessions)
- [Supabase custom schemas](https://supabase.com/docs/guides/api/using-custom-schemas)

