
class CoreException(Exception):
    def __init__(self, description: str):
        self.description = description


class NotFoundException(CoreException):
    def __init__(self, description: str):
        super().__init__(description)
