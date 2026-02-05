"""Abstract provider base for WANDA Voice Core."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class ProviderBase(ABC):
    """Abstract base for LLM providers."""

    name: str = "base"

    @abstractmethod
    async def send(self, prompt: str, context: Optional[str] = None) -> str:
        """Send prompt to provider and return response text."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is reachable."""
        ...

    def send_sync(self, prompt: str, context: Optional[str] = None) -> str:
        """Synchronous send (default: run async in new loop)."""
        import asyncio
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(
                    asyncio.run, self.send(prompt, context)
                ).result()
        return asyncio.run(self.send(prompt, context))
