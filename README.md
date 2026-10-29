# Public Bicycle Rental Management System (PBRMS)

> A centralized, production-ready, full-stack web application designed for urban bicycle rental management, connecting **Administrators**, **Customers / Users**, and **Rental Owners**. Fully implements all 24 Jira backlog user stories across 4 Sprints (PB-01 to PB-24, total **97 Story Points**).

---

## Table of Contents
1. [Project Overview & Key Features](#project-overview--key-features)
2. [Technology Stack](#technology-stack)
3. [System Architecture](#system-architecture)
4. [Project Directory Structure](#project-directory-structure)
5. [Database Setup & Schema](#database-setup--schema)
6. [Environment Variables](#environment-variables)
7. [Installation & Setup](#installation--setup)
8. [Demo Accounts & Credentials](#demo-accounts--credentials)
9. [Running the Application](#running-the-application)
10. [REST API Documentation](#rest-api-documentation)
11. [Jira Backlog Traceability (PB-01 to PB-24)](#jira-backlog-traceability-pb-01-to-pb-24)
12. [Testing, Coverage & QA Reports](#testing-coverage--qa-reports)
13. [DevOps & Jenkins CI Pipeline](#devops--jenkins-ci-pipeline)

---

## Project Overview & Key Features

The **Public Bicycle Rental Management System (PBRMS)** provides an end-to-end platform for shared micro-mobility services.

### Core User Roles
1. **Platform Administrator (`admin`)**:
   - Platform health, aggregate KPIs, revenue metrics, and user management.
   - Rental Owner verification & approval system (`PB-05`).
   - Docking station CRUD operations and station capacity management (`PB-06`, `PB-07`).
   - Sprints 1–4 Jira Backlog and Quality Assurance Audit Console.
2. **Customer / User (`user`)**:
   - Live docking station browser with capacity progress indicators (`PB-07`, `PB-11`).
   - Real-time keyword & station bicycle search (`PB-11`).
   - Atomic 1-click rental workflow with double-booking prevention (`PB-12`, `PB-13`).
   - Live ride duration timer and transparent fare calculation (`PB-14`, `PB-15`).
   - Return workflow to any destination station with capacity verification (`PB-16`).
   - Simulated payment ledger and receipt modal (`PB-17`).
3. **Rental Owner (`rental_owner`)**:
   - Fleet registration, hourly pricing, and station docking (`PB-08`, `PB-09`).
   - 1-click status transitions (`Available` ↔ `Maintenance`, `Inactive`) (`PB-10`).
   - Fleet earnings tracking and active rental monitoring.

---

## Technology Stack

- **Backend**: Python 3.10+, Flask Application Factory pattern, Flask Blueprints.
- **ORM & Models**: Flask-SQLAlchemy with declarative ORM models (`backend/models/`).
- **Database**: MySQL 8 relational schema with foreign key constraints, checks, transactions, and row-locking. Includes automatic zero-config SQLite fallback for isolated automated tests and portable zero-dependency execution.
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Bootstrap Icons. Fully responsive across desktop, tablet, and mobile.
- **Authentication**: Secure password hashing with `bcrypt` (salt generation, 12 rounds), JSON Web Tokens (`HS256`), server-side role-based access control (`@role_required`).
- **Testing & QA**: `pytest` test suite (35 passed tests), `pytest-cov` for branch and line coverage, `Radon` for cyclomatic complexity and maintainability index, and `Selenium` Headless Chrome for UI automation.
- **DevOps**: Declarative `Jenkinsfile`, `.gitignore`, `requirements.txt`, `.env.example`.

---

## System Architecture

```
+-----------------------------------------------------------------------------------------+
|                                    FRONTEND LAYER                                       |
|  - Landing Page (index.html)        - Station Browser (stations.html)                   |
|  - About & Rates (about.html)       - Login & Register (login.html, register.html)      |
|  - Customer Portal (/user/dashboard.html)                                               |
|  - Rental Owner Portal (/owner/dashboard.html)                                          |
|  - Admin Console & QA Audit (/admin/dashboard.html)                                     |
|              (Bootstrap 5, Vanilla ES6+ Fetch Client, JWT Storage)                      |
+-----------------------------------------------------------------------------------------+
                                             │  HTTPS / REST JSON
                                             ▼
+-----------------------------------------------------------------------------------------+
|                                    APPLICATION LAYER                                    |
|  Entry Points: run.py (CLI runner), backend/app.py (Factory)                            |
|  Blueprints:                                                                            |
|    - /api/auth       (Authentication, Registration, Profile)                            |
|    - /api/stations   (Station CRUD, Capacity Tracking)                                  |
|    - /api/bicycles   (Fleet Inventory, Status Transitions, Search)                      |
|    - /api/rentals    (Rental Workflow, Concurrency Guards, Return, Fare Calculation)    |
|    - /api/payments   (Simulated Payment Ledger)                                         |
|    - /api/admin      (Metrics, Owner Verification, User Management)                     |
|    - /api/qa         (Backlog, Complexity, Coverage, Automated Workflow Runner)         |
|  Middleware: JWT Verification (@token_required), RBAC (@role_required), Validators      |
|  Services: AuthService, StationService, BicycleService, RentalService, PaymentService   |
|  ORM Models: User, Admin, RentalOwner, Station, Bicycle, Rental, Payment                |
+-----------------------------------------------------------------------------------------+
                                             │  SQLAlchemy ORM / Parameterized SQL
                                             ▼
+-----------------------------------------------------------------------------------------+
|                                     DATA LAYER                                          |
|  MySQL 8 / SQLite Relational Database Engine                                            |
|  Tables: admin, user, rental_owner, station, bicycle, rental, payment                   |
+-----------------------------------------------------------------------------------------+
```

---

## Project Directory Structure

```
Seap/
├── backend/
│   ├── app.py                      # Flask application factory, CORS, static server & blueprints
│   ├── config.py                   # Environment configuration (Development, Testing, Production)
│   ├── extensions.py               # Shared SQLAlchemy extension instance
│   ├── requirements.txt            # Python dependencies (Flask, SQLAlchemy, bcrypt, pytest, radon, selenium)
│   ├── database/
│   │   ├── db.py                   # DB connection manager, query/execute helpers, schema initialization
│   │   └── seed.py                 # Automated seed data generator with bcrypt demo accounts
│   ├── models/
│   │   ├── __init__.py             # SQLAlchemy models exporter
│   │   ├── user.py                 # User, Admin, RentalOwner ORM models
│   │   ├── station.py              # Station ORM model
│   │   ├── bicycle.py              # Bicycle ORM model
│   │   ├── rental.py               # Rental ORM model
│   │   └── payment.py              # Payment ORM model
│   ├── routes/
│   │   ├── auth_routes.py          # /api/auth endpoints
│   │   ├── station_routes.py       # /api/stations endpoints
│   │   ├── bicycle_routes.py       # /api/bicycles endpoints (with keyword search)
│   │   ├── rental_routes.py        # /api/rentals endpoints (rent, return, active)
│   │   ├── payment_routes.py       # /api/payments endpoints
│   │   ├── admin_routes.py         # /api/admin metrics & owner approvals
│   │   └── qa_routes.py            # /api/qa backlog, complexity, coverage, workflow runner
│   ├── services/
│   │   ├── auth_service.py         # Bcrypt hashing, JWT generation & authentication
│   │   ├── station_service.py      # Station CRUD & capacity enforcement
│   │   ├── bicycle_service.py      # Inventory query, keyword search & lifecycle transitions
│   │   ├── rental_service.py       # Atomic booking, duration & fare algorithm, return logic
│   │   └── payment_service.py      # Simulated payment ledger management
│   └── utils/
│       ├── auth_middleware.py      # JWT decorators (@token_required, @role_required)
│       └── validators.py           # Field validation & password complexity checks
│
├── frontend/
│   ├── index.html                  # Landing page with Live Search, Station Directory & Jira Explorer
│   ├── about.html                  # About PBRMS, Fare Rules, and Role Guide
│   ├── stations.html               # Dedicated Station & Bicycle Search browser
│   ├── login.html                  # Unified login with 1-click demo credential buttons
│   ├── register.html               # Customer & Owner registration with interactive password meter
│   ├── user/
│   │   └── dashboard.html          # Customer portal: available bikes, active rental banner, return modal
│   ├── admin/
│   │   └── dashboard.html          # Admin console: KPIs, Owner Approvals, Station CRUD, QA Audit
│   ├── owner/
│   │   └── dashboard.html          # Rental Owner portal: fleet management & 1-click status maintenance
│   ├── css/
│   │   └── style.css               # Theme styling, Jira badges, priority pills, and QA console styles
│   └── js/
│       ├── api.js                  # Centralized Fetch API client with JWT handling
│       ├── auth.js                 # Authentication handlers & demo fill
│       ├── user.js                 # Customer rental flow, search filtering & live elapsed timer
│       ├── admin.js                # Admin management handlers & QA audit panel
│       └── owner.js                # Owner fleet handlers & status toggles
│
├── tests/
│   ├── conftest.py                 # Pytest fixtures and isolated test database setup
│   ├── test_admin.py               # Tests: Admin KPIs, User listing, Owner Approvals (PB-04, PB-05)
│   ├── test_auth.py                # Tests: Registration, Login, Hashing, RBAC (PB-02, PB-03, PB-04)
│   ├── test_bicycles.py            # Tests: Inventory, Status transitions, Capacity (PB-08, PB-09, PB-10)
│   ├── test_fare.py                # Tests: Fare calculation algorithm precision (PB-15)
│   ├── test_mysql_migration.py     # Tests: MySQL 8.0 pbrms_db live connection, models & relations
│   ├── test_qa.py                  # Tests: QA endpoints (backlog, complexity, coverage, workflow)
│   ├── test_rentals.py             # Tests: Rental workflow, Double-booking guard, Return (PB-12, PB-13, PB-16)
│   ├── test_stations.py            # Tests: Station CRUD, Lookup, Capacity updates (PB-06, PB-07)
│   ├── test_ui_workflow.py         # Tests: Headless E2E Customer Journey workflow (PB-23)
│   └── ui/
│       └── test_ui_selenium.py     # Genuine Selenium Headless Chrome UI automation test (PB-23)
│
├── docs/
│   └── JIRA_BACKLOG_MAPPING.md     # Traceability matrix for all 24 tasks (PB-01 to PB-24)
│
├── reports/
│   ├── coverage.txt                # Text-based Pytest coverage report (77% overall coverage)
│   ├── coverage_html/              # Interactive HTML Pytest coverage report
│   ├── complexity.txt              # Radon cyclomatic complexity and maintainability report
│   └── test_results.txt            # Verbose Pytest execution output (30/30 passed)
│
├── scripts/
│   └── migrate_sqlite_to_mysql.py  # Repeatable ETL migration from SQLite to MySQL pbrms_db
│
├── database/
│   ├── schema.sql                  # MySQL 8 DDL tables, foreign keys, and indexes
│   └── seed.sql                    # Initial seed data SQL
│
├── run.py                          # Unified CLI application runner
├── .env.example                    # Environment template with placeholders
├── .gitignore                      # Git ignore rules
├── Jenkinsfile                     # Declarative CI pipeline for Jenkins
└── README.md                       # Comprehensive documentation
```

---

## Database Setup & Schema

The system runs on **MySQL 8** (active database: `pbrms_db` using PyMySQL and SQLAlchemy) with isolated **SQLite** test mode (`TestingConfig`) for lightning-fast automated regression testing.

### Database Tables:
- **`admin`**: System administrators (`admin_id`, `name`, `email`, `password`, `created_at`)
- **`user`**: Registered customers (`user_id`, `name`, `email`, `phone`, `password`, `created_at`)
- **`rental_owner`**: Bicycle owners (`owner_id`, `name`, `email`, `phone`, `password`, `address`, `approval_status`, `created_at`)
- **`station`**: Docking stations (`station_id`, `station_name`, `location`, `capacity`, `available_bicycles`, `created_at`)
- **`bicycle`**: Fleet inventory (`bicycle_id`, `bicycle_number`, `type`, `status`, `rental_rate`, `owner_id`, `station_id`)
- **`rental`**: Rental transactions (`rental_id`, `user_id`, `bicycle_id`, `start_station_id`, `return_station_id`, `start_time`, `return_time`, `duration`, `fare`, `status`, `created_at`)
- **`payment`**: Simulated transaction ledger (`payment_id`, `rental_id`, `amount`, `status`, `payment_date`)

### Initializing and Migrating:
- **Automatic ORM table creation**: Tables are generated safely using SQLAlchemy declarative models via `init_db_schema()` or `db.create_all()`.
- **SQLite to MySQL ETL Migration**: Run `python scripts/migrate_sqlite_to_mysql.py` to transfer existing SQLite records with full row-count validation.

---

## Environment Variables

Copy `.env.example` to `.env` and configure your credentials:

```bash
copy .env.example .env
```

Configuration variables:
```ini
FLASK_ENV=development
SECRET_KEY=pbrms-super-secret-key-change-in-production-2026
JWT_EXPIRY_HOURS=24
PORT=5000

# MySQL 8 Configuration
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=pbrms_db
DB_USER=pbrms_user
DB_PASSWORD=your_password_here
USE_SQLITE_FALLBACK=false
DB_NAME=pbrms_db

# SQLite Fallback (set to false to force MySQL only)
USE_SQLITE_FALLBACK=true
```

---

## Installation & Setup

1. **Clone the repository and enter directory**:
   ```bash
   cd Seap
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r backend/requirements.txt
   ```

4. **Initialize database schema & seed data**:
   ```powershell
   python run.py --init-db --seed
   ```

---

## Demo Accounts & Credentials

The database comes pre-seeded with ready-to-test accounts. On `login.html`, click any quick-demo badge to prefill credentials:

| Role | Name | Email | Password | Status / Scenario |
| :--- | :--- | :--- | :--- | :--- |
| **Admin** | System Administrator | `admin@pbrms.com` | `Admin@123` | Full system audit & owner verification |
| **Customer** | Alice Johnson | `alice@example.com` | `User@123` | Has 1 active rental (returns test) |
| **Customer** | Bob Smith | `bob@example.com` | `User@123` | Clean customer account (ready to rent) |
| **Rental Owner** | John Doe (Metro Bikes) | `john.bikes@example.com` | `Owner@123` | **Approved** owner with fleet |
| **Rental Owner** | Sarah Connor (Eco Cycles) | `sarah.rentals@example.com` | `Owner@123` | **Pending** verification (PB-05 test) |
| **Rental Owner** | Mike Miller (Express Fleet) | `mike.cycles@example.com` | `Owner@123` | **Rejected** owner |

---

## Running the Application

Start the web application using the unified runner:

```powershell
python run.py
```

Options:
- `python run.py --port 5000`: Run on custom port
- `python run.py --host 0.0.0.0`: Bind to all network interfaces
- `python run.py --init-db --seed`: Reinitialize and seed database before running

Open your web browser at:
```
http://127.0.0.1:5000
```

### Key Application Pages:
- **Landing Page & Jira Explorer**: `http://127.0.0.1:5000/index.html`
- **About & Service Overview**: `http://127.0.0.1:5000/about.html`
- **Station & Bicycle Search**: `http://127.0.0.1:5000/stations.html`
- **User Login**: `http://127.0.0.1:5000/login.html`
- **User Registration**: `http://127.0.0.1:5000/register.html`
- **Customer Portal**: `http://127.0.0.1:5000/user/dashboard.html`
- **Rental Owner Portal**: `http://127.0.0.1:5000/owner/dashboard.html`
- **Admin Console & QA Audit**: `http://127.0.0.1:5000/admin/dashboard.html`

---

## REST API Documentation

| Method | Endpoint | Access | Backlog Ref | Description |
| :--- | :--- | :--- | :---: | :--- |
| `POST` | `/api/auth/register` | Public | PB-02, PB-03 | Register Customer or Rental Owner |
| `POST` | `/api/auth/login` | Public | PB-02, PB-03 | Authenticate and issue JWT token |
| `POST` | `/api/auth/logout` | Public | PB-02 | Clear session token |
| `GET` | `/api/auth/me` | Authenticated | PB-02, PB-04 | Retrieve authenticated user profile |
| `GET` | `/api/stations` | Public | PB-06, PB-07 | List all docking stations with counts |
| `GET` | `/api/stations/<id>` | Public | PB-06 | Retrieve details for a specific station |
| `POST` | `/api/stations` | Admin | PB-06 | Create new docking station |
| `PUT` | `/api/stations/<id>` | Admin | PB-06 | Update station name, location, capacity |
| `DELETE` | `/api/stations/<id>` | Admin | PB-06 | Delete station (if empty) |
| `GET` | `/api/bicycles` | Public | PB-08, PB-09 | List fleet bicycles with filters |
| `GET` | `/api/bicycles/available` | Public | PB-11 | Search available bicycles (`?station_id=&search=`) |
| `POST` | `/api/bicycles` | Admin, Owner | PB-09 | Register new fleet bicycle |
| `PUT` | `/api/bicycles/<id>` | Admin, Owner | PB-09, PB-10 | Update bicycle details or status |
| `DELETE` | `/api/bicycles/<id>` | Admin, Owner | PB-09 | Safe delete or deactivate bicycle |
| `POST` | `/api/rentals` | Customer | PB-12, PB-13 | Initiate bicycle rental (atomic) |
| `GET` | `/api/rentals/active` | Customer | PB-12, PB-14 | Retrieve customer's active rental |
| `POST` | `/api/rentals/<id>/return` | Customer, Admin | PB-15, PB-16 | Return bicycle, calculate fare, record payment |
| `GET` | `/api/rentals` | Authenticated | PB-14 | List rental history |
| `GET` | `/api/payments` | Authenticated | PB-17 | Retrieve simulated payment transactions |
| `GET` | `/api/admin/dashboard` | Admin | PB-04 | Platform KPIs and aggregate metrics |
| `GET` | `/api/admin/owners` | Admin | PB-05 | List rental owners with status |
| `POST` | `/api/admin/owners/<id>/status` | Admin | PB-05 | Approve or Reject rental owner |
| `GET` | `/api/qa/backlog` | Public | PB-01–24 | Complete 24 backlog items with story points |
| `GET` | `/api/qa/complexity` | Public | PB-22 | Live Radon McCabe cyclomatic complexity stats |
| `GET` | `/api/qa/coverage` | Public | PB-21 | Statement test coverage metrics |
| `POST` | `/api/qa/run-workflow` | Public | PB-23 | Automated Key UI Workflow Executor |

---

## Jira Backlog Traceability (PB-01 to PB-24)

All 24 user stories across 4 Sprints are fully implemented and verified. For detailed acceptance criteria and mapping to models, services, frontend, and tests, see [docs/JIRA_BACKLOG_MAPPING.md](docs/JIRA_BACKLOG_MAPPING.md).

| Sprint | Task ID | Backlog Task | Priority | SP | Status | Verification Target |
| :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| **Sprint 1** | `PB-01` | Set Up Flask Project and MySQL Database | Highest | 3 | Complete | `backend/app.py`, `backend/database/db.py`, `run.py` |
| **Sprint 1** | `PB-02` | User Registration and Login | Highest | 5 | Complete | `tests/test_auth.py`, `frontend/login.html`, `register.html` |
| **Sprint 1** | `PB-03` | Password Hashing and Validation | Highest | 3 | Complete | `backend/services/auth_service.py`, `backend/utils/validators.py` |
| **Sprint 1** | `PB-04` | Role-Based Access Control (RBAC) | High | 5 | Complete | `backend/utils/auth_middleware.py`, `tests/test_admin.py` |
| **Sprint 1** | `PB-05` | Rental Owner Verification by Admin | Medium | 3 | Complete | `backend/routes/admin_routes.py`, `tests/test_admin.py` |
| **Sprint 2** | `PB-06` | Create and Manage Rental Stations | High | 3 | Complete | `backend/routes/station_routes.py`, `tests/test_stations.py` |
| **Sprint 2** | `PB-07` | Track Station Capacity and Bicycle Counts | Medium | 5 | Complete | `tests/test_bicycles.py`, `tests/test_rentals.py` |
| **Sprint 2** | `PB-08` | Create Bicycle Database Models | Highest | 3 | Complete | `backend/models/bicycle.py`, `database/schema.sql` |
| **Sprint 2** | `PB-09` | Add, Edit and Delete Bicycle Records | High | 5 | Complete | `backend/routes/bicycle_routes.py`, `frontend/owner/dashboard.html` |
| **Sprint 2** | `PB-10` | Manage Bicycle Status | High | 3 | Complete | `backend/services/bicycle_service.py`, `tests/test_bicycles.py` |
| **Sprint 2** | `PB-11` | Search Available Bicycles by Station | High | 5 | Complete | `frontend/stations.html`, `frontend/index.html` |
| **Sprint 3** | `PB-12` | Implement Bicycle Rental Workflow | Highest | 5 | Complete | `backend/services/rental_service.py`, `tests/test_rentals.py` |
| **Sprint 3** | `PB-13` | Prevent Duplicate Active Rentals | Highest | 5 | Complete | `tests/test_rentals.py::test_prevent_double_rental` |
| **Sprint 3** | `PB-14` | Record Rental Start and Return Timestamps | High | 3 | Complete | `backend/models/rental.py`, `tests/test_rentals.py` |
| **Sprint 3** | `PB-15` | Calculate Rental Duration and Fare | High | 5 | Complete | `backend/services/rental_service.py`, `tests/test_fare.py` |
| **Sprint 3** | `PB-16` | Update Bicycle Status After Return | High | 3 | Complete | `backend/services/rental_service.py`, `tests/test_rentals.py` |
| **Sprint 3** | `PB-17` | Maintain Simulated Payment Ledger and Status | High | 5 | Complete | `backend/models/payment.py`, `backend/routes/payment_routes.py` |
| **Sprint 4** | `PB-18` | Test Authentication and Security Features | High | 3 | Complete | `tests/test_auth.py` (5 automated tests) |
| **Sprint 4** | `PB-19` | Test Bicycle Inventory and Station Features | High | 5 | Complete | `tests/test_bicycles.py`, `tests/test_stations.py` (9 tests) |
| **Sprint 4** | `PB-20` | Test Rental, Return and Fare Calculation | Highest | 5 | Complete | `tests/test_rentals.py`, `tests/test_fare.py` (5 tests) |
| **Sprint 4** | `PB-21` | Generate Code Coverage Report | Medium | 3 | Complete | `pytest-cov`, `reports/coverage.txt`, `reports/coverage_html/` |
| **Sprint 4** | `PB-22` | Perform Cyclomatic Complexity Analysis | Low | 2 | Complete | `Radon` CC/MI analysis, `reports/complexity.txt` |
| **Sprint 4** | `PB-23` | Automate a Key UI Workflow | Medium | 5 | Complete | `tests/ui/test_ui_selenium.py`, `tests/test_ui_workflow.py` |
| **Sprint 4** | `PB-24` | Fix Defects and Perform Integration Testing | Highest | 5 | Complete | 35/35 tests passing, integration verification in `reports/` |
| **Total** | | **All 4 Sprints · 24 Backlog Items** | | **97 SP** | **100% Done** | |

---

## Testing, Coverage & QA Reports

### 1. Run Complete Test Suite (35 Tests)
```powershell
python -m pytest tests/ -v
```

### 2. Run Test Coverage Analysis (PB-21)
Generates terminal coverage and HTML report:
```powershell
python -m pytest --cov=backend --cov-report=term --cov-report=html:reports/coverage_html tests/
```
Text report is saved to `reports/coverage.txt`. Current overall coverage is **77%**.

### 3. Run Cyclomatic Complexity Analysis with Radon (PB-22)
```powershell
# Cyclomatic Complexity
radon cc backend -s -a

# Maintainability Index
radon mi backend -s
```
Summary is saved in `reports/complexity.txt`:
- Total blocks analyzed: 98
- Average complexity grade: **A (4.23)**
- Maintainability grade: **A (100.0)** across all modules

### 4. Run Automated Key UI Workflow with Selenium (PB-23)
```powershell
python -m pytest tests/ui/test_ui_selenium.py -v
```
Exercises the customer journey using Selenium Headless Chrome against a live local server.

---

## DevOps & Jenkins CI Pipeline

## DevOps CI

This project uses Git, GitHub, and Jenkins to automate continuous integration and testing.

The project includes a declarative `Jenkinsfile` ready for continuous integration:

1. **Checkout**: Pulls the repository.
2. **Setup**: Prepares Python environment and installs `requirements.txt`.
3. **Database**: Seeds SQLite test database.
4. **Test & Coverage**: Runs `pytest --cov=backend --junitxml=junit.xml`.
5. **Quality Gate**: Runs Radon complexity validation.
6. **Publish**: Archives test reports and coverage results.
