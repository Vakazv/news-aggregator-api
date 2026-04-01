# News Aggregator API

Backend service for storing, filtering and caching news content.

## Stack
- Python 3.11
- FastAPI
- PostgreSQL
- Redis
- Docker
- pytest

## Features
- CRUD for news
- Filtering by source and tag
- Pagination with `limit` and `offset`
- REST API
- Redis caching for news list
- Docker Compose setup
- Basic API tests

## Project structure
- `app/routes/` — API endpoints
- `app/models.py` — database models
- `app/schemas.py` — Pydantic schemas
- `app/crud.py` — data access logic
- `app/cache.py` — Redis cache layer
- `tests/` — tests

## Run locally

```bash
docker compose up --build