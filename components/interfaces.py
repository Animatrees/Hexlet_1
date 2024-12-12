from abc import ABC, abstractmethod


class IDispatcher(ABC):
    """
    The `IDispatcher` interface defines the contract for a dispatcher that manages workers and tasks.

    Methods:
    --------
    - dispatch_task(worker) -> None:
        Asynchronously assigns a task from the queue to the specified worker.
        This method must be implemented by any class inheriting from `IDispatcher`.
    """

    @abstractmethod
    async def dispatch_task(self, worker) -> None:
        pass
