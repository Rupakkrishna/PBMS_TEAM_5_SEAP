# Public Bicycle Rental Management System (PBRMS)
## Jira Backlog Mapping & Traceability Matrix (PB-01 to PB-24)

This document provides a comprehensive, bidirectional traceability matrix linking all 24 Jira Backlog Items (total **97 Story Points** across 4 Sprints) to their respective backend services, API endpoints, SQLAlchemy ORM models, frontend user interfaces, and automated test suites.

---

### Sprint Summary

| Sprint | Focus Area | Story Points | Tasks | Status |
|---|---|:---:|:---:|:---:|
| **Sprint 1** | Project Setup & Authentication | 19 SP | PB-01 to PB-05 | **100% Completed** |
| **Sprint 2** | Station & Bicycle Inventory Management | 24 SP | PB-06 to PB-11 | **100% Completed** |
| **Sprint 3** | Rental, Return, Fare & Simulated Payment | 26 SP | PB-12 to PB-17 | **100% Completed** |
| **Sprint 4** | Testing, Quality Assurance & Automation | 28 SP | PB-18 to PB-24 | **100% Completed** |
| **Total** | **Full System Lifecycle** | **97 SP** | **24 Tasks** | **100% Completed** |

---

## Detailed Task-by-Task Mapping

### Sprint 1: Project Setup & Authentication (19 SP)

#### PB-01: Set Up Flask Project and MySQL Database
* **Priority**: Highest | **Story Points**: 3 | **Status**: Complete
* **Acceptance Criteria**: Flask application configured with MySQL connectivity (with zero-config SQLite fallback for testing/portability), environment variable configuration (`.env.example`), automatic schema creation, and database connection pooling/error recovery.
* **SQLAlchemy Models**: [backend/models/__init__.py](file:///c:/Users/USER/Seap/backend/models/__init__.py), [backend/extensions.py](file:///c:/Users/USER/Seap/backend/extensions.py)
* **Backend Services & Routes**:
  - `backend/app.py`: `create_app()` factory
  - `backend/config.py`: `Config`, `DevelopmentConfig`, `TestingConfig`, `ProductionConfig`
  - `backend/database/db.py`: `get_db()`, `execute_db()`, `query_db()`, `init_db_schema()`, `transaction_scope()`
  - `run.py`: CLI entry point supporting `--init-db`, `--seed`, `--host`, `--port`
* **Frontend**: Global responsive UI wrapper, [frontend/index.html](file:///c:/Users/USER/Seap/frontend/index.html), API connection checks.
* **Automated Tests**:
  - `tests/conftest.py`: `app`, `init_db` fixtures
  - `tests/test_auth.py`: `test_unauthorized_endpoint_access`

---

#### PB-02: User Registration and Login
* **Priority**: Highest | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Unified and role-specific registration and login for Customers (`user`) and Rental Owners (`rental_owner`), generating JWT tokens, tracking active session state, and displaying contextual notifications.
* **SQLAlchemy Models**: [backend/models/user.py](file:///c:/Users/USER/Seap/backend/models/user.py) (`User`, `RentalOwner`, `Admin`)
* **Backend Services & Routes**:
  - `POST /api/auth/register`: Register new customer or owner
  - `POST /api/auth/login`: Authenticate and issue JWT
  - `POST /api/auth/logout`: Terminate session
  - `GET /api/auth/me`: Fetch authenticated user profile
  - `backend/services/auth_service.py`: `register_user()`, `register_owner()`, `login_user()`
* **Frontend**:
  - [frontend/register.html](file:///c:/Users/USER/Seap/frontend/register.html): Dynamic role toggle, phone validation, password meter
  - [frontend/login.html](file:///c:/Users/USER/Seap/frontend/login.html): Quick demo login buttons for Customer, Owner, Admin, and Pending Owner
  - [frontend/js/auth.js](file:///c:/Users/USER/Seap/frontend/js/auth.js): JWT token storage (`localStorage`), redirect routers
* **Automated Tests**:
  - `tests/test_auth.py`: `test_user_registration`, `test_rental_owner_registration`, `test_login_success`, `test_invalid_login`

---

#### PB-03: Password Hashing and Validation
* **Priority**: Highest | **Story Points**: 3 | **Status**: Complete
* **Acceptance Criteria**: Passwords hashed with bcrypt (salt generation, never stored plaintext). Registration enforces at least 8 characters, upper, lower, digit, and special character. Real-time visual feedback on UI.
* **SQLAlchemy Models**: [backend/models/user.py](file:///c:/Users/USER/Seap/backend/models/user.py)
* **Backend Services & Routes**:
  - `backend/services/auth_service.py`: `hash_password()`, `check_password()`
  - `backend/utils/validators.py`: `validate_password()`
* **Frontend**:
  - [frontend/register.html](file:///c:/Users/USER/Seap/frontend/register.html): Interactive password strength bar, live rule checklists (length, capital, number, special symbol)
  - [frontend/js/auth.js](file:///c:/Users/USER/Seap/frontend/js/auth.js): Event listeners for `input` on password field
* **Automated Tests**:
  - `tests/test_auth.py`: `test_invalid_login`, `test_user_registration`

---

#### PB-04: Role-Based Access Control (RBAC)
* **Priority**: High | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Strict server-side access controls enforcing permissions for Customer (`user`), Rental Owner (`rental_owner`), and Platform Administrator (`admin`). Protected endpoints reject unauthorized roles with HTTP 401/403.
* **SQLAlchemy Models**: [backend/models/user.py](file:///c:/Users/USER/Seap/backend/models/user.py)
* **Backend Services & Routes**:
  - `backend/utils/auth_middleware.py`: `@token_required`, `@role_required(*allowed_roles)`
  - All admin routes (`/api/admin/*`) restricted to `admin`
  - Bicycle mutation routes restricted to `rental_owner` or `admin`
  - Rental creation restricted to `user`
* **Frontend**:
  - Dynamic navigation bars in [frontend/user/dashboard.html](file:///c:/Users/USER/Seap/frontend/user/dashboard.html), [frontend/owner/dashboard.html](file:///c:/Users/USER/Seap/frontend/owner/dashboard.html), [frontend/admin/dashboard.html](file:///c:/Users/USER/Seap/frontend/admin/dashboard.html)
  - Route guards in JavaScript redirecting unauthenticated users to `/login.html`
* **Automated Tests**:
  - `tests/test_auth.py`: `test_unauthorized_endpoint_access`
  - `tests/test_admin.py`: `test_admin_dashboard_unauthorized`
  - `tests/test_stations.py`: `test_create_station_unauthorized`

---

#### PB-05: Rental Owner Verification by Admin
* **Priority**: Medium | **Story Points**: 3 | **Status**: Complete
* **Acceptance Criteria**: Rental owner accounts require admin approval (`Pending`, `Approved`, `Rejected`). Unverified owners are prohibited from adding bicycles or performing restricted owner actions. Admin dashboard provides 1-click approval/rejection.
* **SQLAlchemy Models**: [backend/models/user.py](file:///c:/Users/USER/Seap/backend/models/user.py) (`RentalOwner.approval_status`)
* **Backend Services & Routes**:
  - `GET /api/admin/owners`: List all owners with status filtering
  - `POST /api/admin/owners/<id>/status`: Update approval status to Approved/Rejected
  - `backend/routes/bicycle_routes.py`: Enforces owner approval verification before bicycle creation
* **Frontend**:
  - [frontend/admin/dashboard.html](file:///c:/Users/USER/Seap/frontend/admin/dashboard.html): "Rental Owners" tab with badge indicators and Approve/Reject action buttons
  - [frontend/owner/dashboard.html](file:///c:/Users/USER/Seap/frontend/owner/dashboard.html): Banner warning when status is `Pending` or `Rejected`
* **Automated Tests**:
  - `tests/test_admin.py`: `test_admin_list_owners`, `test_admin_approve_and_reject_owner`

---

### Sprint 2: Station & Bicycle Inventory Management (24 SP)

#### PB-06: Create and Manage Rental Stations
* **Priority**: High | **Story Points**: 3 | **Status**: Complete
* **Acceptance Criteria**: Authorized users can view, create, edit, and delete docking stations, storing name, physical location, total capacity, and available slots.
* **SQLAlchemy Models**: [backend/models/station.py](file:///c:/Users/USER/Seap/backend/models/station.py) (`Station`)
* **Backend Services & Routes**:
  - `GET /api/stations`: Retrieve all stations
  - `GET /api/stations/<id>`: Get station details
  - `POST /api/stations`: Create station (Admin only)
  - `PUT /api/stations/<id>`: Update station (Admin only)
  - `DELETE /api/stations/<id>`: Delete station (Admin only)
  - `backend/services/station_service.py`: CRUD operations
* **Frontend**:
  - [frontend/stations.html](file:///c:/Users/USER/Seap/frontend/stations.html): Public station catalog with capacity meters
  - [frontend/admin/dashboard.html](file:///c:/Users/USER/Seap/frontend/admin/dashboard.html): Station management table with modal CRUD
* **Automated Tests**:
  - `tests/test_stations.py`: `test_list_stations`, `test_get_station_by_id`, `test_create_station_admin`, `test_update_and_delete_station`

---

#### PB-07: Track Station Capacity and Bicycle Counts
* **Priority**: Medium | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Live tracking of station capacity, available bicycles, and occupied slots. Return operation rejects bicycles when station capacity is reached (`Station has reached maximum capacity`).
* **SQLAlchemy Models**: [backend/models/station.py](file:///c:/Users/USER/Seap/backend/models/station.py)
* **Backend Services & Routes**:
  - `backend/services/station_service.py`: `update_station_counts()`, `get_station_by_id()`
  - `backend/services/rental_service.py`: Capacity validation guard during return
* **Frontend**:
  - Capacity progress bar with color thresholds (Green < 75%, Yellow 75–99%, Red 100% Full)
  - Return modal displays available dock spaces in real-time
* **Automated Tests**:
  - `tests/test_bicycles.py`: `test_station_availability_update_and_capacity`
  - `tests/test_rentals.py`: `test_return_bicycle_capacity_limit`

---

#### PB-08: Create Bicycle Database Models
* **Priority**: Highest | **Story Points**: 3 | **Status**: Complete
* **Acceptance Criteria**: Relational schema and SQLAlchemy model for bicycles storing unique identifier (`bicycle_number`), bike type (`City`, `Mountain`, `Electric`, `Road`), hourly rental rate, status (`Available`, `Rented`, `Maintenance`, `Inactive`), foreign keys to `rental_owner` and `station`.
* **SQLAlchemy Models**: [backend/models/bicycle.py](file:///c:/Users/USER/Seap/backend/models/bicycle.py) (`Bicycle`)
* **Backend Services & Routes**:
  - `backend/database/db.py`: `init_db_schema()` table definition
  - `backend/models/bicycle.py`: Full ORM model with relationships and JSON serializer
* **Frontend**: Bicycle details cards displaying ID, Type, Hourly Rate, and Station dock.
* **Automated Tests**:
  - `tests/test_bicycles.py`: `test_bicycle_availability`

---

#### PB-09: Add, Edit and Delete Bicycle Records
* **Priority**: High | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Authorized rental owners can register new bicycles, edit bicycle details (rate, type, location), and safely delete records (or deactivate if associated with rental history).
* **SQLAlchemy Models**: [backend/models/bicycle.py](file:///c:/Users/USER/Seap/backend/models/bicycle.py)
* **Backend Services & Routes**:
  - `POST /api/bicycles`: Add new bicycle
  - `PUT /api/bicycles/<id>`: Update bicycle attributes
  - `DELETE /api/bicycles/<id>`: Delete bicycle or soft-deactivate
  - `backend/services/bicycle_service.py`: CRUD methods
* **Frontend**:
  - [frontend/owner/dashboard.html](file:///c:/Users/USER/Seap/frontend/owner/dashboard.html): "Add New Bicycle" modal, "Edit Bicycle" modal, and Delete confirmation
* **Automated Tests**:
  - `tests/test_bicycles.py`: `test_bicycle_availability`

---

#### PB-10: Manage Bicycle Status
* **Priority**: High | **Story Points**: 3 | **Status**: Complete
* **Acceptance Criteria**: Enforce strict lifecycle transitions (`Available` <-> `Rented`, `Available` <-> `Maintenance`, `Inactive`). Prevent bikes under maintenance or rented from being offered for new rentals.
* **SQLAlchemy Models**: [backend/models/bicycle.py](file:///c:/Users/USER/Seap/backend/models/bicycle.py)
* **Backend Services & Routes**:
  - `backend/services/bicycle_service.py`: `update_bicycle_status()`
  - Transition validation logic enforcing valid state changes
* **Frontend**:
  - [frontend/owner/dashboard.html](file:///c:/Users/USER/Seap/frontend/owner/dashboard.html): 1-click status toggle button (`Set Maintenance` / `Set Available`)
* **Automated Tests**:
  - `tests/test_bicycles.py`: `test_bicycle_status_transition`

---

#### PB-11: Search Available Bicycles by Station
* **Priority**: High | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Users can filter bicycles by station ID or search by keyword across bike number, station name, location, and bike type. Clear empty states when no bicycles match.
* **SQLAlchemy Models**: [backend/models/bicycle.py](file:///c:/Users/USER/Seap/backend/models/bicycle.py), [backend/models/station.py](file:///c:/Users/USER/Seap/backend/models/station.py)
* **Backend Services & Routes**:
  - `GET /api/bicycles/available?station_id=<id>&search=<query>`: Dynamic SQL filtering
  - `backend/services/bicycle_service.py`: `get_available_bicycles(station_id, search)`
* **Frontend**:
  - [frontend/index.html](file:///c:/Users/USER/Seap/frontend/index.html): Public bicycle search explorer
  - [frontend/stations.html](file:///c:/Users/USER/Seap/frontend/stations.html): Dedicated search and station browser
  - [frontend/user/dashboard.html](file:///c:/Users/USER/Seap/frontend/user/dashboard.html): Real-time search box filtering available bikes
* **Automated Tests**:
  - `tests/test_bicycles.py`: `test_bicycle_availability`
  - `tests/test_ui_workflow.py`: `test_automated_key_ui_workflow`

---

### Sprint 3: Rental, Return, Fare & Simulated Payment (26 SP)

#### PB-12: Implement Bicycle Rental Workflow
* **Priority**: Highest | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Authenticated customers can rent an available bicycle. The system atomically creates an active rental, updates bicycle status to `Rented`, decrements station count, and displays the active rental on the dashboard.
* **SQLAlchemy Models**: [backend/models/rental.py](file:///c:/Users/USER/Seap/backend/models/rental.py), [backend/models/bicycle.py](file:///c:/Users/USER/Seap/backend/models/bicycle.py)
* **Backend Services & Routes**:
  - `POST /api/rentals`: Initiate bicycle rental
  - `backend/services/rental_service.py`: `create_rental()` with `transaction_scope()`
* **Frontend**:
  - [frontend/user/dashboard.html](file:///c:/Users/USER/Seap/frontend/user/dashboard.html): "Rent Now" action button, active rental banner displaying timer and vehicle details
* **Automated Tests**:
  - `tests/test_rentals.py`: `test_bicycle_rental_lifecycle`
  - `tests/ui/test_ui_selenium.py`: `test_selenium_key_ui_workflow`

---

#### PB-13: Prevent Duplicate Active Rentals
* **Priority**: Highest | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Prevent concurrent or duplicate rentals. A user cannot rent multiple bicycles at once, and a bicycle cannot be rented by multiple users simultaneously.
* **SQLAlchemy Models**: [backend/models/rental.py](file:///c:/Users/USER/Seap/backend/models/rental.py)
* **Backend Services & Routes**:
  - `backend/services/rental_service.py`: Pre-condition check for `has_active_rental(user_id)` and bicycle status `Available` inside an atomic transaction.
* **Frontend**:
  - [frontend/user/dashboard.html](file:///c:/Users/USER/Seap/frontend/user/dashboard.html): All "Rent Now" buttons disabled and badged with *"Active Rental in Progress"* when user already has an active trip.
* **Automated Tests**:
  - `tests/test_rentals.py`: `test_prevent_double_rental`

---

#### PB-14: Record Rental Start and Return Timestamps
* **Priority**: High | **Story Points**: 3 | **Status**: Complete
* **Acceptance Criteria**: Accurately records UTC start timestamp upon rental initiation, and return timestamp upon docking. Timestamps stored consistently in ISO-8601 format.
* **SQLAlchemy Models**: [backend/models/rental.py](file:///c:/Users/USER/Seap/backend/models/rental.py) (`Rental.start_time`, `Rental.end_time`)
* **Backend Services & Routes**:
  - `backend/services/rental_service.py`: Datetime capture via `datetime.now(timezone.utc)`
* **Frontend**:
  - Live elapsed time counter on user dashboard; start and return timestamps on rental receipts and rental history table.
* **Automated Tests**:
  - `tests/test_rentals.py`: `test_bicycle_rental_lifecycle`

---

#### PB-15: Calculate Rental Duration and Fare
* **Priority**: High | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Configurable transparent fare formula:
  $$\text{Fare} = \text{Base Unlock Fee (\$1.50)} + \left(\lceil\text{Duration (min)} / 60\rceil \times \text{Hourly Rate}\right)$$
  Minimum fare applied for short trips; duration and fare calculation displayed transparently.
* **SQLAlchemy Models**: [backend/models/rental.py](file:///c:/Users/USER/Seap/backend/models/rental.py) (`Rental.total_fare`)
* **Backend Services & Routes**:
  - `backend/services/rental_service.py`: `calculate_fare(start_time, end_time, hourly_rate)`
* **Frontend**:
  - Fare breakdown modal showing unlock fee, billed hours, rate per hour, and total sum.
* **Automated Tests**:
  - `tests/test_fare.py`: `test_fare_calculation`

---

#### PB-16: Update Bicycle Status After Return
* **Priority**: High | **Story Points**: 3 | **Status**: Complete
* **Acceptance Criteria**: Return workflow prompts customer to select destination station. System verifies destination station capacity, updates rental to `Completed`, sets bicycle status back to `Available`, increments station bicycle count, and creates payment record atomically.
* **SQLAlchemy Models**: [backend/models/rental.py](file:///c:/Users/USER/Seap/backend/models/rental.py), [backend/models/station.py](file:///c:/Users/USER/Seap/backend/models/station.py)
* **Backend Services & Routes**:
  - `POST /api/rentals/<id>/return`: Return bicycle endpoint
  - `backend/services/rental_service.py`: `return_rental()` transaction
* **Frontend**:
  - [frontend/user/dashboard.html](file:///c:/Users/USER/Seap/frontend/user/dashboard.html): "Return Bicycle" modal with station picker and capacity indicators
* **Automated Tests**:
  - `tests/test_rentals.py`: `test_return_bicycle`, `test_return_bicycle_capacity_limit`

---

#### PB-17: Maintain Simulated Payment Ledger and Status
* **Priority**: High | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Transparent simulated payment ledger recording `rental_id`, `amount`, `payment_method`, simulated status (`Paid (Simulated)`, `Pending`, `Failed (Simulated)`), and transaction reference. UI prominently highlights that payments are simulated.
* **SQLAlchemy Models**: [backend/models/payment.py](file:///c:/Users/USER/Seap/backend/models/payment.py) (`Payment`)
* **Backend Services & Routes**:
  - `GET /api/payments`: List user payments
  - `GET /api/payments/<rental_id>`: Fetch payment for specific rental
  - `POST /api/payments`: Process simulated checkout
  - `backend/services/payment_service.py`: `create_simulated_payment()`
* **Frontend**:
  - Rental Completion modal displaying "Simulated Receipt", payment method, and simulated payment badge.
  - Payment Ledger table in user dashboard.
* **Automated Tests**:
  - `tests/test_rentals.py`: `test_bicycle_rental_lifecycle`
  - `tests/test_ui_workflow.py`: `test_automated_key_ui_workflow`

---

### Sprint 4: Testing, Quality Assurance & Automation (28 SP)

#### PB-18: Test Authentication and Security Features
* **Priority**: High | **Story Points**: 3 | **Status**: Complete
* **Acceptance Criteria**: Automated unit and security test suite covering password hashing, credential validation, token generation, role verification, and unauthorized endpoint access prevention.
* **Automated Tests**:
  - `tests/test_auth.py`:
    - `test_user_registration`
    - `test_rental_owner_registration`
    - `test_login_success`
    - `test_invalid_login`
    - `test_unauthorized_endpoint_access`

---

#### PB-19: Test Bicycle Inventory and Station Features
* **Priority**: High | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Comprehensive test coverage for bicycle querying, station capacity increments/decrements, bicycle lifecycle status transitions, and station CRUD.
* **Automated Tests**:
  - `tests/test_bicycles.py`:
    - `test_bicycle_availability`
    - `test_bicycle_status_transition`
    - `test_station_availability_update_and_capacity`
  - `tests/test_stations.py`:
    - `test_list_stations`
    - `test_get_station_by_id`
    - `test_get_station_bicycles`
    - `test_create_station_admin`
    - `test_create_station_unauthorized`
    - `test_update_and_delete_station`

---

#### PB-20: Test Rental, Return and Fare Calculation
* **Priority**: Highest | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Test rental initiation, double-rental prevention, return handling, station capacity checks upon return, and mathematical precision of the tiered fare calculation algorithm.
* **Automated Tests**:
  - `tests/test_rentals.py`:
    - `test_bicycle_rental_lifecycle`
    - `test_prevent_double_rental`
    - `test_return_bicycle`
    - `test_return_bicycle_capacity_limit`
  - `tests/test_fare.py`:
    - `test_fare_calculation` (exact duration, hour rounding, base fee)

---

#### PB-21: Generate Code Coverage Report
* **Priority**: Medium | **Story Points**: 3 | **Status**: Complete
* **Acceptance Criteria**: Measure branch and statement test coverage across the backend using `pytest-cov`. Output both text report (`reports/coverage.txt`) and interactive HTML report (`reports/coverage_html/index.html`). REST endpoint `/api/qa/coverage` surfaces live stats to UI.
* **Backend Routes**:
  - `GET /api/qa/coverage`: Returns statements, missed lines, and overall percentage
* **Reports Generated**:
  - `reports/coverage.txt` (77% overall coverage across all modules)
  - `reports/coverage_html/index.html`
* **Automated Tests**:
  - `tests/test_qa.py`: `test_qa_coverage_endpoint`

---

#### PB-22: Perform Cyclomatic Complexity Analysis
* **Priority**: Low | **Story Points**: 2 | **Status**: Complete
* **Acceptance Criteria**: Execute cyclomatic complexity, maintainability index (MI), and raw code metrics using `Radon`. Save detailed report to `reports/complexity.txt`. Expose REST endpoint `/api/qa/complexity` for real-time dashboard visualization.
* **Backend Routes**:
  - `GET /api/qa/complexity`: Returns module-by-module complexity grade and maintainability score
* **Reports Generated**:
  - `reports/complexity.txt` (Average Complexity: **A (4.23)**; Maintainability Index: **A (100.0)**)
* **Automated Tests**:
  - `tests/test_qa.py`: `test_qa_complexity_endpoint`

---

#### PB-23: Automate a Key UI Workflow
* **Priority**: Medium | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Fully automated browser end-to-end test exercising the complete user journey: login as customer, browse available bicycles, initiate rental, verify active timer, return bicycle to destination station, verify simulated payment receipt, and confirm bicycle returned to station inventory.
* **Automated Tests**:
  - `tests/ui/test_ui_selenium.py`: `test_selenium_key_ui_workflow` (Genuine Selenium Headless Chrome driver)
  - `tests/test_ui_workflow.py`: `test_automated_key_ui_workflow` (Flask TestClient headless integration workflow)
  - `POST /api/qa/run-workflow`: Web-accessible interactive test executor

---

#### PB-24: Fix Defects and Perform Integration Testing
* **Priority**: Highest | **Story Points**: 5 | **Status**: Complete
* **Acceptance Criteria**: Comprehensive defect remediation across all modules (schema migrations, transaction rollback handling, concurrency locking, UI dropdown race conditions, and boundary capacity validation). All 30 unit, integration, and UI tests pass with zero failures.
* **Artifacts & Verification**:
  - 30 passed tests in `reports/test_results.txt`
  - Defect fixes documented and verified in `reports/` and `docs/`

