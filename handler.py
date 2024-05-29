import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Coroutine


class Handler(ABC):
    """
    Base class for all handlers
    """

    @abstractmethod
    def run_at(self) -> datetime:
        """
        Get the time at which the handler should run
        :return: datetime object representing the time to run the next request
        """
        pass

    @abstractmethod
    async def run(self) -> None:
        """
        Start retrieving bill updates and push updates to the database
        :return: None
        """
        pass


handlers: dict[Handler, asyncio.Task] = {}
