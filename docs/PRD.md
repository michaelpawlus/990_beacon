# 990 Beacon — Product Requirements Document

**Version:** 1.0
**Author:** Michael Pawlus
**Date:** February 22, 2026
**Status:** Draft

---

## Table of Contents

1. [Vision & Problem Statement](#1-vision--problem-statement)
2. [Target Users & Personas](#2-target-users--personas)
3. [Market Context](#3-market-context)
4. [Product Overview](#4-product-overview)
5. [Data Sources & Pipeline](#5-data-sources--pipeline)
6. [Architecture & Tech Stack](#6-architecture--tech-stack)
7. [Phased Roadmap](#7-phased-roadmap)
8. [Phase 1: Foundation (Detailed)](#8-phase-1-foundation-detailed)
9. [Phase 2: Core Product](#9-phase-2-core-product)
10. [Phase 3: Intelligence Layer](#10-phase-3-intelligence-layer)
11. [Phase 4: Monetization](#11-phase-4-monetization)
12. [Phase 5: Collaboration & Alerts](#12-phase-5-collaboration--alerts)
13. [Phase 6: API & Scale](#13-phase-6-api--scale)
14. [Phase 7: Marketing & Launch](#14-phase-7-marketing--launch)
15. [Pricing Strategy](#15-pricing-strategy)
16. [Success Metrics](#16-success-metrics)
17. [Risk Register](#17-risk-register)
18. [Logging & Learning Protocol](#18-logging--learning-protocol)

---

## 1. Vision & Problem Statement

### Vision

990 Beacon is a subscription intelligence platform that transforms raw IRS 990 nonprofit filing data into actionable insights for fundraisers, prospect researchers, grant writers, and nonprofit consultants. It combines structured financial data with AI-powered analysis to answer questions that existing tools make tedious or impossible.

### The Problem

Prospect researchers and fundraisers need to understand nonprofit organizations — their financial health, leadership compensation, grant-making patterns, growth trajectories, and peer comparisons. Today, this requires:

- Manually downloading 990 filings from the IRS or ProPublica
- Reading dense XML or PDF documents page by page
- Building one-off spreadsheets to compare organizations
- Repeating this work every filing cycle with no memory of prior research
- Having no way to monitor changes over time without manual re-checking

The IRS publishes this data freely, but the gap between "publicly available" and "actually usable" is enormous. Existing tools like GuideStar/Candid require expensive institutional subscriptions and offer limited analytical depth. ProPublica's Nonprofit Explorer is free but provides no alerting, no AI analysis, no saved research, and no team collaboration.

### Why Now

Three converging trends make this the right moment:

1. The IRS 990 e-file dataset on AWS is now comprehensive and machine-readable (XML), covering 2013-present with millions of filings.
2. LLMs can now generate useful narrative summaries of financial data that were previously only possible from human analysts.
3. The advancement/fundraising industry is actively seeking AI-powered tools but most vendors are bolting AI onto legacy platforms rather than building AI-native products.

### Why Michael

This isn't a cold start. Michael has built IRS 990 lookup tools three separate times (irs990lookup, lookup990, irs990_lookup in R), built fundraising analytics packages, spent years in prospect research and advancement data science, and currently leads AI implementation for a major university's fundraising operation. The domain expertise is deep and genuine — this product would be built by someone who has been the target user.

---

## 2. Target Users & Personas

### Primary Personas

**Persona 1: Sarah — Senior Prospect Researcher**
- Works at a large university advancement office (team of 5-15 researchers)
- Spends 30% of her week manually reviewing 990s to profile foundation prospects
- Currently uses GuideStar ($3,000/yr institutional license) + manual spreadsheets
- Pain: "I need to know if this foundation is growing, shrinking, or about to sunset — and I need that answer in 5 minutes, not 2 hours."
- Willingness to pay: $50-150/month for a tool that saves her 8+ hours/week

**Persona 2: David — Independent Nonprofit Consultant**
- Runs a solo consulting practice advising nonprofits on fundraising strategy
- Needs to quickly benchmark a client against peer organizations
- Currently pieces together data from ProPublica, Charity Navigator, and manual research
- Pain: "When a client asks 'how do we compare to similar orgs?' I spend an entire day building that analysis from scratch every time."
- Willingness to pay: $30-80/month; needs to see ROI quickly

**Persona 3: Maria — Grant Writer**
- Writes grants for a mid-size nonprofit; submits 20-40 applications per year
- Needs to research funders: what they fund, how much, typical grant size, geographic focus
- Currently relies on Foundation Directory Online ($200/month) and manual 990 review
- Pain: "I waste hours reading 990s to figure out if a foundation even funds work like ours."
- Willingness to pay: $40-100/month if it meaningfully increases grant win rate

**Persona 4: James — VP of Advancement**
- Executive at a mid-size university; oversees a team of fundraisers and researchers
- Needs portfolio-level views: which prospects are worth pursuing, where are the opportunities
- Currently relies on his research team's manual work and expensive vendor tools
- Pain: "I need a dashboard that tells me which foundations in our pipeline have the capacity and inclination to give — and alerts me when something changes."
- Willingness to pay: $200-500/month for a team plan

### Secondary Personas

- **Journalists** investigating nonprofit finances
- **Nonprofit board members** benchmarking their own organization
- **Wealth advisors** understanding a client's philanthropic landscape
- **Academic researchers** studying the nonprofit sector

---

## 3. Market Context

### Competitive Landscape

| Competitor | Strengths | Weaknesses | Pricing |
|---|---|---|---|
| GuideStar/Candid | Comprehensive data, industry standard | Expensive, clunky UI, no AI | $3,000-10,000/yr institutional |
| Foundation Directory Online | Deep funder data | Expensive, focused on funders only | $200/mo+ |
| ProPublica Nonprofit Explorer | Free, good coverage | No analysis, no alerts, no saved research | Free |
| Charity Navigator | Good ratings | Consumer-focused, limited depth | Free / donation |
| Open990 | Open source 990 data | Technical, no product UX | Free |

### 990 Beacon's Positioning

990 Beacon sits in the gap between "free but unusable" (ProPublica) and "comprehensive but expensive" (Candid). It targets the professional user who needs more than a search engine but isn't at an institution that can afford five-figure annual licenses. The AI layer is the differentiator: no existing tool provides LLM-generated narrative analysis, automated benchmarking, or natural-language querying of 990 data.

---

## 4. Product Overview

### Core Capabilities

**Search & Explore** — Full-text and structured search across all e-filed 990s. Filter by geography, NTEE code, revenue range, asset size, filing year. Typeahead autocomplete. Saved searches.

**Organization Profiles** — A single-page view for any nonprofit that consolidates all available 990 data into a readable profile: mission, financials over time, key people, top compensation, program expenses, and related organizations.

**Financial Health Scoring** — An algorithmic score (1-100) based on financial indicators: revenue diversity, operating reserves, fundraising efficiency, program expense ratio, revenue growth trend, and working capital. Benchmarked against NTEE peer group.

**AI Summaries** — LLM-generated narrative summaries for each organization: "what does this org do, is it healthy, what's changed recently, and what should I know before approaching them?" Updated with each new filing.

**Benchmarking** — Side-by-side comparison of 2-5 organizations across key metrics. Percentile rankings within NTEE category and revenue cohort.

**Watchlists & Alerts** — Save organizations to watchlists. Get email alerts when new filings are processed, when key metrics change beyond a threshold, or when leadership changes are detected.

**Team Workspaces** — Shared watchlists, research notes, and saved searches within an organization account. Activity feed showing team research activity.

**Export & Reporting** — Export organization profiles, comparisons, and watchlist summaries as PDF, CSV, or formatted reports. Scheduled report delivery via email.

**API Access** — RESTful API for programmatic access to organization data, scores, and search. Metered by request volume.

---

## 5. Data Sources & Pipeline

### Primary: IRS 990 E-File Data

The IRS publishes electronically filed 990 returns as XML on AWS S3. This is the authoritative source.

- **Location:** `s3://irs-form-990/` (public bucket)
- **Coverage:** Tax years 2013-present
- **Volume:** ~3 million filings, growing ~300K/year
- **Format:** XML (one file per filing)
- **Update frequency:** Weekly (new filings added as processed)
- **Index:** Annual index CSV files listing all available filings with EIN, organization name, filing date, and S3 object key

**Data extracted per filing:**
- EIN, organization name, address, state, NTEE code
- Filing type (990, 990-EZ, 990-PF)
- Tax year, filing date
- Total revenue, total expenses, net assets
- Program service revenue, contributions/grants, investment income
- Program expenses, management expenses, fundraising expenses
- Compensation of officers/directors/key employees (name, title, compensation)
- Top 5 highest compensated employees
- Mission/activity description
- Related organizations
- For 990-PF: grants paid (recipient name, amount, purpose)

### Secondary Sources (Future Phases)

- **IRS BMF (Business Master File):** Basic registration data for all tax-exempt organizations (EIN, name, ruling date, NTEE code, asset/income ranges). Useful for orgs that haven't e-filed.
- **Charity Navigator Ratings:** Public ratings data (if available via API or scraping).
- **State charity registration databases:** Additional compliance data.
- **News/web signals:** Leadership changes, major gifts, program announcements (Phase 6+).

### Data Pipeline Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌────────────┐
│  IRS S3     │────▶│  Ingestion   │────▶│  Transform  │────▶│  Postgres  │
│  (XML)      │     │  Worker      │     │  & Score    │     │  (Primary) │
└─────────────┘     └──────────────┘     └─────────────┘     └────────────┘
                                                                    │
                                                              ┌─────▼──────┐
                                                              │  Search    │
                                                              │  Index     │
                                                              │ (Postgres  │
                                                              │  FTS/      │
                                                              │  pgvector) │
                                                              └────────────┘
```

**Ingestion cadence:**
- Full historical load: one-time batch job processing all ~3M filings
- Incremental: weekly job checking IRS index for new filings
- Processing rate target: ~1,000 filings/minute (XML parse + insert)

---

## 6. Architecture & Tech Stack

### System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │ Marketing│  │ App Shell│  │ Search   │  │ Org Profile   │   │
│  │ Pages    │  │ + Auth   │  │ UI       │  │ Dashboard     │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │ Compare  │  │ Watch-   │  │ Settings │  │ Admin Panel   │   │
│  │ View     │  │ lists    │  │ /Billing │  │ (Team mgmt)   │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘   │
└───────────────────────────┬──────────────────────────────────────┘
                            │ HTTPS
┌───────────────────────────▼──────────────────────────────────────┐
│                      API LAYER (FastAPI)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │ Auth     │  │ Search   │  │ Org      │  │ Scoring       │   │
│  │ Routes   │  │ Routes   │  │ Routes   │  │ Routes        │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │ Watch-   │  │ Export   │  │ AI       │  │ Billing/      │   │
│  │ list API │  │ Routes   │  │ Routes   │  │ Usage API     │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘   │
└───────────────────────────┬──────────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│                      DATA LAYER                                   │
│  ┌─────────────────┐  ┌────────────────┐  ┌─────────────────┐   │
│  │ PostgreSQL      │  │ Redis          │  │ S3/Blob        │   │
│  │ (Supabase)      │  │ (Cache/Queue)  │  │ (Exports/PDFs) │   │
│  │ - Org data      │  │ - Search cache │  │                 │   │
│  │ - User data     │  │ - Rate limits  │  │                 │   │
│  │ - FTS index     │  │ - Job queue    │  │                 │   │
│  │ - Auth (RLS)    │  │                │  │                 │   │
│  └─────────────────┘  └────────────────┘  └─────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│                   BACKGROUND WORKERS                              │
│  ┌─────────────────┐  ┌────────────────┐  ┌─────────────────┐   │
│  │ 990 Ingestion   │  │ AI Summary     │  │ Alert/Email     │   │
│  │ Pipeline        │  │ Generator      │  │ Worker          │   │
│  └─────────────────┘  └────────────────┘  └─────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### Tech Stack Decisions

| Layer | Technology | Rationale |
|---|---|---|
| **Frontend** | Next.js 14+ (App Router), TypeScript, Tailwind CSS, shadcn/ui | Michael has Next.js experience (homeowner-dashboard). App Router gives SSR for marketing pages + client components for the app. shadcn/ui avoids building a design system from scratch. |
| **Auth** | Clerk | Handles auth, org/team management, RBAC, and user management UI out of the box. Reduces weeks of auth plumbing to hours. Free tier covers development and early users. |
| **API** | Python, FastAPI | Michael's strongest language. FastAPI gives automatic OpenAPI docs (useful for the eventual public API), async support, and Pydantic validation. |
| **Database** | PostgreSQL via Supabase | Postgres full-text search avoids a separate search engine for MVP. Supabase gives managed Postgres + Row Level Security + realtime + storage. Can migrate to raw Postgres later if needed. |
| **Cache/Queue** | Redis (Upstash) | Serverless Redis for search caching, rate limiting, and lightweight job queuing. Upstash has a generous free tier. |
| **AI/LLM** | Anthropic Claude API | Michael's deep familiarity. Sonnet for summaries (cost-effective), Haiku for classification tasks. |
| **Payments** | Stripe | Industry standard. Checkout, subscriptions, customer portal, usage-based billing, invoicing. |
| **Email** | Resend | Simple API, good deliverability, React email templates. Free tier covers early growth. |
| **Hosting (Frontend)** | Vercel | Native Next.js support, preview deployments, edge functions. Free tier for development. |
| **Hosting (API)** | Railway | Simple Python deployment, managed Postgres option as backup, good DX. ~$5/month to start. |
| **CI/CD** | GitHub Actions | Already on GitHub. Free for public repos. |
| **Monitoring** | Sentry (errors), PostHog (product analytics) | Both have generous free tiers. Sentry catches runtime errors; PostHog tracks feature usage. |
| **File Storage** | Supabase Storage or Cloudflare R2 | For generated PDF exports and cached reports. |

---

## 7. Phased Roadmap

### Overview

```
Phase 1: Foundation          ██████░░░░░░░░░░░░░░  Weeks 1-3
Phase 2: Core Product        ░░░░░░██████░░░░░░░░  Weeks 4-7
Phase 3: Intelligence Layer  ░░░░░░░░░░░░████░░░░  Weeks 8-10
Phase 4: Monetization        ░░░░░░░░░░░░░░░░██░░  Weeks 11-12
Phase 5: Collaboration       ░░░░░░░░░░░░░░░░░░██  Weeks 13-15
Phase 6: API & Scale         ░░░░░░░░░░░░░░░░░░░░  Weeks 16-18
Phase 7: Marketing & Launch  ░░░░░░░░░░░░░░░░░░░░  Weeks 19-20
```

### Phase Dependencies

```
Phase 1 (Foundation)
    └──▶ Phase 2 (Core Product)
              ├──▶ Phase 3 (Intelligence)
              │         └──▶ Phase 5 (Collaboration & Alerts)
              └──▶ Phase 4 (Monetization)
                            └──▶ Phase 6 (API & Scale)
                                       └──▶ Phase 7 (Launch)
```

### Exit Criteria Per Phase

Each phase has defined exit criteria. A phase is complete when all exit criteria pass and all tests are green. Phases are logged in `CHANGELOG.md` with what was done and why. Lessons learned are logged in `CLAUDE.md`.

---

## 8. Phase 1: Foundation (Detailed)

### Goal

Stand up the project skeleton with authenticated users who can log in, see a dashboard, and have their session managed properly. Establish the development workflow, testing patterns, CI/CD pipeline, and database schema foundations. No 990 data yet — this phase is pure infrastructure.

### Why This Comes First

Every subsequent phase depends on having a working auth system, database, API, and deployment pipeline. Building this first means Phase 2+ can focus entirely on product features without fighting infrastructure issues. It also forces decisions about project structure that are painful to change later.

### Step-by-Step Build Plan

Each step below ends with tests that must pass before proceeding to the next step.

---

#### Step 1.1: Repository Setup & Project Structure

**What:** Initialize the monorepo with frontend and backend projects, linting, formatting, and Git configuration.

**Actions:**
```
990-beacon/
├── .github/
│   └── workflows/
│       ├── frontend-ci.yml
│       └── backend-ci.yml
├── frontend/               # Next.js app
│   ├── src/
│   │   ├── app/            # App Router pages
│   │   ├── components/     # Shared components
│   │   ├── lib/            # Utilities, API client
│   │   └── styles/         # Global styles
│   ├── __tests__/          # Frontend tests
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── package.json
├── backend/                # FastAPI app
│   ├── app/
│   │   ├── api/            # Route modules
│   │   ├── core/           # Config, security, dependencies
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app entry
│   ├── tests/              # Backend tests
│   ├── alembic/            # DB migrations
│   ├── alembic.ini
│   ├── requirements.txt
│   └── pyproject.toml
├── docs/                   # Documentation
│   └── PRD.md
├── CLAUDE.md               # Lessons learned & skills log
├── CHANGELOG.md            # Phase completion log
├── README.md
└── docker-compose.yml      # Local dev (Postgres + Redis)
```

**Tests after this step:**
- [ ] `cd frontend && npm run build` completes without errors
- [ ] `cd frontend && npm run lint` passes
- [ ] `cd backend && python -m pytest` runs (even with 0 tests) without errors
- [ ] `docker-compose up -d` starts Postgres and Redis containers
- [ ] Backend can connect to local Postgres: `python -c "from app.core.config import settings; print(settings.DATABASE_URL)"`

---

#### Step 1.2: Database Schema & Migrations

**What:** Define the core database tables for organizations, filings, users, and watchlists. Set up Alembic for migration management.

**Schema (initial):**

```sql
-- Core 990 data tables
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ein VARCHAR(10) NOT NULL UNIQUE,
    name TEXT NOT NULL,
    city TEXT,
    state VARCHAR(2),
    ntee_code VARCHAR(10),
    ruling_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_org_ein ON organizations(ein);
CREATE INDEX idx_org_state ON organizations(state);
CREATE INDEX idx_org_ntee ON organizations(ntee_code);
CREATE INDEX idx_org_name_trgm ON organizations USING gin(name gin_trgm_ops);

CREATE TABLE filings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    object_id VARCHAR(50) NOT NULL UNIQUE,  -- IRS S3 object key
    tax_year INTEGER NOT NULL,
    filing_type VARCHAR(10) NOT NULL,       -- 990, 990EZ, 990PF
    filing_date DATE,
    total_revenue BIGINT,
    total_expenses BIGINT,
    net_assets BIGINT,
    contributions_and_grants BIGINT,
    program_service_revenue BIGINT,
    investment_income BIGINT,
    program_expenses BIGINT,
    management_expenses BIGINT,
    fundraising_expenses BIGINT,
    num_employees INTEGER,
    num_volunteers INTEGER,
    mission_description TEXT,
    raw_xml_url TEXT,                        -- S3 URL for original XML
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_filing_org ON filings(organization_id);
CREATE INDEX idx_filing_year ON filings(tax_year);
CREATE INDEX idx_filing_type ON filings(filing_type);

CREATE TABLE filing_people (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filing_id UUID NOT NULL REFERENCES filings(id),
    name TEXT NOT NULL,
    title TEXT,
    compensation BIGINT,
    is_officer BOOLEAN DEFAULT FALSE,
    is_director BOOLEAN DEFAULT FALSE,
    is_key_employee BOOLEAN DEFAULT FALSE,
    is_highest_compensated BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_people_filing ON filing_people(filing_id);

CREATE TABLE filing_grants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filing_id UUID NOT NULL REFERENCES filings(id),
    recipient_name TEXT NOT NULL,
    recipient_ein VARCHAR(10),
    recipient_city TEXT,
    recipient_state VARCHAR(2),
    amount BIGINT,
    purpose TEXT
);

CREATE INDEX idx_grants_filing ON filing_grants(filing_id);

-- User & workspace tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clerk_id VARCHAR(100) NOT NULL UNIQUE,
    email TEXT NOT NULL,
    full_name TEXT,
    plan_tier VARCHAR(20) DEFAULT 'free',     -- free, pro, team
    stripe_customer_id VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    clerk_org_id VARCHAR(100) UNIQUE,
    owner_id UUID NOT NULL REFERENCES users(id),
    plan_tier VARCHAR(20) DEFAULT 'free',
    stripe_subscription_id VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE team_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES teams(id),
    user_id UUID NOT NULL REFERENCES users(id),
    role VARCHAR(20) DEFAULT 'member',        -- owner, admin, member
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(team_id, user_id)
);

CREATE TABLE watchlists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    team_id UUID REFERENCES teams(id),        -- NULL = personal
    is_shared BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE watchlist_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    watchlist_id UUID NOT NULL REFERENCES watchlists(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id),
    notes TEXT,
    added_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(watchlist_id, organization_id)
);

-- Search & activity tables
CREATE TABLE saved_searches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    name TEXT NOT NULL,
    query_params JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE usage_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    event_type VARCHAR(50) NOT NULL,          -- search, profile_view, export, api_call
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_usage_user_date ON usage_events(user_id, created_at);

-- AI-generated content
CREATE TABLE org_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    filing_id UUID REFERENCES filings(id),    -- summary generated from this filing
    summary_text TEXT NOT NULL,
    model_version VARCHAR(50),
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE org_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    filing_id UUID NOT NULL REFERENCES filings(id),
    overall_score INTEGER NOT NULL,           -- 1-100
    revenue_diversity_score INTEGER,
    operating_reserves_score INTEGER,
    fundraising_efficiency_score INTEGER,
    program_expense_ratio_score INTEGER,
    revenue_growth_score INTEGER,
    working_capital_score INTEGER,
    peer_percentile INTEGER,                  -- percentile within NTEE group
    scored_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Tests after this step:**
- [ ] `alembic upgrade head` runs successfully against local Postgres
- [ ] `alembic downgrade base` rolls back cleanly
- [ ] `alembic upgrade head` again succeeds (round-trip)
- [ ] All indexes exist: `SELECT indexname FROM pg_indexes WHERE tablename IN ('organizations', 'filings');`
- [ ] Trigram extension installed: `SELECT * FROM pg_extension WHERE extname = 'pg_trgm';`
- [ ] Can insert and query a sample organization and filing

---

#### Step 1.3: Backend API Skeleton

**What:** Set up the FastAPI application with health check, CORS, error handling, and the first route module (auth webhook receiver for Clerk).

**Key files:**
- `backend/app/main.py` — App factory, middleware, CORS
- `backend/app/core/config.py` — Pydantic Settings (env vars)
- `backend/app/core/database.py` — SQLAlchemy async engine + session
- `backend/app/core/deps.py` — Dependency injection (DB session, current user)
- `backend/app/api/health.py` — Health check endpoint
- `backend/app/api/webhooks.py` — Clerk webhook handler (user.created, user.updated)

**API Endpoints (Phase 1):**

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | `/health` | Health check (DB connectivity) | None |
| GET | `/api/v1/me` | Current user profile | Required |
| POST | `/api/v1/webhooks/clerk` | Clerk webhook receiver | Webhook secret |

**Tests after this step:**
- [ ] `GET /health` returns `{"status": "ok", "db": "connected"}`
- [ ] `GET /api/v1/me` without auth returns 401
- [ ] `GET /api/v1/me` with valid Clerk JWT returns user data
- [ ] Clerk webhook with valid signature creates user in DB
- [ ] Clerk webhook with invalid signature returns 401
- [ ] CORS allows requests from `http://localhost:3000`
- [ ] OpenAPI docs accessible at `/docs`

---

#### Step 1.4: Frontend Shell & Auth Integration

**What:** Set up the Next.js app with Clerk authentication, a layout with sidebar navigation, and protected routes.

**Pages:**
- `/` — Marketing landing page (public)
- `/sign-in` — Clerk sign-in (public)
- `/sign-up` — Clerk sign-up (public)
- `/dashboard` — Authenticated home (protected)
- `/dashboard/search` — Placeholder (protected)
- `/dashboard/watchlists` — Placeholder (protected)
- `/dashboard/settings` — Placeholder (protected)

**Components:**
- `AppShell` — Sidebar + header + main content area
- `Sidebar` — Navigation links
- `UserMenu` — Clerk user button with sign-out

**Tests after this step:**
- [ ] `/` renders the landing page without authentication
- [ ] `/dashboard` redirects to `/sign-in` when not authenticated
- [ ] After sign-in, user lands on `/dashboard`
- [ ] Sign-out returns user to `/`
- [ ] Sidebar navigation between dashboard pages works
- [ ] New sign-up triggers Clerk webhook, user appears in DB
- [ ] Mobile responsive: sidebar collapses on small screens
- [ ] Lighthouse accessibility score > 90 on landing page

---

#### Step 1.5: Frontend-Backend Integration

**What:** Connect the frontend to the backend API. The dashboard page calls `GET /api/v1/me` and displays the user's profile info, confirming the full auth flow works end-to-end.

**Implementation:**
- API client module (`frontend/src/lib/api.ts`) with base URL config, auth header injection (Clerk JWT), and error handling
- Dashboard page fetches and displays user info from backend
- Environment-based API URL (`NEXT_PUBLIC_API_URL`)

**Tests after this step:**
- [ ] Dashboard page shows user's name and email from backend (not Clerk client-side)
- [ ] API client automatically attaches Clerk JWT to requests
- [ ] API client handles 401 by redirecting to sign-in
- [ ] API client handles network errors gracefully (shows error state, not crash)
- [ ] Works in both development (localhost) and production (deployed) configurations

---

#### Step 1.6: CI/CD Pipeline

**What:** Set up GitHub Actions for automated testing and deployment.

**Workflows:**
- **frontend-ci.yml:** On push/PR to main — install, lint, type-check, test, build
- **backend-ci.yml:** On push/PR to main — install, lint, type-check (mypy), test (with test DB)
- **deploy-frontend.yml:** On push to main — deploy to Vercel
- **deploy-backend.yml:** On push to main — deploy to Railway

**Tests after this step:**
- [ ] Push to a feature branch triggers CI for both frontend and backend
- [ ] CI fails if any test fails (blocking merge)
- [ ] CI fails if linting fails
- [ ] Merge to main triggers deployment
- [ ] Deployed frontend can reach deployed backend
- [ ] Health check passes on deployed backend

---

#### Step 1.7: Local Development Experience

**What:** Ensure a new developer (or future-you) can clone the repo and be running in under 5 minutes.

**Implementation:**
- `docker-compose.yml` for Postgres + Redis
- `Makefile` with commands: `make setup`, `make dev`, `make test`, `make lint`, `make migrate`
- `.env.example` files for both frontend and backend
- `README.md` with quickstart guide
- Seed script that creates a test user and a handful of sample organizations

**Tests after this step:**
- [ ] Fresh clone → `make setup` → `make dev` starts both frontend and backend
- [ ] `make test` runs all tests and reports results
- [ ] `.env.example` files document all required environment variables
- [ ] README quickstart is accurate and complete (test by following it literally)

---

### Phase 1 Exit Criteria

All of the following must be true:

1. A user can visit the site, sign up, and see a personalized dashboard
2. The backend correctly stores user records via Clerk webhooks
3. The frontend authenticates API requests using Clerk JWTs
4. All tests pass in CI
5. The app is deployed and accessible at a public URL
6. A new developer can set up the project locally in under 5 minutes
7. `CHANGELOG.md` has a Phase 1 entry documenting what was built and why
8. `CLAUDE.md` has any lessons learned logged

### Phase 1 Deliverables

- Working monorepo with frontend + backend
- Auth system (sign up, sign in, sign out, session management)
- Database with migrations
- CI/CD pipeline
- Deployed to staging environment
- README with quickstart
- CHANGELOG entry
- CLAUDE.md initialized

---

## 9. Phase 2: Core Product

### Goal

Users can search for nonprofit organizations, view detailed organization profiles with financial data, and the system has real 990 data powering it.

### Steps

**Step 2.1: IRS 990 Data Ingestion Pipeline**
- Build a Python script that downloads IRS index files and identifies new filings
- XML parser that extracts all fields defined in the schema
- Batch processor that handles the full historical dataset (~3M filings)
- Incremental processor for weekly updates
- Error handling for malformed/incomplete XML (this will be ~5-10% of filings)
- Tests: Parse 100 sample XMLs of each type (990, 990-EZ, 990-PF), verify field extraction accuracy > 95%, pipeline recovers from failures without re-processing completed filings

**Step 2.2: Search API**
- Postgres full-text search across organization names
- Structured filters: state, NTEE code, revenue range, asset range, filing year
- Typeahead/autocomplete endpoint (optimized for speed)
- Pagination and result counting
- Tests: Search for known organizations by name returns correct results, filter combinations work correctly, typeahead responds in < 200ms, pagination returns correct pages

**Step 2.3: Organization Profile API**
- Endpoint that returns all data for a given organization
- Financial time series (all filings, ordered by tax year)
- People data (officers, directors, key employees, compensation)
- Grant data (for 990-PF filers)
- Computed metrics: program expense ratio, fundraising efficiency, revenue growth rate
- Tests: Profile for a known org returns correct financial history, computed metrics match hand-calculated values, handles orgs with only one filing gracefully

**Step 2.4: Search UI**
- Search bar with typeahead
- Filter panel (state, NTEE, revenue range, etc.)
- Results list with key stats per org (revenue, assets, location, latest filing year)
- Empty states and loading states
- Tests: Search renders results, filters update results, clicking a result navigates to profile, empty search shows appropriate message

**Step 2.5: Organization Profile Page**
- Header: name, EIN, location, NTEE category, mission
- Financial overview: revenue, expenses, net assets (latest year)
- Financial trend charts (line charts for revenue/expenses/assets over time)
- People table: officers and key employees with compensation
- Grants table (990-PF only): recipients, amounts, purposes
- Key metrics cards: program expense ratio, fundraising efficiency, revenue growth
- Tests: Profile page renders all sections for a complete org, handles missing data gracefully, charts render correctly, responsive on mobile

**Step 2.6: Usage Tracking**
- Log search events, profile views, and other user actions to `usage_events`
- Basic usage dashboard in settings (your searches this month)
- Tests: Searching creates a usage event, viewing a profile creates a usage event, usage counts are accurate

### Phase 2 Exit Criteria

1. At least 100,000 organizations are searchable (subset load for MVP)
2. Search returns results in < 500ms
3. Organization profiles display complete financial histories
4. All tests pass
5. CHANGELOG and CLAUDE.md updated

---

## 10. Phase 3: Intelligence Layer

### Goal

Add the AI-powered features that differentiate 990 Beacon from existing tools: automated financial health scoring, LLM-generated narrative summaries, and peer benchmarking.

### Steps

**Step 3.1: Financial Health Scoring Algorithm**
- Implement the scoring model with six dimensions:
  - **Revenue Diversity** (0-100): Herfindahl index across revenue sources. Penalize orgs where >80% comes from one source.
  - **Operating Reserves** (0-100): Months of operating expenses covered by unrestricted net assets. Score: 0 months = 0, 3 months = 50, 6+ months = 100.
  - **Fundraising Efficiency** (0-100): Cost to raise $1. Score: >$0.50 = 0, $0.25 = 50, <$0.10 = 100. N/A for orgs with no fundraising.
  - **Program Expense Ratio** (0-100): % of total expenses going to programs. Score: <50% = 0, 75% = 50, >85% = 100.
  - **Revenue Growth** (0-100): 3-year compound annual growth rate. Score: negative = 25 (unless intentional wind-down), 0% = 50, >10% = 100.
  - **Working Capital** (0-100): Current assets minus current liabilities divided by total expenses. Score: negative = 0, 0 = 25, 25%+ = 100.
- Overall score: weighted average (equal weights initially, tunable)
- Peer percentile: rank within NTEE code + revenue decile
- Batch job to score all organizations with sufficient data
- Tests: Known healthy org scores > 70, known distressed org scores < 40, scores are deterministic, peer percentiles sum to 100

**Step 3.2: AI Summary Generation**
- Prompt engineering for org summaries using Claude Sonnet
- Input: latest filing data (structured), 3-year trend data, scoring output
- Output: 3-5 paragraph narrative covering: what the org does, financial health assessment, notable trends, key risks/opportunities, comparison to peers
- Rate limiting and cost tracking
- Caching: regenerate only when new filing is ingested
- Tests: Generated summaries mention the org by name, summaries reference specific financial data points, summaries don't hallucinate data not in the filing, cost per summary < $0.01

**Step 3.3: Benchmarking & Comparison**
- API endpoint: compare 2-5 organizations side by side
- Comparison data: all scored metrics, key financials, people/compensation
- Percentile context: "This org's program expense ratio is in the 75th percentile for [NTEE category]"
- Tests: Comparison of 3 orgs returns aligned data, percentile calculations are correct, handles orgs in different NTEE categories with appropriate caveats

**Step 3.4: Intelligence UI**
- Health score badge on org profile (color-coded, with breakdown)
- AI summary section on org profile (collapsible, with "regenerate" option)
- Comparison page: select orgs, see side-by-side metrics with charts
- Score explanation tooltip (what each dimension means)
- Tests: Score displays correctly on profile, summary renders with loading state, comparison page allows adding/removing orgs, score tooltips are informative

### Phase 3 Exit Criteria

1. All organizations with 3+ filings have health scores
2. AI summaries generate in < 10 seconds
3. Summaries are factually grounded in filing data
4. Comparison view works for 2-5 organizations
5. All tests pass
6. CHANGELOG and CLAUDE.md updated

---

## 11. Phase 4: Monetization

### Goal

Implement Stripe billing with tiered subscriptions, usage metering, and a customer portal. Free users get limited access; paid users unlock full features.

### Steps

**Step 4.1: Stripe Integration — Backend**
- Stripe products and prices for three tiers (Free, Pro, Team)
- Webhook handler for subscription events (created, updated, canceled, payment_failed)
- Sync subscription status to user/team records
- Tests: Creating a subscription updates user's plan_tier, canceling a subscription downgrades to free, webhook signature validation works, handles duplicate webhook events idempotently

**Step 4.2: Usage Metering & Limits**
- Define limits per tier:
  - **Free:** 10 searches/day, 5 profile views/day, no exports, no AI summaries, no API
  - **Pro ($49/mo):** Unlimited search, unlimited profiles, 50 exports/mo, AI summaries, 5 watchlists, no API
  - **Team ($149/mo per 3 seats, +$39/seat):** Everything in Pro + team workspaces, shared watchlists, 200 exports/mo, API access (1,000 calls/mo)
- Middleware that checks usage against limits before processing requests
- Usage counter reset at billing cycle start
- Graceful limit-reached UX (not a hard error — show upgrade prompt)
- Tests: Free user is blocked after 10 searches, Pro user is not blocked, usage resets at billing cycle, upgrade prompt displays correctly

**Step 4.3: Billing UI**
- Pricing page (public, on marketing site)
- Upgrade flow from within the app
- Stripe Customer Portal link for managing subscription
- Current plan display in settings
- Usage meter display (e.g., "8 of 10 searches used today")
- Tests: Pricing page renders all tiers, upgrade redirects to Stripe Checkout, Stripe portal opens correctly, usage display is accurate

**Step 4.4: Trial & Onboarding**
- 14-day free trial of Pro for new signups (no credit card required)
- Onboarding flow: welcome screen → guided search → save first watchlist → see first AI summary
- Trial expiry handling: downgrade to Free, send email 3 days before expiry
- Tests: New user starts on Pro trial, trial expiry downgrades correctly, expiry email sends at T-3 days

### Phase 4 Exit Criteria

1. Can complete full purchase flow: sign up → trial → enter payment → subscribe
2. Usage limits enforced correctly per tier
3. Stripe webhooks handle all subscription lifecycle events
4. Downgrade and cancellation work cleanly
5. All tests pass
6. CHANGELOG and CLAUDE.md updated

---

## 12. Phase 5: Collaboration & Alerts

### Goal

Enable team workflows and proactive monitoring. Users can share research, collaborate in teams, and get notified when organizations they're tracking have new filings or significant changes.

### Steps

**Step 5.1: Watchlists (Full Implementation)**
- Create, rename, delete watchlists
- Add/remove organizations from watchlists
- Attach notes to watchlist items
- Bulk actions (add multiple orgs from search results)
- Watchlist summary view: aggregated stats across all tracked orgs
- Tests: CRUD operations work, notes persist, bulk add works, summary stats are accurate

**Step 5.2: Team Workspaces**
- Create team (linked to Clerk organization)
- Invite members by email
- Role management (owner, admin, member)
- Shared watchlists (visible to all team members)
- Activity feed: "[Member] viewed [Org]", "[Member] added [Org] to [Watchlist]"
- Tests: Invitation flow works, roles restrict correctly (member can't delete team), shared watchlists visible to all members, activity feed records events

**Step 5.3: Email Alerts**
- New filing alert: "Organization X filed their 2025 990 — here's what changed"
- Threshold alert: "Organization X's revenue dropped 20% year-over-year"
- Leadership change alert: "New CEO listed at Organization X"
- Weekly digest: summary of all watchlist activity
- Alert preferences (per watchlist: email, in-app, or off)
- Tests: New filing ingestion triggers alert for watchers, threshold calculations are correct, email renders correctly, user can disable alerts, digest only includes relevant changes

**Step 5.4: In-App Notifications**
- Notification bell in the app header
- Notification list with mark-as-read
- Real-time updates (Supabase Realtime or polling)
- Tests: Notifications appear when alerts fire, mark-as-read works, unread count is accurate

### Phase 5 Exit Criteria

1. Users can create watchlists and get email alerts for changes
2. Teams can share watchlists and see each other's activity
3. Alert emails are well-formatted and actionable
4. All tests pass
5. CHANGELOG and CLAUDE.md updated

---

## 13. Phase 6: API & Scale

### Goal

Expose a public RESTful API for programmatic access, implement rate limiting, API key management, and optimize the system for scale.

### Steps

**Step 6.1: Public API**
- API key issuance and management (in settings page)
- API key authentication middleware
- Endpoints: search, organization profile, scores, comparison
- OpenAPI/Swagger documentation auto-generated from FastAPI
- API versioning (`/api/v1/`)
- Tests: API key auth works, invalid key returns 401, all endpoints return correct data, OpenAPI spec is valid

**Step 6.2: Rate Limiting**
- Per-plan rate limits (stored in Redis)
- Rate limit headers in responses (`X-RateLimit-Remaining`, `X-RateLimit-Reset`)
- Graceful 429 response with retry-after
- Tests: Rate limit headers present, exceeding limit returns 429, limits reset correctly

**Step 6.3: Performance Optimization**
- Database query optimization (EXPLAIN ANALYZE on slow queries)
- Redis caching for hot organization profiles and search results
- Connection pooling tuning
- CDN for static assets
- Tests: Search p95 < 300ms, profile load p95 < 500ms, cache hit rate > 60% for repeat queries

**Step 6.4: Data Pipeline Scale**
- Full historical load of all ~3M filings
- Incremental weekly processing
- Pipeline monitoring and alerting
- Tests: Full dataset loaded, weekly job completes without errors, monitoring alerts on failure

### Phase 6 Exit Criteria

1. Public API is documented and functional
2. Rate limiting works per plan
3. System handles 100 concurrent users without degradation
4. Full 990 dataset is loaded
5. All tests pass
6. CHANGELOG and CLAUDE.md updated

---

## 14. Phase 7: Marketing & Launch

### Goal

Prepare the product for public launch with a marketing site, content, and launch strategy.

### Steps

**Step 7.1: Marketing Site**
- Hero section with clear value proposition
- Feature showcase with screenshots
- Pricing table
- FAQ section
- Social proof / testimonials (initially: "Built by a prospect researcher with 10+ years in advancement")
- CTA: "Start your free trial"
- SEO: meta tags, Open Graph, structured data
- Tests: Lighthouse performance > 90, SEO meta tags present, all links work, responsive on mobile

**Step 7.2: Content & SEO**
- Blog section (Next.js MDX)
- Launch post: "Why I built 990 Beacon"
- 3-5 SEO-targeted posts: "How to read a 990 form", "Top 10 metrics for evaluating foundation health", "990-PF grant analysis guide"
- Documentation site for API users
- Tests: Blog posts render correctly, sitemap.xml is valid, documentation is accurate

**Step 7.3: Launch Checklist**
- Legal: Terms of Service, Privacy Policy (use a template, not legal advice)
- Custom domain setup
- Error monitoring (Sentry) verified in production
- Analytics (PostHog) tracking key events
- Transactional email templates tested
- Stripe production mode enabled
- Database backups configured
- Incident response plan documented
- Tests: All production services accessible, error monitoring captures test error, analytics tracks test event, backup runs successfully

**Step 7.4: Launch Channels**
- Prospect Research community (APRA Connect)
- LinkedIn post
- Product Hunt submission
- Hacker News "Show HN"
- Nonprofit technology forums and Slack groups
- Direct outreach to 10 prospect researchers Michael knows personally
- Tests: Launch page loads under peak traffic simulation

### Phase 7 Exit Criteria

1. Marketing site is live and polished
2. At least 5 pieces of content published
3. Legal pages in place
4. All production infrastructure verified
5. Launch executed on at least 3 channels
6. All tests pass
7. CHANGELOG and CLAUDE.md updated

---

## 15. Pricing Strategy

### Tiers

| Feature | Free | Pro ($49/mo) | Team ($149/mo base) |
|---|---|---|---|
| Organization search | 10/day | Unlimited | Unlimited |
| Profile views | 5/day | Unlimited | Unlimited |
| Financial health scores | View only (no breakdown) | Full breakdown | Full breakdown |
| AI summaries | No | Yes | Yes |
| Watchlists | 1 (max 10 orgs) | 5 (unlimited orgs) | Unlimited (shared) |
| Email alerts | No | Weekly digest | Real-time + digest |
| Benchmarking/comparison | No | Up to 3 orgs | Up to 5 orgs |
| Exports (PDF/CSV) | No | 50/month | 200/month |
| API access | No | No | 1,000 calls/month |
| Team members | 1 | 1 | 3 included (+$39/seat) |
| Support | Community | Email (48hr) | Priority email (24hr) |

### Pricing Rationale

- **Free tier** is generous enough to be useful for occasional researchers and serves as top-of-funnel. The 10 search / 5 profile daily limit lets someone evaluate the product meaningfully.
- **Pro at $49/mo** is positioned well below institutional tools (Candid at $3K+/yr) but above the "hobby" threshold. For an individual consultant or researcher, this pays for itself if it saves 2+ hours per month.
- **Team at $149/mo** for 3 seats is ~$50/seat — aligned with Pro pricing — but adds collaboration and API features that make it attractive for small teams. Additional seats at $39 give volume discount incentive.

### Annual Discount

20% discount for annual billing: Pro at $470/yr ($39/mo effective), Team at $1,430/yr ($119/mo effective).

---

## 16. Success Metrics

### North Star Metric

**Weekly Active Searchers** — unique users who perform at least one search per week. This measures core engagement with the product's primary value.

### Phase-Specific Metrics

| Phase | Key Metric | Target |
|---|---|---|
| Phase 1 | Successful auth round-trip | 100% of signups create DB user |
| Phase 2 | Search latency p95 | < 500ms |
| Phase 2 | Organizations searchable | > 100,000 |
| Phase 3 | AI summary factual accuracy | > 95% (spot-check audit) |
| Phase 4 | Trial → Paid conversion | > 5% |
| Phase 5 | Alert click-through rate | > 20% |
| Phase 6 | API uptime | > 99.5% |
| Phase 7 | Signups in first month | > 100 |

### Business Metrics (6-12 months post-launch)

- Monthly Recurring Revenue (MRR)
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV) — target LTV:CAC > 3:1
- Net Revenue Retention — target > 100% (expansion revenue from upgrades)
- Churn rate — target < 5% monthly

---

## 17. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| IRS changes 990 XML schema | Low | High | Abstract the parser behind an adapter. Version the parser. Monitor IRS announcements. |
| IRS stops publishing e-file data | Very Low | Critical | Data is mandated by law. If S3 bucket changes, alternative sources exist (bulk download). |
| LLM costs exceed budget | Medium | Medium | Cache aggressively. Use Haiku for simple tasks. Set per-user generation limits. Monitor daily spend. |
| Competitor launches similar product | Medium | Medium | Domain expertise and speed of iteration are the moat, not the idea. Stay close to users. |
| Low conversion rate | High | High | Validate pricing with target users before building payment. Consider freemium adjustments. |
| Data quality issues (malformed 990s) | High | Medium | Robust error handling in parser. Flag incomplete records. Show data confidence indicators in UI. |
| Scope creep | High | Medium | This PRD defines phases. Resist adding features until current phase exit criteria are met. |
| Solo developer burnout | Medium | High | Phases are scoped to 2-3 weeks. Ship something working at each phase. Celebrate milestones. |

---

## 18. Logging & Learning Protocol

### CHANGELOG.md

After each phase, log:

```markdown
## Phase [N]: [Name] — Completed [Date]

### What Was Built
- [Feature/component 1]
- [Feature/component 2]

### Why These Decisions Were Made
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

### What Changed From the Plan
- [Deviation 1]: [Why]

### Time Spent
- Estimated: [X hours/days]
- Actual: [Y hours/days]
- Delta explanation: [Why]
```

### CLAUDE.md — Skills & Lessons Learned

This file serves two purposes:
1. **Project-specific context** for AI assistants (Claude, Copilot) working on this codebase
2. **Living knowledge base** of mistakes, gotchas, and patterns learned during development

Structure:

```markdown
# CLAUDE.md — 990 Beacon

## Project Overview
[Brief description for AI context]

## Tech Stack Quick Reference
[Versions, key libraries, deployment targets]

## Architecture Decisions
[Key decisions and their rationale]

## Known Gotchas
### [Category: e.g., "IRS 990 Parsing"]
- [Gotcha 1]: [What happened, why, how to avoid]
- [Gotcha 2]: [...]

### [Category: e.g., "Clerk Auth"]
- [Gotcha 1]: [...]

## Patterns & Conventions
- [Naming conventions]
- [File organization rules]
- [Testing patterns]
- [Error handling patterns]

## Never Do This Again
- [ ] [Mistake 1]: [What went wrong, what to do instead]
- [ ] [Mistake 2]: [...]

## Skills Learned
- [Skill 1]: [Date] — [Brief description of what was learned]
- [Skill 2]: [Date] — [...]
```

### Testing Protocol

Every step in every phase follows this protocol:

1. **Write tests first** (or simultaneously) for the feature being built
2. **Run tests locally** — all must pass before committing
3. **Commit with conventional commit message** (`feat:`, `fix:`, `test:`, `docs:`, `chore:`)
4. **Push to feature branch** — CI runs automatically
5. **CI must pass** before merging to main
6. **After merge** — verify deployed environment works

Test categories:
- **Unit tests:** Pure logic, no external dependencies. Fast. Run on every commit.
- **Integration tests:** Tests that touch the database or external services. Use test fixtures.
- **E2E tests (Phase 2+):** Playwright tests for critical user flows (sign up, search, view profile).

---

## Appendix A: IRS 990 XML Field Mapping

The IRS 990 e-file XML uses XPath expressions to locate fields. The mapping varies by form type and schema version. Key fields:

| Field | 990 XPath | 990-EZ XPath |
|---|---|---|
| Organization Name | `//Return/ReturnHeader/Filer/BusinessName/BusinessNameLine1Txt` | Same |
| EIN | `//Return/ReturnHeader/Filer/EIN` | Same |
| Tax Year | `//Return/ReturnHeader/TaxYr` | Same |
| Total Revenue | `//Return/ReturnData/IRS990/CYTotalRevenueAmt` | `//IRS990EZ/TotalRevenueAmt` |
| Total Expenses | `//Return/ReturnData/IRS990/CYTotalExpensesAmt` | `//IRS990EZ/TotalExpensesAmt` |
| Net Assets | `//Return/ReturnData/IRS990/NetAssetsOrFundBalancesEOYAmt` | `//IRS990EZ/NetAssetsOrFundBalancesEOYAmt` |
| Mission | `//Return/ReturnData/IRS990/ActivityOrMissionDesc` | `//IRS990EZ/PrimaryExemptPurposeTxt` |

Note: Field names changed between IRS schema versions (2013 vs 2014+). The parser must handle both naming conventions.

---

## Appendix B: NTEE Code Categories

The National Taxonomy of Exempt Entities (NTEE) classifies nonprofits into 26 major categories (A-Z) and ~400 subcategories. Key categories for prospect research:

- **A** — Arts, Culture, and Humanities
- **B** — Education
- **E** — Health
- **G** — Voluntary Health Associations
- **H** — Medical Research
- **P** — Human Services
- **T** — Philanthropy, Voluntarism, and Grantmaking Foundations
- **U** — Science and Technology
- **X** — Religion

NTEE codes are used for peer benchmarking (comparing orgs within the same category).

---

## Appendix C: Phase 1 File-by-File Specification

### Backend Files

**`backend/app/main.py`**
```python
# FastAPI app factory
# - CORS middleware (allow frontend origin)
# - Exception handlers (return JSON for all errors)
# - Include routers: health, webhooks, users
# - Lifespan handler for DB connection pool
```

**`backend/app/core/config.py`**
```python
# Pydantic BaseSettings
# Fields: DATABASE_URL, REDIS_URL, CLERK_SECRET_KEY, CLERK_WEBHOOK_SECRET,
#         STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, ANTHROPIC_API_KEY,
#         FRONTEND_URL, ENVIRONMENT (dev/staging/prod)
```

**`backend/app/core/database.py`**
```python
# SQLAlchemy async engine
# AsyncSession factory
# get_db dependency generator
```

**`backend/app/core/deps.py`**
```python
# get_current_user: decode Clerk JWT → lookup user in DB → return User model
# get_optional_user: same but returns None for unauthenticated requests
# get_db: yield async DB session
```

**`backend/app/models/organization.py`**
```python
# SQLAlchemy models: Organization, Filing, FilingPerson, FilingGrant
```

**`backend/app/models/user.py`**
```python
# SQLAlchemy models: User, Team, TeamMember
```

**`backend/app/models/watchlist.py`**
```python
# SQLAlchemy models: Watchlist, WatchlistItem, SavedSearch
```

**`backend/app/models/analytics.py`**
```python
# SQLAlchemy models: UsageEvent, OrgSummary, OrgScore
```

**`backend/app/schemas/user.py`**
```python
# Pydantic schemas: UserResponse, UserCreate (from webhook), ClerkWebhookPayload
```

**`backend/app/api/health.py`**
```python
# GET /health → {"status": "ok", "db": "connected", "version": "0.1.0"}
```

**`backend/app/api/webhooks.py`**
```python
# POST /api/v1/webhooks/clerk
# Verify Svix signature → handle user.created, user.updated, user.deleted
```

**`backend/app/api/users.py`**
```python
# GET /api/v1/me → current user profile
```

### Frontend Files

**`frontend/src/app/layout.tsx`** — Root layout with Clerk provider

**`frontend/src/app/page.tsx`** — Marketing landing page

**`frontend/src/app/(auth)/sign-in/[[...sign-in]]/page.tsx`** — Clerk sign-in

**`frontend/src/app/(auth)/sign-up/[[...sign-up]]/page.tsx`** — Clerk sign-up

**`frontend/src/app/dashboard/layout.tsx`** — Authenticated layout with sidebar

**`frontend/src/app/dashboard/page.tsx`** — Dashboard home (fetches /api/v1/me)

**`frontend/src/components/app-shell.tsx`** — Sidebar + header + content area

**`frontend/src/components/sidebar.tsx`** — Navigation links

**`frontend/src/lib/api.ts`** — API client with auth header injection

---

*This document is a living artifact. It will be updated as phases are completed and as the product evolves based on user feedback and technical learnings.*
