import os
import logging
from fastapi.testclient import TestClient
from app.main import app
from app.core.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

# Point to correct environment DB
os.environ["DATABASE_URL"] = "sqlite:///./data/jobpilot.db"

client = TestClient(app)


def test_api():
    # 1. Health check
    logger.info("Testing health check endpoint...")
    resp = client.get("/health")
    logger.info("Health status: %d, data: %s", resp.status_code, resp.json())
    assert resp.status_code == 200

    # 2. Get all jobs
    logger.info("Retrieving jobs from API...")
    resp = client.get("/api/v1/jobs?limit=5")
    logger.info("Jobs list status: %d", resp.status_code)
    assert resp.status_code == 200
    jobs = resp.json()
    logger.info("Total jobs returned: %d", len(jobs))

    if jobs:
        first_job = jobs[0]
        logger.info("First Job: %s at %s", first_job["title"], first_job["company_name"])
        job_id = first_job["id"]
        
        # 3. Get single job
        logger.info("Retrieving job details for ID %d...", job_id)
        detail_resp = client.get(f"/api/v1/jobs/{job_id}")
        logger.info("Job details status: %d", detail_resp.status_code)
        assert detail_resp.status_code == 200
        assert detail_resp.json()["id"] == job_id
        
        # 4. Search jobs
        search_term = first_job["title"].split()[0]
        logger.info("Searching jobs with term '%s'...", search_term)
        search_resp = client.get(f"/api/v1/jobs?q={search_term}")
        logger.info("Search results status: %d, count: %d", search_resp.status_code, len(search_resp.json()))
        assert search_resp.status_code == 200

    # 5. Invalid job lookup
    logger.info("Testing non-existent job ID lookup...")
    invalid_resp = client.get("/api/v1/jobs/999999")
    logger.info("Invalid Job response code: %d", invalid_resp.status_code)
    assert invalid_resp.status_code == 404
    logger.info("All API tests completed successfully!")


if __name__ == "__main__":
    test_api()
