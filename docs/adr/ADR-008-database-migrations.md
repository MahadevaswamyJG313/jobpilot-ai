# ADR-008: Database Migration Strategy

## Status

Accepted

## Context

As the application evolves, database schemas will change. Recreating the database for every change would lead to data loss and make deployments difficult.

## Decision

Use Alembic as the migration tool for managing schema changes.

## Consequences

### Positive

- Version-controlled database schema.
- Safe upgrades in development and production.
- Team members can synchronize schema changes consistently.

### Negative

- Adds migration files that require maintenance.
- Developers must generate and review migrations for schema updates.