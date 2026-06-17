# Artemis

Despite the name, **Artemis** has absolutely nothing to do with space exploration. It is a dedicated, collaborative backend sandbox built to experiment with modern web development patterns, asynchronous architectures, containerization, and automated CI/CD workflows.

---

## Features

* **User Authentication:** Complete registration and login system utilizing OAuth2 Form Data handling and signed JWT access tokens.
* **Secured Data Isolation:** Multi-tenant project and job tracking architectures that dynamically isolate resources based on the authenticated user context.
* **Asynchronous Lifespan Architecture:** Implements stateful FastAPI startup/shutdown configurations handling continuous-polling global HTTPX clients.
* **Automated DX Tools:** Local developer workflows accelerated via automated `justfile` recipes.

## Tech Stack

* **Framework:** FastAPI (Python 3.12+)
* **Security & Auth:** Argon2 (password hashing) & PyJWT (bearer token issuance)
* **Database & ORM:** PostgreSQL with async SQLAlchemy 2.0 (using `selectinload` for relationship optimization)
* **Migrations:** Async Alembic execution environment.
* **Containerization:** Multi-stage `Dockerfile` and `compose.yml` optimized with system-level python dependencies.
* **Observability:** Core Prometheus telemetry exporters paired with pre-configured Grafana monitoring dashboards.

## CI/CD & Versioning 

This project uses Conventional Commits to automatically manage versioning and changelogs via Google's `release-please` automation engines.
