# POS System — CS50 Final Project

A full-stack **Point-of-Sale (POS)** application built as my final project for **CS50x**. The system lets a small retail shop ring up customer sales, manage the product catalog, track stock as items are sold, and review business performance through a dashboard with charts.

#### Video Demo: <URL HERE>

---

## Description

This project is a complete two-tier web application — a **FastAPI** backend exposing a JSON REST API, and a **Vue 3** frontend that consumes it. The frontend is the cashier-facing POS terminal: cashiers log in, build a cart of products, and check the sale out in a single click. Behind the scenes the backend records the transaction, decrements stock for each item, and serves the dashboard that the shop owner uses to review the day.

I chose to build a POS rather than a generic CRUD app because checkout is genuinely hard to get right — it has to be **atomic** (the sale, its line items, and the stock decrements all succeed or all fail together), it has to be **safe under concurrency** (two cashiers ringing up the same last item must not oversell), and it has to be **trustworthy** (clients cannot tamper with prices and historical sales cannot be silently edited). Solving those problems forced me to use real database transactions, row-level locking, server-side price computation, and immutable sale records — concepts that go beyond what a typical CS50x tracker app teaches.

I deliberately split the backend into clean layers (router → service → model) so that adding a new resource is a mechanical exercise rather than an architectural decision. Pydantic schemas act like Laravel Form Requests — they validate input *before* business logic runs, and they shape the JSON output so that sensitive fields like `password_hash` can never leak.

---

## Features

### 🔐 User login (JWT)
- `POST /api/v1/auth/login` issues a Bearer token signed with HS256
- Tokens carry `sub` (user id), `role`, and `exp` (60-minute expiry)
- The frontend stores the token in `localStorage` and attaches it to every request via the API helper in [frontend/src/services/api.js](frontend/src/services/api.js)
- A Vue Router guard redirects unauthenticated visitors to `/login`

### 👥 Role-based access (`staff` + `admin`)
The two roles are intentionally **non-overlapping** for the write actions, mirroring how a real shop is run — the owner manages the catalog, the cashier rings up customers:

- **Admin only** — manages the product catalog (`POST`, `PATCH`, `DELETE` on `/products`) and reviews who has access (`GET /users`). **Admins cannot create sales.**
- **Staff only** — rings up customer transactions (`POST /sales`). **Staff cannot add, edit, or delete products.**
- **Both roles** can read the product list, view the sales history, and see the dashboard.

How the rules are enforced:
- **Server-side** — `POST /products`, `PATCH /products/{id}`, `DELETE /products/{id}`, and `GET /users` are guarded by the FastAPI `require_admin` dependency. A wrong role gets `403 Forbidden`.
- **Client-side** — the staff-only "create sale" UI is hidden from admin accounts, and the admin-only product/user management UI is hidden from staff accounts. The sidebar in [frontend/src/components/layout/Sidebar.vue](frontend/src/components/layout/Sidebar.vue) and the route guard in [frontend/src/router/index.js](frontend/src/router/index.js) read the user's role from the JWT and gate navigation accordingly.
- New self-registrations always default to `staff` — clients cannot self-promote to `admin`

### 📦 Product CRUD
- Full create / read / update / delete with admin enforcement on writes
- SKU uniqueness checked at both the application and the PostgreSQL `UNIQUE` constraint level (race-condition safe)
- Inputs validated by Pydantic — SKU pattern (uppercase letters/digits/hyphen), price > 0 with two decimal places, stock between 0 and 1,000,000
- Delete is blocked (HTTP 409) if the product is referenced by past sales — preserves audit history via DB-level `ON DELETE RESTRICT`

### 💰 Sale process (atomic checkout)
- A single `POST /api/v1/sales` endpoint accepts a cart of line items
- The service layer locks the affected product rows with `SELECT … FOR UPDATE`, validates stock, computes `unit_price` server-side (the client cannot tamper with prices), inserts the `Sale` and all `SaleItem` rows, decrements stock, and commits in **one transaction**
- If anything fails, the entire transaction rolls back — no orphaned sales, no negative stock
- Sales are immutable (no edit endpoint) so that financial records remain trustworthy

### 📊 Dashboard reporting
- `GET /dashboard/summary` — KPI cards (total sales amount, total quantity sold, product count)
- `GET /dashboard/sales-by-month` — bar-chart data for monthly order counts
- `GET /dashboard/users-by-role` — donut-chart data for the staff vs admin breakdown
- All aggregates are computed in SQL (`SUM`, `COUNT`, `GROUP BY`) — no row-by-row scanning in Python
- Charts rendered on the frontend with **Chart.js** via `vue-chartjs`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | FastAPI (Python 3.11) |
| ORM | SQLAlchemy 2.x (typed `Mapped[]` syntax) |
| Database | PostgreSQL 17 |
| Auth | JWT (`python-jose`) + bcrypt password hashing |
| Validation | Pydantic v2 |
| Dependency mgmt | Pipenv |
| Frontend framework | Vue 3 (Composition API) + Vite |
| UI library | PrimeVue 4 + PrimeIcons |
| Routing | Vue Router 4 |
| Charts | Chart.js 4 + vue-chartjs |
| HTTP client | Native `fetch` wrapper |

---

## Project Structure

```
inventory-dashboard-cs50/
├── backend/
│   ├── main.py                     # FastAPI app, lifespan, CORS, router include
│   ├── Pipfile / Pipfile.lock      # Python dependencies
│   ├── .env                        # DB credentials + JWT secret (gitignored)
│   └── app/
│       ├── core/
│       │   ├── config.py           # Pydantic Settings — reads .env
│       │   ├── database.py         # SQLAlchemy engine, SessionLocal, get_db
│       │   └── security.py         # bcrypt + JWT encode/decode
│       ├── api/
│       │   ├── deps.py             # get_current_user, require_admin
│       │   └── v1/
│       │       ├── router.py       # Aggregates all endpoint routers
│       │       └── endpoints/
│       │           ├── auth.py     # POST /auth/login
│       │           ├── users.py    # /users + /users/register + /users/me
│       │           ├── products.py # GET/POST/PATCH/DELETE /products
│       │           ├── sales.py    # GET/POST /sales
│       │           └── dashboard.py# /dashboard/{summary,sales-by-month,users-by-role}
│       ├── models/                 # SQLAlchemy ORM models (User, Product, Sale, SaleItem)
│       ├── schemas/                # Pydantic request/response schemas
│       └── services/               # Business logic — DB access lives here
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.js                 # Vue app bootstrap, PrimeVue, router
        ├── App.vue
        ├── router/index.js         # Routes + auth guard
        ├── composables/useAuth.js  # Reactive auth state
        ├── services/               # API client (api.js + per-resource modules)
        │   ├── api.js              # Base fetch wrapper with auth header injection
        │   ├── products.js
        │   ├── sales.js
        │   ├── users.js
        │   └── dashboard.js
        ├── views/                  # Page components
        │   ├── Login.vue
        │   ├── Dashboard.vue       # KPIs + bar chart + donut chart
        │   ├── Products.vue        # CRUD table
        │   ├── Sale.vue            # Cart + checkout
        │   └── Users.vue           # Admin-only user list
        └── components/
            ├── layout/             # Sidebar + main shell
            ├── products/           # Product create/edit modals
            ├── sales/              # Sale checkout modal
            └── users/              # User create modal
```

### Why this layout

The backend follows the **router → service → model** pattern that scales from a one-file prototype into a mature application without refactoring:

- **Router (`endpoints/`)** — thin HTTP layer. It parses the request, calls a service function, and returns the result. No business logic.
- **Service (`services/`)** — owns the workflow. Validates business rules, talks to the database, manages transactions.
- **Model (`models/`)** — pure data definitions backed by SQLAlchemy. No behavior.
- **Schema (`schemas/`)** — Pydantic models for API contracts. The same SKU validation that runs on input also documents the API in Swagger.

The frontend mirrors this with **views → services → composables**, keeping API calls out of components.

---

## Database Schema

Four tables, designed up front:

```sql
users        — id, username (unique), password_hash, role, created_at
products     — id, sku (unique), name, price, stock_quantity, created_at, updated_at
sales        — id, user_id (FK→users, ON DELETE SET NULL), total_amount, created_at
sale_items   — id, sale_id (FK→sales, ON DELETE CASCADE),
               product_id (FK→products, ON DELETE RESTRICT),
               quantity, unit_price, subtotal
```

Foreign-key behavior was a deliberate design choice:
- A deleted user shouldn't erase their historical sales → `SET NULL`
- A voided sale should remove its line items → `CASCADE`
- A product that's been sold can't be deleted (audit integrity) → `RESTRICT`

A PostgreSQL custom-format dump (`pos_cs50`) is included in the repo root with the schema **and** seed accounts (one `admin`, one `staff`) so reviewers can log in immediately without registering.

---

## Setup

### Prerequisites
- Python 3.11
- Node.js 20.19+ (or 22.12+)
- PostgreSQL 17 running locally on port `5435`
- Pipenv (`pip install pipenv`)

### 1. Database

The seed file `pos_cs50` is a PostgreSQL **custom-format** dump (created with `pg_dump -Fc`), so it must be loaded with `pg_restore`, not `psql -f`.

```bash
# Create the empty database
createdb -h localhost -p 5435 pos

# Restore schema + seed data into it (run from the repo root)
pg_restore -h localhost -p 5435 -d pos pos_cs50
```

The dump ships with two seeded accounts (both use the password `12345678`):

| Username | Password | Role |
|---|---|---|
| `admin` | `12345678` | admin |
| `staff` | `12345678` | staff |

Use these to log in straight after the frontend boots.

### 2. Backend

```bash
cd backend
pipenv install
```

Create `backend/.env`:

```
DB_USERNAME=mht
DB_PASSWORD=12345678
DB_HOST=localhost
DB_PORT=5435
DB_NAME=pos

SECRET_KEY=<generate with: openssl rand -hex 32>
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Run the API:

```bash
pipenv run uvicorn main:app --reload --port 8000
```

Open <http://localhost:8000/docs> for the interactive Swagger UI.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the URL Vite prints (usually <http://localhost:5173>) and log in with `admin` / `12345678` or `staff` / `12345678` from the seed dump.

---

## API Reference

| Method | Path | Auth |
|---|---|---|
| POST | `/api/v1/auth/login` | public |
| POST | `/api/v1/users/register` | public |
| GET | `/api/v1/users/me` | any user |
| GET | `/api/v1/users` | admin |
| GET | `/api/v1/products` | any user |
| POST | `/api/v1/products` | admin |
| PATCH | `/api/v1/products/{id}` | admin |
| DELETE | `/api/v1/products/{id}` | admin |
| GET | `/api/v1/sales` | any user |
| POST | `/api/v1/sales` | any user (UI-gated to staff) |
| GET | `/api/v1/dashboard/summary` | any user |
| GET | `/api/v1/dashboard/sales-by-month` | any user |
| GET | `/api/v1/dashboard/users-by-role` | any user |

Full request/response schemas (with examples) are auto-generated and browsable at `/docs` once the backend is running.

---

## Design Decisions Worth Calling Out

- **Server-computed prices.** When creating a sale, the client sends only `product_id` and `quantity`. The backend looks up the current price itself — a client cannot send `unit_price: 0.01` to commit fraud.
- **`SELECT … FOR UPDATE` row locking** during checkout prevents two concurrent sales from selling the same last item.
- **`Decimal` everywhere for money.** No `float`. The DB column is `NUMERIC(10,2)` and the Python type is `Decimal` end-to-end so rounding never bites.
- **Eager loading on `GET /sales`** uses `joinedload(Sale.user)` and `selectinload(Sale.items).joinedload(SaleItem.product)` to avoid N+1 queries when the frontend asks for the full sale tree.
- **Strict typing in services** — variables are annotated, and `cast()` is used at SQLAlchemy boundaries instead of runtime conversions like `Decimal(x)` or `int(x)`.
- **`__init__.py` in every package** so that imports work the same way under uvicorn, pytest, and direct invocation.

---

## Files I Wrote

Practically every Python file under `backend/app/` and every `.vue` / `.js` file under `frontend/src/` (apart from the Vite scaffolding in `frontend/src/components/icons/` and the demo `HelloWorld.vue` / `TheWelcome.vue` / `WelcomeItem.vue`, which I left from `npm create vue@latest` for reference).

The most substantial files:
- [backend/app/services/sale_service.py](backend/app/services/sale_service.py) — atomic checkout logic with row locking
- [backend/app/services/dashboard_service.py](backend/app/services/dashboard_service.py) — SQL aggregates
- [backend/app/api/deps.py](backend/app/api/deps.py) — JWT decoding + role guards
- [backend/app/core/security.py](backend/app/core/security.py) — bcrypt + token issuing
- [frontend/src/views/Sale.vue](frontend/src/views/Sale.vue) — cart UI and checkout flow
- [frontend/src/views/Dashboard.vue](frontend/src/views/Dashboard.vue) — KPI cards and chart wiring
