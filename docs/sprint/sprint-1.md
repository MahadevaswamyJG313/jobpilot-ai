## Sprint 1

### Completed

- Added SQLAlchemy
- Created Base model
- Added Job model
- Implemented Repository layer
- Added Service layer
- Added Provider interface

### Pending

- Mapper
- Scheduler
- Search API

### Notes

Repository pattern adopted.
Service layer introduced.
Provider abstraction completed.

## Completed

- Added Mapper layer.
- Implemented `JobMapper` to convert `ProviderJob` into `Job`.
- Kept providers independent from SQLAlchemy models.

## Learning

The Mapper pattern separates data transformation from business logic, improving maintainability and reducing duplication.

## Completed

- Implemented `MockProvider`.
- Verified the provider interface with sample job data.
- Established the first provider implementation using the shared `JobProvider` contract.

## Learning

Using a mock provider allows us to validate the application's architecture independently of external APIs.

### Infrastructure

- Added Alembic for database schema migrations.
- Added pytest for automated testing.
- Transitioning from manual verification scripts to automated tests.

### Development Tooling

- Installed Alembic.
- Initialized migration environment.
- Prepared the project for version-controlled database schema changes.