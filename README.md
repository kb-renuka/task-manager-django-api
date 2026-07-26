# Task Manager REST API

A full-featured task management REST API built with Django and Django REST Framework, featuring JWT authentication, filtering, pagination, and a complete admin interface. Deployed live on Render with PostgreSQL.

**Live API:** https://task-manager-django-api-rmyj.onrender.com
**API Docs (Swagger):** https://task-manager-django-api-rmyj.onrender.com/api/docs/
**Admin Panel:** https://task-manager-django-api-rmyj.onrender.com/admin/

> Note: hosted on Render's free tier, so the first request after inactivity may take up to 50 seconds while the instance spins back up.

---

## Tech Stack

- **Backend:** Django 5.0, Django REST Framework
- **Auth:** JWT (djangorestframework-simplejwt) — access + refresh tokens, blacklisting on logout
- **Database:** PostgreSQL (production), SQLite (local dev)
- **Docs:** drf-yasg (Swagger / OpenAPI)
- **Filtering & Pagination:** django-filter, custom pagination class
- **Deployment:** Render, Gunicorn, WhiteNoise for static files

## Key Features

- **JWT Authentication** — register, login, token refresh, token verify, logout with blacklisting
- **Full CRUD** for Tasks and Categories, scoped per authenticated user
- **Task workflow actions** — mark complete, reopen, list overdue tasks, dashboard stats
- **Filtering, search, and ordering** on task list endpoints
- **Pagination** on all list endpoints
- **Rate limiting** — throttling for authenticated and anonymous users
- **Custom exception handling** for consistent API error responses
- **Django Admin** fully configured for Tasks and Categories with list filters and search

## API Overview

| Endpoint | Method | Description |
|---|---|---|
| `/api/auth/register/` | POST | Register a new user |
| `/api/auth/login/` | POST | Obtain JWT access & refresh tokens |
| `/api/auth/login/refresh/` | POST | Refresh access token |
| `/api/auth/logout/` | POST | Blacklist refresh token |
| `/api/auth/profile/` | GET/PUT/PATCH | View or update user profile |
| `/api/categories/` | GET/POST | List or create categories |
| `/api/categories/{id}/` | GET/PUT/PATCH/DELETE | Manage a single category |
| `/api/tasks/` | GET/POST | List (paginated, filterable) or create tasks |
| `/api/tasks/{id}/` | GET/PUT/PATCH/DELETE | Manage a single task |
| `/api/tasks/{id}/complete/` | PATCH | Mark a task as done |
| `/api/tasks/{id}/reopen/` | PATCH | Move a task back to TODO |
| `/api/tasks/overdue/` | GET | List tasks past due date and not done |
| `/api/tasks/stats/` | GET | Dashboard counts by status/priority |

Full interactive documentation with request/response schemas is available at `/api/docs/`.

## Local Setup

```bash
# Clone the repo
git clone https://github.com/kb-renuka/task-manager-django-api.git
cd task-manager-django-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Fill in SECRET_KEY and other values in .env

# Run migrations
python manage.py migrate

# Create a superuser (for admin access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

The API will be available at `http://localhost:8000/`, with docs at `http://localhost:8000/api/docs/`.

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for local dev, `False` in production |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts |
| `DATABASE_URL` | PostgreSQL connection string (production) |
| `CORS_ALLOW_ALL` | Whether to allow all CORS origins |

## Deployment

Deployed on [Render](https://render.com) as a web service, with a managed PostgreSQL instance. Build pipeline runs `pip install`, `collectstatic`, and `migrate` on every deploy; static files are served via WhiteNoise.

## Author

Built by [kb-renuka](https://github.com/kb-renuka)
