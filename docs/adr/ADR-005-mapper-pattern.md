# ADR-005: Introduce Mapper Pattern

## Status

Accepted

## Context

Job providers return external data formats, while the application stores SQLAlchemy models. Directly coupling providers to database models would make providers dependent on persistence details.

## Decision

Introduce a dedicated Mapper layer to convert `ProviderJob` objects into `Job` database models.

## Consequences

### Positive

- Providers remain independent of the database.
- Centralized transformation logic.
- Easier maintenance when models evolve.
- Reusable mapping across multiple providers.

### Negative

- Introduces an additional architectural layer.
- Requires maintaining mapping code.