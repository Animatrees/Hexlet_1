import asyncio

from commands import create_dispatcher, get_help, create_workers, create_task


async def initialize() -> None:
    """
    Controller for the distributed system simulator.

    This script serves as the entry point for the distributed system simulator.
    It allows users to interact with the system through a set of commands.

    Functions:
    -----------
    - initialize() -> None:
        Asynchronously initializes the simulator, handles user input, and executes commands.

        Workflow:
        ---------
        1. Creates a dispatcher using `create_dispatcher()`.
        2. Displays a help message with `get_help()`.
        3. Enters a command loop where users can:
            - Add servers using the `add_servers <amount>` command.
            - Add tasks using the `add_task <duration>` command.
            - Check system status with the `status` command.
            - View help with the `help` command.
            - Exit the simulator with the `exit` command.

        Commands:
        ---------
        - `add_servers <amount>`: Creates and adds the specified number of servers to the dispatcher.
            Example: `add_servers 5`
        - `add_task <duration>`: Creates a task with the given duration (in seconds) and assigns it to a worker if available.
            Example: `add_task 10`
        - `status`: Displays the current status of workers and the task queue.
        - `help`: Displays the list of available commands.
        - `exit`: Exits the simulator.

        Exceptions:
        -----------
        - Handles invalid input for commands (e.g., non-integer values for `amount` or `duration`).
        - Displays appropriate error messages if exceptions occur during command execution.

        Notes:
        ------
        - Input is handled asynchronously using `asyncio.to_thread` to avoid blocking the event loop.
        - The simulator will continue running until the `exit` command is entered.
    """

    dispatcher = create_dispatcher()
    help = get_help()

    command = await asyncio.to_thread(input, f"""Добро пожаловать в симулятор распределенной системы!
    
{help}

Ваша команда: """)

    while command != 'exit':
        match command.split():
            case ['add_servers', amount]:
                try:
                    amount = int(amount)
                    workers = create_workers(amount=amount, dispatcher=dispatcher)
                except ValueError as e:
                    print(f'Во время создания серверов произошла ошибка: {e}.')
                else:
                    print(f'Создание серверов прошло успешно.')
                    await dispatcher.add_workers(workers)

            case ['add_task', duration]:
                try:
                    duration = int(duration)
                    task = create_task(duration=duration)
                except ValueError as e:
                    print(f'Во время создания задачи произошла ошибка: {e}')
                else:
                    result = await dispatcher.add_task(task=task)
                    print(result)

            case ['status']:
                status = dispatcher.get_status()
                print(status)

            case ['help']:
                print(help)

            case ['exit']:
                continue

            case _:
                print('Неизвестная команда. Введите "help" для получения списка доступных команд.')
        command = await asyncio.to_thread(input, 'Ваша команда: ')

    print('Спасибо, что были с нами!)')
