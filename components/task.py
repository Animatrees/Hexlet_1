class Task:
    """
    The Task class represents a task with a specified duration in seconds.

    Attributes:
    -----------
    - duration (int): The duration of the task in seconds. Must be a non-negative integer.

    Methods:
    --------
    - __init__(duration: int) -> None:
        Initializes a Task instance with a given duration.
        Raises ValueError if the duration is not a non-negative integer.

    - duration (property):
        - Getter: Returns the duration of the task.
        - Setter: Sets the duration of the task.
        Ensures the value is a non-negative integer.
    """

    def __init__(
            self,
            duration: int,
    ) -> None:
        self.duration = duration

    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, value: int) -> None:
        if type(value) != int or value < 0:
            raise ValueError('Длительность задания не может быть меньше 0 секунд.')

        self._duration = value
