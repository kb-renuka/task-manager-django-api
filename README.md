# Task Management REST API — Django

A Django REST Framework microservice for managing tasks — full CRUD, JWT authentication, pagination, filtering, and search. Django/DRF counterpart to the Spring Boot task-manager-api project.

## Tech Stack
- Django 5 + Django REST Framework
- JWT auth via djangorestframework-simplejwt (access + refresh tokens, blacklist on logout)
- django-filter for query filtering, DRF SearchFilter/OrderingFilter
- SQLite by default, drop-in Postgres via env vars
- Swagger docs via drf-yasg

## Architecture
Layered like the Spring Boot version — models (entity/repository layer) then serializers (DTO/validation layer) then views (controller/service layer), with permissions.py enforcing per-user ownership and pagination.py / filters.py as shared concerns.

- taskmanager/ — project settings, root urls
- accounts/ — registration, login, profile, JWT issuance
- tasks/ — Task & Category models, views, serializers, filters

## Setup

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

API is served at http://localhost:8000/api/. Swagger docs at /api/docs/. Django admin at /admin/.

## Endpoints

### Auth (/api/auth/)
| Method | Endpoint | Description |
|---|---|---|
| POST | /register/ | Create account, returns JWT pair |
| POST | /login/ | Obtain access + refresh tokens |
| POST | /login/refresh/ | Refresh an access token |
| POST | /login/verify/ | Verify a token is valid |
| POST | /logout/ | Blacklist refresh token |
| GET/PUT/PATCH | /profile/ | View or update the logged-in user |

### Categories (/api/categories/)
| Method | Endpoint | Description |
|---|---|---|
| GET | / | List your categories (paginated) |
| POST | / | Create a category |
| GET | /{id}/ | Retrieve a category |
| PUT/PATCH | /{id}/ | Update a category |
| DELETE | /{id}/ | Delete a category |

### Tasks (/api/tasks/)
| Method | Endpoint | Description |
|---|---|---|
| GET | / | List tasks — paginated, filterable, searchable |
| POST | / | Create a task |
| GET | /{id}/ | Retrieve a task |
| PUT/PATCH | /{id}/ | Update a task |
| DELETE | /{id}/ | Delete a task |
| PATCH | /{id}/complete/ | Mark a task done |
| PATCH | /{id}/reopen/ | Move a task back to TODO |
| GET | /overdue/ | Tasks past due date, not done |
| GET | /stats/ | Dashboard counts |

Query params on GET /api/tasks/: status, priority, category, due_before, due_after, created_after, search, ordering, page, page_size.

## Models

**Task** — title, description, status (TODO/IN_PROGRESS/DONE), priority (LOW/MEDIUM/HIGH), due_date, category (FK), owner (FK to User), completed_at, timestamps.

**Category** — name, color, owner (FK to User), unique per user.

Every task and category is scoped to its owner — users only ever see and modify their own data.

## Testing

    python manage.py test

## Deployment
Set DEBUG=False, a real SECRET_KEY, and proper ALLOWED_HOSTS in .env. Point DB_* at Postgres. Run with gunicorn taskmanager.wsgi:application behind your platform of choice.
