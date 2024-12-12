from collections import deque

from components.interfaces import IDispatcher
from components.task import Task
from components.worker import Worker
from exceptions import DispatcherHasNoWorkersError


class Dispatcher(IDispatcher):
    """
    The Dispatcher class is responsible for managing workers and tasks.
    It distributes tasks among workers and maintains a queue for pending tasks.

    Methods:
    --------
    - __init__() -> None:
        Initializes the dispatcher with an empty list of workers and a task queue.

    - get_last_worker_id() -> int:
        Returns the total number of workers managed by the dispatcher.

    - add_workers(workers: list[Worker]) -> None:
        Asynchronously adds workers to the dispatcher.
        Tasks from the queue are assigned to newly added workers if available.

    - find_worker() -> Worker | None:
        Finds an available worker.
        Raises DispatcherHasNoWorkersError if no workers exist.

    - add_task(task: Task) -> str:
        Asynchronously assigns a task to an available worker.
        If no worker is available, the task is added to the queue.
        Returns a message indicating the status.

    - dispatch_task(worker: Worker) -> None:
        Asynchronously assigns the first task from the queue to the specified worker.
        If no tasks are in the queue, the method does nothing.

    - get_status() -> str:
        Returns the current status of workers and the task queue.
    """

    def __init__(self) -> None:
        self.workers = []
        self.line = deque()

    def get_last_worker_id(self) -> int:
        return len(self.workers)

    async def add_workers(self, workers: list[Worker]) -> None:
        for worker in workers:
            if self.line:
                await self.dispatch_task(worker=worker)
            else:
                break

        self.workers.extend(workers)

    def find_worker(self) -> Worker | None:
        if not self.workers:
            raise DispatcherHasNoWorkersError
        for worker in self.workers:
            if worker.is_available():
                return worker

    async def add_task(self, task: Task) -> str:
        try:
            worker = self.find_worker()
        except DispatcherHasNoWorkersError as e:
            return str(e)

        if worker:
            await worker.assign_task(task)
            return f'Сервер {worker.id} начал выполнение задачи.'
        else:
            self.line.append(task)
            return f'Нет свободных серверов. Задача добавлена в очередь.'

    async def dispatch_task(self, worker: Worker) -> None:
        if self.line:
            task = self.line.popleft()
            print(f'Задание из очереди направлено на сервер {worker.id}.')
            await worker.assign_task(task)

    def get_status(self) -> str:
        servers_status = '\n'.join(map(str, self.workers)) if self.workers else 'Нет доступных серверов.'
        tasks_amount = len(self.line)
        status_line = f"""Состояние серверов:
{servers_status}
Очередь заданий: {tasks_amount}"""
        return status_line
