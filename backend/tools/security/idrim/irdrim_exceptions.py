# backend/tools/security/idrim/idrim_exceptions.py


class IDRIMBaseException(Exception):
    def __init__(self, message: str, *, code: str = "idrim_error"):
        super().__init__(message)
        self.message = message
        self.code = code

    def to_dict(self) -> dict:
        return {
            "error": self.code,
            "message": self.message,
        }


class IDRIMValidationError(IDRIMBaseException):
    def __init__(self, message: str):
        super().__init__(message, code="idrim_validation_error")


class IDRIMEngineStateError(IDRIMBaseException):
    def __init__(self, message: str):
        super().__init__(message, code="idrim_engine_state_error")


class IDRIMTaskExecutionError(IDRIMBaseException):
    def __init__(self, message: str):
        super().__init__(message, code="idrim_task_execution_error")


class IDRIMServiceError(IDRIMBaseException):
    def __init__(self, message: str):
        super().__init__(message, code="idrim_service_error")
