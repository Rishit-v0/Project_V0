# Django REST API — Production-Grade Backend

A multi-tenant REST API built with Django, DRF, PostgreSQL, and Docker.
Built as part of a backend engineering exercise after a gap.

## Tech Stack

- **Framework:** Django 4.2 + Django REST Framework
- **Database:** PostgreSQL 15 with composite indexes
- **Cache:** Redis 7 with django-redis
- **Auth:** JWT via djangorestframework-simplejwt
- **Containerization:** Docker + Docker Compose
- **Language:** Python 3.13

## Features

- Custom User model with email-based authentication
- JWT register, login, token refresh endpoints
- Product CRUD with per-user data isolation
- Redis caching with automatic cache invalidation on writes
- PostgreSQL query optimization with composite indexes
- Raw SQL + Django ORM comparison endpoint
- EXPLAIN ANALYZE verified query performance

## Project Structure

\`\`\`
Django_quickstart/
├── core/               # Django project settings and URLs
├── api/                # Main app — models, views, serializers, URLs
│   ├── migrations/     # Database migrations
│   ├── models.py       # User + Product models with indexes
│   ├── views.py        # ViewSets + APIViews with caching
│   ├── serializers.py  # DRF serializers with validation
│   └── urls.py         # URL routing
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
└── requirements.txt
\`\`\`

## Getting Started

### Prerequisites
- Docker Desktop installed and running

### Run the project

\`\`\`bash
# Clone the repo
git clone https://github.com/yourusername/Django_quickstart.git
cd Django_quickstart

# Copy env file and fill in your values
cp .env.example .env

# Build and start
docker-compose up --build

# Create superuser (in a new terminal)
docker-compose exec web python manage.py createsuperuser
\`\`\`

### API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/v1/register/ | None | Register new user |
| POST | /api/v1/auth/token/ | None | Login, get JWT |
| POST | /api/v1/auth/token/refresh/ | None | Refresh token |
| GET | /api/v1/profile/ | JWT | Get own profile |
| PUT | /api/v1/profile/ | JWT | Update profile |
| GET | /api/v1/products/ | JWT | List own products |
| POST | /api/v1/products/ | JWT | Create product |
| GET | /api/v1/products/{id}/ | JWT | Get product |
| PUT | /api/v1/products/{id}/ | JWT | Update product |
| DELETE | /api/v1/products/{id}/ | JWT | Delete product |
| GET | /api/v1/products/stats/ | JWT | Aggregated stats |

### Environment Variables

Copy `.env.example` to `.env` and fill in:

\`\`\`env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_NAME=TestDB
DATABASE_USER=postgres
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=db
DATABASE_PORT=5432
REDIS_URL=redis://redis:6379/1
\`\`\`

## Key Technical Decisions

**Why custom User model:** Django's default User model can't be changed after
the first migration. Always define a custom User model at project start.

**Why Redis caching:** Product list and stats queries are expensive on large
datasets. Cache invalidation on write ensures data consistency.

**Why composite indexes:** Filtering by (is_active, created_by) together
is the most common query pattern — a composite index covers it in one lookup.