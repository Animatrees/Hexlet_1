import asyncio

from components.interfaces import IDispatcher
from components.task import Task


class Worker:
    """
    The Worker class represents a server or worker that can process tasks assigned by a dispatcher.

    Attributes:
    -----------
    - id (int): The unique identifier of the worker.
    - dispatcher (IDispatcher): The dispatcher managing the worker.
    - current_task (Task | None): The task currently being processed by the worker.
    - remaining_time (int): The remaining time (in seconds) to complete the current task.

    Methods:
    --------
    - __init__(_id: int, dispatcher: IDispatcher) -> None:
        Initializes a Worker instance with a unique ID and an associated dispatcher.

    - assign_task(task: Task) -> None:
        Asynchronously assigns a task to the worker and starts processing it.

    - work() -> None:
        Asynchronously processes the current task by decrementing the remaining time every second.
        When the task is completed, the worker notifies the dispatcher to assign the next task.

    - is_available() -> bool:
        Returns `True` if the worker is available (i.e., not processing any task), otherwise `False`.

    - __str__() -> str:
        Returns a string representation of the worker, indicating its status (available or working on a task).
    """

    def __init__(
            self,
            _id: int,
            dispatcher: IDispatcher
    ) -> None:
        self.id = _id
        self.dispatcher = dispatcher
        self.current_task = None
        self.remaining_time = 0

    async def assign_task(self, task: Task) -> None:
        self.current_task = task
        self.remaining_time = task.duration
        asyncio.create_task(self.work())

    async def work(self):
        while self.remaining_time > 0:
            await asyncio.sleep(1)
            self.remaining_time -= 1
        print(f'\nСервер {self.id} успешно выполнил задачу длительностью {self.current_task.duration} сек.')
        self.current_task = None
        await self.dispatcher.dispatch_task(self)

    def is_available(self) -> bool:
        if self.current_task is None:
            return True
        return False

    def __str__(self):
        if self.current_task is None:
            return f'Сервер {self.id}: пусто'
        else:
            return f'Сервер {self.id}: выполняет задание (осталось {self.remaining_time} сек.)'
