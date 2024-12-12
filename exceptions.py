class ApplicationError(Exception):
    pass


class DispatcherHasNoWorkersError(ApplicationError):
    def __str__(self):
        return f'У менеджера нет серверов для обработки вашей задачи. Создайте хотя бы один сервер.'
