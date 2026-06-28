# LifeOS Architecture Recommendation

## Repository Analysis

Current state:

- Branch: `main`
- Remote: `origin` points to `https://github.com/Harshp110/lifeos.git`
- History: one initial commit
- Existing implementation: none
- Files present before architecture documentation: `README.md`, `.gitignore`

This is a greenfield repository. The architecture should optimize for production-grade foundations, fast iteration, strong privacy guarantees, and clear AI safety boundaries before feature code is written.

## Product Assumptions

LifeOS is an AI-powered personal operating system. The architecture should assume:

- User-owned personal data with high privacy expectations.
- AI workflows over notes, tasks, calendar events, documents, email, goals, habits, memories, and integrations.
- Long-running background work for ingestion, summarization, reminders, sync, embeddings, memory extraction, and automation.
- Multi-user SaaS readiness without prematurely building enterprise features.
- High trust requirements: data loss, incorrect automation, opaque memory, leaked secrets, or hallucinated actions would be product-breaking.

## First Implementation Scope

Build the first implementation around:

- Web app.
- Backend API.
- Background worker.
- PostgreSQL, Redis, and S3-compatible object storage.
- Core domain model.
- Memory Engine.
- Knowledge package.
- Decision Engine.
- Split AI packages: `ai-core`, `agents`, `prompts`, and `tools`.
- Plugin SDK for internal extension points.

Explicitly exclude from the first implementation:

- Mobile app.
- Terraform or full infrastructure-as-code.
- Billing and subscriptions.
- Dedicated advanced search infrastructure such as OpenSearch or Meilisearch.
- Third-party plugin marketplace.
- Independent microservices.

These exclusions keep the first production milestone focused on the operating system core rather than platform sprawl.

## Recommended Monorepo Architecture

Use a TypeScript-first monorepo with `pnpm` workspaces and Turborepo.

Recommended layout:

```text
LifeOS/
  apps/
    web/                 # Next.js frontend
    api/                 # Backend HTTP API
    worker/              # Background jobs and queues
  packages/
    ai-core/             # Model providers, streaming, parsing, cost tracking
    agents/              # Agent orchestration and task loops
    prompts/             # Prompt registry, versions, fixtures, eval inputs
    tools/               # Typed tool contracts and server-side tool executors
    memory-engine/       # Memory extraction, scoring, approval, retention
    knowledge/           # Knowledge graph, content chunks, citations, retrieval
    decision-engine/     # Policies, risk scoring, approvals, action decisions
    plugin-sdk/          # Plugin manifests, permissions, triggers, actions
    auth/                # Auth policies, session helpers, permission checks
    config/              # Shared typed config and environment validation
    database/            # Schema, migrations, seed scripts, data access
    domain/              # Core LifeOS domain types and business rules
    integrations/        # Google, Microsoft, email, calendar, storage adapters
    observability/       # Logging, tracing, metrics helpers
    queue/               # Queue contracts, job names, payload schemas
    security/            # Encryption, secret handling, audit helpers
    testing/             # Shared test factories, mocks, contract fixtures
    ui/                  # Shared design system components
  docs/
    architecture-recommendation.md
  tooling/
    eslint/
    prettier/
    typescript/
  infra/
    docker/              # Local development dependency definitions only
```

Why this shape:

- `apps` contains deployable units only.
- `packages` contains internal libraries with explicit ownership.
- AI is split by responsibility instead of becoming one large utility package.
- Memory, knowledge, and decisions are first-class product primitives.
- The Plugin SDK creates a controlled extension model without requiring a marketplace or remote plugin runtime.
- The repository can start as a modular monolith while preserving extraction paths later.

Avoid starting with microservices. LifeOS needs coherent domain modeling, reliable local development, and fast product learning more than independent service scaling in the first phase.

## Frontend Structure

Use `apps/web` with Next.js App Router, React, TypeScript, Tailwind CSS, and shared components from `packages/ui`.

Recommended frontend folders:

```text
apps/web/
  app/                   # Route segments, layouts, server components
  components/            # App-specific UI composition
  features/              # Product feature modules
  lib/                   # Web-only helpers
  styles/                # Global styles and Tailwind entry
  tests/                 # Frontend integration tests
```

Recommended feature modules:

- `inbox`: universal capture and triage.
- `today`: current plan, focus blocks, due tasks, reminders.
- `tasks`: tasks, projects, recurring routines, dependencies.
- `notes`: notes, documents, entities, backlinks.
- `calendar`: calendar view, scheduling, external sync.
- `command-center`: AI chat, command execution, and action approvals.
- `memory`: user-approved facts, preferences, corrections, and retrieval controls.
- `knowledge`: source objects, entities, citations, and relationship browsing.
- `decisions`: pending approvals, action rationale, policy outcomes, and run history.
- `automations`: user-visible rules, triggers, approvals, and run history.
- `plugins`: installed internal plugins, permissions, and health.
- `settings`: account, integrations, privacy, export, and security.

Frontend principles:

- Treat the first screen as the operating surface, not a marketing page.
- Make memory visible and editable. Users must understand what LifeOS believes about them.
- Make AI actions attributable to source data and policy decisions.
- Show approval requirements before sensitive actions run.
- Keep plugin permissions inspectable.
- Build auditability into the UI: users should be able to answer "why did LifeOS do this?"

## Backend Structure

Use `apps/api` as a modular Node.js backend. Recommended stack: Fastify, TypeScript, Zod for boundary validation, OpenAPI generation, and explicit service modules.

Fastify is the recommended first choice because it keeps the backend lean and explicit. NestJS remains a viable alternative if the team strongly prefers framework-level conventions, but the first implementation should not mix both.

Recommended backend modules:

```text
apps/api/
  src/
    modules/
      auth/
      users/
      workspaces/
      tasks/
      notes/
      calendar/
      conversations/
      memory/
      knowledge/
      decisions/
      automations/
      integrations/
      plugins/
      files/
      audit/
    middleware/
    routes/
    server.ts
```

Backend principles:

- Start as a modular monolith with clear module boundaries.
- Keep route handlers thin: validate, authorize, call application service, return response.
- Keep database access behind package-level repositories or query modules.
- Use one consistent authorization path for every user-scoped read/write.
- Emit domain events for important state changes.
- Use an outbox table for reliable event/job dispatch.
- Keep AI tool execution server-side only.
- Route sensitive action proposals through the Decision Engine.
- Treat integrations and plugins as untrusted IO: validate inputs, store sync cursors, retry idempotently, and audit side effects.

## Worker Structure

Use `apps/worker` for background jobs. Recommended queue: BullMQ with Redis initially.

Worker responsibilities:

- External data sync.
- File parsing and content normalization.
- Knowledge chunking and citation extraction.
- Embedding generation with `pgvector`.
- Memory candidate extraction and re-scoring.
- Summarization.
- Reminder scheduling.
- Decision and automation execution.
- Plugin trigger processing.
- Cleanup, retention, and export jobs.

Every job should have:

- A typed payload schema.
- Idempotency key.
- Retry policy.
- Dead-letter behavior.
- Structured logs.
- User/workspace context.
- Audit entry when user-visible state changes.

## AI Package Split

Do not create a single overloaded `packages/ai`. Split AI into four packages:

### `packages/ai-core`

Owns low-level model interaction:

- Provider adapters.
- Streaming and non-streaming completion APIs.
- Structured output parsing.
- Token and cost accounting.
- Model selection rules.
- Provider error normalization.

### `packages/prompts`

Owns prompt assets and evaluation inputs:

- Prompt templates.
- Prompt versions.
- Prompt metadata.
- Golden fixtures.
- Evaluation datasets.
- Regression expectations.

Prompts should be versioned and testable. Prompt changes that affect user-visible behavior should require eval updates.

### `packages/tools`

Owns typed tool contracts and executors:

- Tool schemas.
- Permission metadata.
- Input/output validation.
- Tool execution adapters.
- Audit metadata for tool calls.

Tools must call normal application services. They must not bypass authorization, validation, or audit logging.

### `packages/agents`

Owns agent orchestration:

- Agent definitions.
- Planning loops.
- Tool selection.
- Memory and knowledge retrieval coordination.
- Decision Engine handoff.
- Agent run state.

Agents may propose actions, but they do not directly mutate production data. Any sensitive action must pass through the Decision Engine and normal domain services.

## Memory Engine

Create `packages/memory-engine` as a first-class subsystem.

The Memory Engine owns how LifeOS forms, updates, forgets, and explains user-specific memory. It is not a generic vector search layer.

Memory types:

- Preference memory: user likes, dislikes, defaults, style, constraints.
- Semantic memory: durable facts about the user and their world.
- Episodic memory: time-bound events and interactions worth recalling.
- Procedural memory: user-approved ways LifeOS should perform recurring work.
- Working memory: short-lived context for the current session or task.

Memory lifecycle:

1. Source event or content enters the system.
2. Worker extracts memory candidates.
3. Candidate links back to source evidence in `packages/knowledge`.
4. Memory Engine scores confidence, sensitivity, freshness, and usefulness.
5. Decision Engine determines whether approval is required.
6. Approved memory is persisted with source links and revision history.
7. Retrieval uses memory with confidence and recency metadata.
8. Feedback, correction, or deletion updates the memory record.

Memory rules:

- Memory is derived data, not canonical truth.
- Every durable memory must have source evidence or explicit user entry.
- Sensitive memory requires user approval.
- Users must be able to inspect, correct, disable, or delete memory.
- Memory should decay or be revalidated when stale.
- AI responses should distinguish known facts from inferred preferences.

## Knowledge Package

Create `packages/knowledge` for the user's canonical knowledge layer.

The Knowledge package owns normalized, source-linked information:

- Source objects from notes, tasks, calendar events, files, and integrations.
- Content chunks.
- Embeddings.
- Entities.
- Entity links and relationships.
- Citations.
- Retrieval APIs.
- Knowledge freshness metadata.

Knowledge is different from memory:

- Knowledge stores what exists in the user's data.
- Memory stores what LifeOS has learned and may reuse about the user.
- Knowledge should be source-linked and mostly mechanical.
- Memory should be curated, scored, and user-controllable.

First implementation retrieval should use PostgreSQL full-text search plus `pgvector`. Do not add OpenSearch, Meilisearch, or other advanced search infrastructure in the first implementation.

## Decision Engine

Create `packages/decision-engine` as the policy and action gate.

The Decision Engine decides whether an AI, automation, plugin, or user command may proceed, needs approval, should be modified, or should be blocked.

Inputs:

- User/workspace context.
- Requested action.
- Tool or plugin identity.
- Data sensitivity.
- Confidence score.
- Memory confidence.
- Source evidence quality.
- User-configured trust settings.
- Historical failure signals.

Outputs:

- Allow.
- Require approval.
- Require clarification.
- Deny.
- Defer to human review.
- Attach explanation and audit metadata.

Responsibilities:

- Centralize approval policies.
- Classify action risk.
- Prevent AI and plugin bypasses.
- Provide user-visible rationale.
- Emit durable decision records for audit.
- Support dry-run decisions for automations.

The Decision Engine should be deterministic where possible. LLMs can provide inputs or summaries, but final policy decisions must be typed, inspectable, and testable.

## Plugin SDK

Create `packages/plugin-sdk` for controlled internal extensibility.

First implementation goals:

- Define plugin manifests.
- Define permission scopes.
- Define trigger, action, and data-source contracts.
- Define plugin health checks.
- Define plugin audit metadata.
- Support internal plugins for integrations and LifeOS-native extensions.

Do not build a third-party marketplace or arbitrary remote plugin runtime in the first implementation. The first Plugin SDK should make internal extension points clean and permissioned; external distribution can come later.

Plugin boundaries:

- Plugins do not access the database directly.
- Plugins call typed host APIs.
- Plugin actions pass through the Decision Engine.
- Plugin credentials are encrypted and scoped.
- Plugin runs are auditable and retry-safe.

## Database Architecture

Use PostgreSQL as the primary system of record. Add only the supporting stores needed for the first implementation:

- PostgreSQL: canonical relational data.
- `pgvector`: embeddings for first implementation retrieval.
- Redis: queues, rate limits, ephemeral cache.
- S3-compatible object storage: files and exports.

Recommended schema domains:

- Identity: `users`, `accounts`, `sessions`, `workspace_memberships`.
- Tenancy: `workspaces`, `workspace_settings`.
- Core work: `tasks`, `projects`, `task_events`, `recurrences`.
- Notes/docs: `notes`, `documents`, `document_versions`.
- Calendar: `calendars`, `calendar_events`, `availability_blocks`.
- Conversations: `conversations`, `messages`.
- AI runs: `ai_runs`, `agent_runs`, `tool_calls`, `prompt_versions`.
- Knowledge: `knowledge_sources`, `content_chunks`, `embeddings`, `entities`, `entity_links`, `citations`.
- Memory: `memory_records`, `memory_candidates`, `memory_sources`, `memory_feedback`, `memory_revisions`.
- Decisions: `decision_runs`, `decision_inputs`, `decision_outcomes`, `approval_policies`.
- Files: `files`, `file_versions`, `file_processing_jobs`.
- Integrations: `integration_accounts`, `sync_states`, `external_objects`.
- Plugins: `plugin_manifests`, `plugin_installations`, `plugin_permissions`, `plugin_runs`.
- Automations: `automation_rules`, `automation_runs`, `automation_approvals`.
- Audit: `audit_log`, `security_events`.
- Jobs/events: `outbox_events`, `inbox_events`.

Database rules:

- Every user-owned row must include `workspace_id` or a clear ownership path.
- Use UUID or ULID primary keys. Prefer sortable IDs for event-heavy tables.
- Use `created_at`, `updated_at`, and soft deletion where user recovery matters.
- Add row-level security only if the team is ready to test it thoroughly. Otherwise enforce tenancy in the application layer first and add RLS for defense in depth later.
- Encrypt sensitive tokens and secrets at the application layer before persistence.
- Keep raw integration payloads only when needed, and define retention windows.
- Store embeddings, summaries, and memory candidates as derived data that can be regenerated or invalidated.
- Use database migrations from day one.

Recommended ORM/query approach:

- Use Drizzle ORM for type-safe SQL and migrations if the team is comfortable staying close to SQL.
- Use Prisma if the team values broader familiarity and tooling more than SQL control.
- For LifeOS, Drizzle is the better long-term default because knowledge, embeddings, event tables, and integration sync benefit from explicit SQL.

## Docker Strategy

Use Docker for local dependencies first, then production packaging.

Local development:

- `docker-compose` should run Postgres, Redis, and object storage.
- Apps should run on the host during development for fast iteration.
- Seed data should be deterministic and safe to reset.
- Volumes should be named and documented.

Production:

- Build separate images for `web`, `api`, and `worker`.
- Use multi-stage builds.
- Run containers as non-root.
- Keep images minimal and deterministic.
- Inject secrets through the deployment platform, not baked files.
- Run migrations as a controlled release step, not implicitly on every app boot.

Initial local services:

```text
postgres
redis
minio
```

Initial production deployables:

```text
web
api
worker
```

Do not add Terraform in the first implementation. Document deployment steps manually or use the chosen platform's minimal configuration until the cloud target stabilizes.

## Testing Strategy

Testing should protect user trust, not just lines of code.

Recommended layers:

- Unit tests: domain logic, validation, permission checks, recurrence rules.
- Memory tests: extraction, scoring, approval requirements, correction, deletion, decay.
- Knowledge tests: chunking, source linking, citations, entity linking, retrieval ranking.
- Decision tests: risk classification, approval policy, denial policy, explanation output.
- Plugin SDK tests: manifest validation, permission scopes, trigger/action contracts.
- AI evals: prompt behavior, retrieval use, tool-call correctness, refusal/approval behavior.
- Integration tests: API routes, database queries, migrations, queue jobs.
- Contract tests: frontend/API contracts, webhook payloads, plugin contracts, AI tool schemas.
- End-to-end tests: critical user workflows in Playwright.
- Migration tests: apply/rollback where supported, seed compatibility, data preservation.
- Security tests: authorization matrix, token encryption, audit logging.
- Load smoke tests: ingestion, embeddings, memory extraction, queue throughput.

Critical first E2E workflows:

- Sign up/sign in.
- Create task, note, project, and calendar event.
- Ask AI to summarize current day with cited sources.
- Ask AI to create a task from a note with Decision Engine approval.
- Approve, edit, and delete a memory.
- Install or enable an internal plugin with scoped permissions.
- Process a background sync job.
- Export user data.

Testing tooling:

- Vitest for TypeScript packages.
- Playwright for browser E2E.
- Testcontainers or Docker-backed integration tests for Postgres/Redis.
- MSW or provider-specific mocks for external APIs.
- Dedicated eval fixtures for prompts, agents, tools, memory, and decisions.

## CI/CD Recommendation

Use GitHub Actions.

Required checks on every pull request:

- Install dependencies with frozen lockfile.
- Typecheck all packages.
- Lint.
- Format check.
- Unit tests.
- Integration tests for changed backend/database packages.
- AI, memory, knowledge, decision, and plugin contract tests when those packages change.
- Build deployable apps.
- Secret scanning.
- Dependency audit.

Recommended workflows:

- `pr.yml`: fast validation.
- `nightly.yml`: full integration, E2E, AI evals, memory evals, dependency audit.
- `release.yml`: build images, run migrations, deploy.
- `preview.yml`: deploy preview environment for frontend/API branches when platform support exists.

Branch strategy:

- Keep `main` releasable.
- Use short-lived feature branches.
- Require PR review and passing checks before merge.
- Use conventional commits or changesets once packages need versioning.

Deployment path:

- Phase 1: deploy web/API/worker to a managed platform with managed Postgres and Redis.
- Phase 2: add preview environments per PR.
- Phase 3: add infrastructure-as-code only after the deployment target and operational needs are stable.

## Coding Standards

Language and style:

- TypeScript strict mode everywhere.
- No implicit `any`.
- Runtime validation at every external boundary.
- Prefer named exports.
- Prefer small modules with explicit dependencies.
- Use path aliases sparingly and consistently.
- Avoid circular dependencies between packages.

Package dependency direction:

- `apps/*` may depend on `packages/*`.
- `agents` may depend on `ai-core`, `prompts`, `tools`, `knowledge`, `memory-engine`, and `decision-engine`.
- `tools` may depend on domain/application contracts, but tool executors must still call normal services.
- `memory-engine` may depend on `knowledge` for source evidence, but `knowledge` should not depend on `memory-engine`.
- `decision-engine` should be callable by agents, tools, automations, plugins, and API services.
- `plugin-sdk` should define contracts and host APIs, not import app internals.

API standards:

- All endpoints require explicit auth posture: public, authenticated, or service-only.
- All request and response payloads have schemas.
- All errors use a consistent typed error format.
- All user-visible mutations create audit records.
- All external side effects are idempotent.

Data standards:

- Every table has documented ownership and retention expectations.
- Every migration is reviewed.
- Every background job payload is versioned or backward compatible.
- All timestamps are stored in UTC.
- User timezone is stored separately and used only for presentation/scheduling logic.

Security standards:

- Encrypt OAuth tokens and other high-value secrets.
- Never log secrets, raw tokens, full sensitive documents, or raw private memory content unless explicitly required in a secure audit context.
- Use least-privilege integration and plugin scopes.
- Require approval for sensitive AI actions.
- Keep audit logs append-only.
- Support user data export and deletion early.

AI standards:

- Prompts are versioned.
- Agent behavior is tested with evals.
- Tool calls are typed and policy checked.
- Model outputs are parsed and validated.
- Retrieval sources are recorded.
- Memory usage is explainable.
- Decision outcomes are persisted.
- Cost, latency, and model choice are tracked.

## Observability

Add observability before the system becomes hard to debug.

Minimum baseline:

- Structured JSON logs.
- Request IDs and trace IDs.
- User/workspace context in logs where safe.
- OpenTelemetry instrumentation.
- Metrics for API latency, job throughput, queue depth, model latency, model cost, memory candidate volume, decision outcomes, integration failures, and sync lag.
- Error tracking with release/version tags.

User-facing observability:

- Automation run history.
- Plugin run history.
- Sync status per integration.
- AI action history.
- Memory history and source evidence.
- Decision rationale.
- Data export status.
- Clear failure messages and retry options.

## Security And Privacy Posture

LifeOS will handle unusually sensitive personal data. Security should be a product feature, not a cleanup task.

Early requirements:

- Strong authentication with passkeys or MFA-ready architecture.
- Workspace-scoped authorization from the first schema.
- Encrypted integration and plugin credentials.
- Audit logs for sensitive access and mutations.
- Data export and deletion.
- Explicit AI approval flows for external actions.
- User-visible memory controls.
- Separation of raw source data, normalized knowledge, derived summaries, and user-approved memories.
- Retention policy for raw imported content.

Later requirements:

- SOC 2 readiness.
- SSO for teams.
- Bring-your-own-key for advanced plans.
- Fine-grained integration permissions.
- External plugin marketplace review process if plugins become a platform surface.

## Key Risks

1. Building an AI chat shell before the data, knowledge, and memory models are trustworthy.
2. Letting AI, plugins, or automations mutate user data without Decision Engine approval and audit paths.
3. Treating memory as truth instead of derived, correctable, source-linked data.
4. Underestimating integration sync complexity.
5. Creating a Plugin SDK that bypasses authorization or data boundaries.
6. Over-engineering infrastructure before product-market fit.
7. Weak tenancy boundaries that become expensive to fix.
8. No eval framework for AI, memory, tool, and decision regressions.
9. Background jobs without idempotency.
10. Logging sensitive personal data during debugging.
11. Choosing too many databases too early.
12. Lack of visible user control over memory, decisions, plugins, and automation.

## Recommended First Milestone Architecture

The first production-shaped milestone should include:

- `apps/web`: authenticated web app with core shell.
- `apps/api`: modular backend with auth, core work objects, conversations, memory, knowledge, decisions, plugins, and audit.
- `apps/worker`: queue consumer for AI, memory, knowledge, plugins, and ingestion jobs.
- `packages/database`: Postgres schema and migrations.
- `packages/domain`: shared domain types and business rules.
- `packages/ai-core`: provider adapter, structured output, streaming, cost tracking.
- `packages/agents`: agent orchestration and run state.
- `packages/prompts`: prompt registry, versions, fixtures, eval inputs.
- `packages/tools`: tool contracts and server-side executors.
- `packages/memory-engine`: memory lifecycle and scoring.
- `packages/knowledge`: source-linked knowledge and retrieval.
- `packages/decision-engine`: approvals, risk policies, action decisions.
- `packages/plugin-sdk`: internal plugin contracts and permissions.
- `packages/config`: typed environment configuration.
- `packages/ui`: design system primitives.
- Postgres, Redis, and local object storage via Docker Compose.
- CI for typecheck, lint, tests, builds, and core evals.

This milestone should not include a mobile app, billing, Terraform, advanced search infrastructure, enterprise SSO, analytics warehouse, third-party plugin marketplace, or independent microservices unless a customer requirement forces a specific exception.

## Complete Implementation Plan

### Phase 0: Foundation

1. Confirm private alpha product scope.
2. Select stack decisions: Next.js, Fastify or NestJS, Drizzle or Prisma, auth provider, deployment target.
3. Create monorepo workspace structure.
4. Add TypeScript, linting, formatting, shared config, and package conventions.
5. Add Docker Compose for Postgres, Redis, and object storage.
6. Add CI skeleton with typecheck, lint, tests, and build.
7. Add package dependency rules for AI, memory, knowledge, decisions, and plugins.

Exit criteria:

- A new developer can clone, install, run local dependencies, and execute checks.
- Main branch is protected by CI.
- The first implementation scope explicitly excludes mobile, billing, Terraform, and advanced search infrastructure.

### Phase 1: Identity, Tenancy, And Core Data

1. Implement auth.
2. Create users, workspaces, memberships, and sessions.
3. Add authorization helpers.
4. Add audit log foundation.
5. Add tasks, notes, projects, tags, and calendar events.
6. Add database migrations and seed data.
7. Add frontend shell with inbox, today, tasks, notes, and calendar.

Exit criteria:

- A user can sign in and manage personal tasks/notes/calendar data in a workspace.
- All reads/writes are workspace-scoped.
- Mutations create audit events.

### Phase 2: Knowledge Layer

1. Create `packages/knowledge`.
2. Normalize source objects from notes, tasks, and calendar events.
3. Add content chunks, citations, entities, and entity links.
4. Add PostgreSQL full-text search and `pgvector` retrieval.
5. Add worker jobs for chunking, embedding, and re-indexing.
6. Add knowledge UI for source inspection and citations.

Exit criteria:

- LifeOS can retrieve source-linked context across core user data.
- AI responses can cite source objects without advanced search infrastructure.

### Phase 3: AI Package Split And Command Center

1. Create `packages/ai-core`.
2. Create `packages/prompts`.
3. Create `packages/tools`.
4. Create `packages/agents`.
5. Add conversations, messages, AI runs, agent runs, and tool calls.
6. Add typed model output parsing.
7. Add initial agent that can answer questions using knowledge retrieval.
8. Add baseline AI eval fixtures.

Exit criteria:

- A user can ask LifeOS questions about their data with cited answers.
- AI internals are separated into core, prompts, tools, and agents.

### Phase 4: Memory Engine

1. Create `packages/memory-engine`.
2. Add memory candidates, records, sources, feedback, and revisions.
3. Add worker jobs for memory candidate extraction.
4. Link memory candidates to Knowledge package source evidence.
5. Add memory scoring for confidence, sensitivity, freshness, and usefulness.
6. Add memory approval, correction, deletion, and disable flows.
7. Add memory eval fixtures.

Exit criteria:

- LifeOS can propose memories from user data.
- Users can approve, inspect, correct, and delete memory.
- Agents can use memory without treating it as canonical truth.

### Phase 5: Decision Engine

1. Create `packages/decision-engine`.
2. Add decision runs, inputs, outcomes, and approval policies.
3. Define risk classes for AI tools, automations, plugin actions, and memory writes.
4. Route sensitive AI tool proposals through the Decision Engine.
5. Add user-facing approval and rationale UI.
6. Add deterministic policy tests.

Exit criteria:

- Sensitive actions require approval or are denied according to testable policies.
- Users can understand why an action was allowed, blocked, or sent for approval.

### Phase 6: Plugin SDK And Integrations

1. Create `packages/plugin-sdk`.
2. Define plugin manifests, permission scopes, triggers, actions, and health checks.
3. Convert first integrations into internal plugins where appropriate.
4. Add encrypted plugin credential storage.
5. Route plugin actions through the Decision Engine.
6. Add plugin run history and audit metadata.

Exit criteria:

- Internal plugins can extend LifeOS through typed contracts.
- Plugin permissions and actions are inspectable and auditable.
- No third-party marketplace or arbitrary plugin runtime exists yet.

### Phase 7: Automations

1. Add automation rules, triggers, conditions, and actions.
2. Connect automations to Plugin SDK triggers and tool actions.
3. Add approval policies by action sensitivity.
4. Add dry-run previews.
5. Add automation run history.
6. Add rate limits and circuit breakers.
7. Add undo/recovery paths where feasible.

Exit criteria:

- Users can create controlled automations and understand exactly what ran.
- Sensitive automations require approval unless the user has configured trust.

### Phase 8: Production Hardening

1. Add preview environments when deployment platform support exists.
2. Add production monitoring, tracing, and alerting.
3. Add backup and restore drills.
4. Add export/delete account flows.
5. Add security review for auth, tokens, plugin credentials, memory, AI tools, and logging.
6. Add load smoke tests for sync, AI, memory extraction, decisions, plugins, and queues.
7. Add deployment runbooks.

Exit criteria:

- The system can support private beta users with operational confidence.
- The team can diagnose failures without reading raw sensitive data.

## Deferred Architecture

The following should remain deferred until there is clear product or operational pressure:

- Mobile app.
- Billing and subscriptions.
- Terraform or mature infrastructure-as-code.
- Dedicated advanced search service.
- Analytics warehouse.
- Enterprise SSO.
- External plugin marketplace.
- Independent microservices.

## Approval Gate Before Code

No application code should be written until the team approves or changes these decisions:

- Monorepo tooling.
- Frontend framework.
- Backend framework.
- ORM/query layer.
- Auth approach.
- Initial database schema boundaries.
- Memory Engine behavior.
- Knowledge package scope.
- Decision Engine approval policy.
- AI package split.
- Plugin SDK scope.
- Docker/local development strategy.
- First private alpha product scope.

