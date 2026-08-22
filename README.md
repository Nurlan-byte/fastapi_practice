# FastAPI Practice

A practice REST API built while learning FastAPI: users, posts, votes and JWT
authentication, backed by PostgreSQL.

**Stack:** Python · FastAPI · SQLAlchemy 2.0 · PostgreSQL · Alembic · Pydantic v2 ·
PyJWT · bcrypt · pytest · Docker · GitHub Actions

Includes Alembic migrations, a pytest suite running against real PostgreSQL, and
a CI pipeline that runs tests, builds an image and deploys over SSH.

## Running locally

```bash
docker compose -f docker-compose-dev.yml up -d     # postgres
python -m venv .venv && source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env                               # fill in before starting
alembic upgrade head
uvicorn app.main:app --reload
pytest                                             # tests
```

Swagger UI at http://127.0.0.1:8000/docs lists every endpoint and lets you call
them. Login is sent as `form-data`, not JSON, with the email in the `username`
field.

## Known limitations

Decisions I would make differently today, left in place rather than retrofitted:

- Synchronous SQLAlchemy throughout; no service layer, so business logic and
  queries sit in the routers.
- `HTTPException` raised directly in routers — no domain exception hierarchy.
- Each endpoint manages its own transaction instead of a single commit at the
  request boundary.
- Duplicates caught by an `if exists()` pre-check, which leaves a race window,
  rather than by handling `IntegrityError`.