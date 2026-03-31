# Django REST API

Production-style REST API built with Django, DRF, PostgreSQL, and Docker.

## Tech Stack
- Django 4.2 + Django REST Framework
- PostgreSQL 15 with composite indexes
- JWT auth via djangorestframework-simplejwt
- Docker + Docker Compose
- Python 3.13

## Features
- Custom User model with email-based login
- JWT register, login, token refresh
- Product CRUD with per-user data isolation
- PostgreSQL query optimization with EXPLAIN ANALYZE
- Raw SQL + Django ORM comparison

## Run It
\`\`\`bash
cp .env.example .env   # fill in your values
docker-compose up --build
docker-compose exec web python manage.py createsuperuser
\`\`\`

## API Endpoints
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/v1/register/ | None | Register |
| POST | /api/v1/auth/token/ | None | Login |
| GET | /api/v1/profile/ | JWT | Own profile |
| GET | /api/v1/products/ | JWT | List products |
| POST | /api/v1/products/ | JWT | Create product |
| GET | /api/v1/products/stats/ | JWT | Aggregated stats |