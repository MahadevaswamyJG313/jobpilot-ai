from abc import ABC, abstractmethod

from app.providers.models import ProviderJob


class JobProvider(ABC):
    """Base interface for all job providers."""

    @abstractmethod
    async def fetch_jobs(self) -> list[ProviderJob]:
        """Fetch jobs from the provider."""
        raise NotImplementedError