# JobPilot AI — Vision Alignment & Execution Roadmap

We have conducted a thorough review of the current `jobpilot-ai` codebase. The architecture is set up in alignment with the proposed vision, separating provider fetching, mapper transformation, service orchestration, repository operations, and database persistence.

---

## 🔍 Codebase Trace vs. Product Vision

Here is how the current implementation maps to the target architecture:

### 1. Job Ingest & Provider Layer (`app/providers/`)
* **Interface**: `JobProvider` (`base.py`) defines the asynchronous contract `fetch_jobs() -> list[ProviderJob]`.
* **Payload Serialization**: `ProviderJob` (`models.py`) encapsulates all normalized job fields, including salary details, location, and remote flags. This decouples upstream raw provider API shapes from downstream database entities.
* **Implementations**:
  * `MockProvider` (`mock_provider.py`) produces mock jobs for early-stage verification.
  * `RemoteOKProvider` (`remoteok_provider.py`) holds an HTTPX client pointing to `https://remoteok.com/api` but currently acts as a stub returning `[]`.

### 2. Data Transformation (`app/mappers/`)
* **`JobMapper`** (`job_mapper.py`): Maps `ProviderJob` to the SQL database model `Job`.

### 3. Business Logic & ORM (`app/services/` & `app/models/`)
* **`JobService`** (`job_service.py`): Contains `sync_jobs()`, which drives the flow:
  $$\text{Provider} \xrightarrow{\text{fetch}} \text{ProviderJob} \xrightarrow{\text{map}} \text{Job} \xrightarrow{\text{repository.create}} \text{DB}$$
  It handles basic deduplication by verifying if the `job_url` already exists in the database.
* **`Job` DB Model** (`job.py`): A complete SQLAlchemy table mapping title, company, location, source, source URL, description, salary (min, max, currency, period), and remote flag.

### 4. Repository Pattern (`app/repositories/`)
* **`JobRepository`** (`job_repository.py`): Provides clean DB access abstractions (`create`, `get_by_url`, `list`, `delete`), decoupling the service layer from direct SQLAlchemy session/query constructs.

---

## ⚡ Gap Analysis (What's Missing for End-to-End Execution)

To turn this into a live, running pipeline with **real jobs** (Phase 2), we must address the following gaps:

1. **RemoteOK Parsing**: The `RemoteOKProvider` fetches content but does not serialize the payload into `ProviderJob` instances. We need to implement JSON parsing, key translation, currency/salary parsing, and remote status calculation for RemoteOK data.
2. **Robust Deduplication**: While the service layer checks if `job_url` exists, we need to ensure this is resilient (e.g. trailing slashes, URL normalization).
3. **Execution Script**: We need a script or CLI command that instantiates the actual DB session, injects the real provider, and executes `sync_jobs()` to store real records in the database.

---

## 🚀 Phase 2 & 3 Roadmap: The Implementation Plan

To keep moving forward cleanly without redesigning architecture, we propose executing the following tasks next:

### Task Helper 1: Upgrade `RemoteOKProvider` to parse real data
Match RemoteOK JSON keys to our `ProviderJob` attributes:
* `position` $\to$ `title`
* `company` $\to$ `company_name`
* `location` $\to$ `location`
* `salary_min` / `salary_max` $\to$ parse from tags or strings in the payload.
* `url` $\to$ `job_url`
* `description` $\to$ `description`

### Task Helper 2: Build a Sync CLI Script
Create a command-line script (e.g., `scripts/run_sync.py`) that:
1. Starts a database session.
2. Instantiates `RemoteOKProvider`.
3. Passes it to `JobService`.
4. Runs `await job_service.sync_jobs()` and prints the sync summary (count of new vs, skipped jobs).

### Task Helper 3: Add Unit/Integration Tests
* Test `JobMapper` on live sample payloads from RemoteOK.
* Test `RemoteOKProvider.fetch_jobs` using `pytest` and `pytest-httpx` or mocking to ensure resilience and HTTP failures are handled.
