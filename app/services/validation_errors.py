class RequestValidationError(ValueError):
    def __init__(self, operation: str, message: str):
        self.operation = operation
        self.message = message

        super().__init__(message)


class SQLValidationError(ValueError):
    def __init__(self, operation: str, message: str):
        self.operation = operation
        self.message = message

        super().__init__(message)


class SQLExecutionError(Exception):
    def __init__(self, message: str):
        self.message = message

        super().__init__(message)

class QueryGuardrailError(ValueError):
    def __init__(self, guardrail: str, message: str):
        self.guardrail = guardrail
        self.message = message

        super().__init__(message)