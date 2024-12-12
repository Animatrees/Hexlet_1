from components import Dispatcher, Worker


def create_workers(amount: int, dispatcher: Dispatcher) -> list[Worker]:
    """
    Function to create a specified number of workers.

    - create_workers(amount: int, dispatcher: Dispatcher) -> list[Worker]:
        Creates a specified number of `Worker` instances, assigns unique IDs to them,
        and associates them with the given `Dispatcher`.

        Parameters:
        -----------
        - amount (int): The number of workers to create. Must be greater than 0.
        - dispatcher (Dispatcher): The dispatcher to which the workers will be associated.

        Returns:
        --------
        - list[Worker]: A list of created `Worker` instances.

        Raises:
        -------
        - ValueError: If `amount` is less than 1.
    """

    if amount < 1:
        raise ValueError('Количество создаваемых серверов должно быть больше 0')
    workers = []
    for i in range(1, amount + 1):
        _id = dispatcher.get_last_worker_id() + i
        workers.append(Worker(_id=_id, dispatcher=dispatcher))

    return workers
