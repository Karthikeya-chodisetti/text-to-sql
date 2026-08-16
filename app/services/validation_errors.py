class AppError(Exception):
    """Base exception for application-level errors."""

    status_code = 500

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ValidationError(AppError):
    """Base exception for validation failures."""

    status_code = 400


class LLMError(AppError):
    """Raised when SQL generation by the LLM fails."""

    status_code = 502


class DatabaseError(AppError):
    """Base exception for database-related failures."""

    status_code = 500


class SQLExecutionError(DatabaseError):
    """Raised when generated SQL cannot be executed."""

    status_code = 400


class RequestValidationError(ValidationError):

    def __init__(self, operation: str, message: str):
        self.operation = operation
        super().__init__(message)


class SQLValidationError(ValidationError):

    def __init__(self, operation: str, message: str):
        self.operation = operation
        super().__init__(message)


class QueryGuardrailError(ValidationError):

    def __init__(self, guardrail: str, message: str):
        self.guardrail = guardrail
        super().__init__(message)
