import httpx

from app.providers.base import JobProvider
from app.providers.models import ProviderJob


class RemoteOKProvider(JobProvider):
    """Fetches jobs from the RemoteOK API."""

    BASE_URL = "https://remoteok.com/api"

    async def fetch_jobs(self) -> list[ProviderJob]:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                self.BASE_URL,
                headers={
                    "User-Agent": "JobPilotAI/0.1",
                },
            )

            response.raise_for_status()

            data = response.json()

        print(f"Fetched {len(data)} records")

        if not isinstance(data, list) or len(data) <= 1:
            return []

        import html
        from app.common.enums import JobSource

        jobs = []
        # The first element is API legal/metadata notices, so skip it.
        for item in data[1:]:
            if not isinstance(item, dict):
                continue

            title = html.unescape(item.get("position") or "")
            company = html.unescape(item.get("company") or "")

            location = item.get("location") or "Remote"
            location = location.strip().strip(",") if location else "Remote"

            job_url = item.get("url") or ""
            if not job_url:
                continue

            description = item.get("description") or ""

            salary_min = item.get("salary_min")
            salary_max = item.get("salary_max")

            try:
                salary_min = float(salary_min) if salary_min is not None else None
            except (ValueError, TypeError):
                salary_min = None

            try:
                salary_max = float(salary_max) if salary_max is not None else None
            except (ValueError, TypeError):
                salary_max = None

            if salary_min == 0:
                salary_min = None
            if salary_max == 0:
                salary_max = None

            has_salary = (salary_min is not None) or (salary_max is not None)
            salary_currency = "USD" if has_salary else None
            salary_period = "YEAR" if has_salary else None

            jobs.append(
                ProviderJob(
                    title=title,
                    company_name=company,
                    location=location,
                    is_remote=True,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    salary_currency=salary_currency,
                    salary_period=salary_period,
                    source=JobSource.REMOTEOK,
                    job_url=job_url,
                    description=description,
                )
            )

        return jobs