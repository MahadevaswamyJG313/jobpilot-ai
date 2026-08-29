import asyncio

from app.providers.remoteok_provider import RemoteOKProvider


async def main():
    provider = RemoteOKProvider()

    jobs = await provider.fetch_jobs()
    print(f"Parsed {len(jobs)} jobs successfully")

    if jobs:
        print("Sample Job 1:")
        print(f"  Title: {jobs[0].title}")
        print(f"  Company: {jobs[0].company_name}")
        print(f"  Location: {jobs[0].location}")
        print(f"  URL: {jobs[0].job_url}")
        print(f"  Salary Min: {jobs[0].salary_min}")
        print(f"  Salary Max: {jobs[0].salary_max}")
        print(f"  Currency: {jobs[0].salary_currency}")
        print(f"  Is Remote: {jobs[0].is_remote}")


if __name__ == "__main__":
    asyncio.run(main())