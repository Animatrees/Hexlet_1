from components import Task


def create_task(duration: int) -> Task:
    """
    Utility function.

    - create_task(duration: int) -> Task:
        Creates and returns a new `Task` instance with the specified duration.
    """
    return Task(duration=duration)
