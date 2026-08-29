import logging
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import SessionLocal
from app.repositories.jobRepository import JobRepository
from app.models.jobModel import Job
from app.common.enums import JobSource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = TestClient(app)


def main():
    db = SessionLocal()
    try:
        job_repo = JobRepository(db)
        jobs = job_repo.list()
        if not jobs:
            logger.info("No jobs found in DB. Seeding a mock job parent for testing...")
            job = Job(
                title="Staff Engineer",
                company_name="JobPilot Inc",
                location="Bengaluru",
                is_remote=True,
                source=JobSource.MANUAL,
                job_url="https://jobpilot.ai/test-job-999",
                description="Seeded manually for testing.",
            )
            job = job_repo.create(job)
            job_id = job.id
        else:
            job_id = jobs[0].id

        logger.info(f"Targeting Job ID: {job_id}")

        # 1. Test saving a job (interaction status = saved)
        payload = {"job_id": job_id, "status": "saved", "notes": "Need to tailor resume"}
        logger.info("POSTing /api/v1/applications Create request...")
        response = client.post("/api/v1/applications", json=payload)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        data = response.json()
        app_id = data["id"]
        logger.info(f"Successfully tracked application ID: {app_id} with status: {data['status']}")

        # 2. Test listing applications
        logger.info("GETting /api/v1/applications List query...")
        response = client.get("/api/v1/applications?status=saved")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        apps_list = response.json()
        assert len(apps_list) > 0, "Saved list should contain at least 1 record"
        logger.info("List fetch verified.")

        # 3. Test status transition to applied
        update_payload = {"status": "applied", "notes": "Submitted resume on backend portal"}
        logger.info(f"PUTting /api/v1/applications/{app_id} Status update...")
        response = client.put(f"/api/v1/applications/{app_id}", json=update_payload)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        updated_data = response.json()
        assert updated_data["status"] == "applied", "Status should update"
        assert updated_data["applied_at"] is not None, "applied_at timestamp must be populated"
        logger.info(f"Successfully updated application ID: {app_id} (applied_at: {updated_data['applied_at']})")

        # 4. Clean up delete application record
        logger.info(f"DELETEing /api/v1/applications/{app_id} to clean database...")
        response = client.delete(f"/api/v1/applications/{app_id}")
        assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        logger.info("Application deleted successfully. Test suite SUCCESS!")

    finally:
        db.close()


if __name__ == "__main__":
    main()
