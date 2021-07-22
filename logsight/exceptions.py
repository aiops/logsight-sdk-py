

class LogsightException(Exception):
    """Base Logsight Exception"""

    message = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        # super().__init__(message)
        if message:
            self.message = message
        try:
            self._error_string = self.message % kwargs
        except Exception:
            self._error_string = self.message

    def __str__(self):
        return self._error_string


class BadRequest(LogsightException):
    status_code = 400


class Unauthorized(LogsightException):
    status_code = 401
    message = "Unauthorized: wrong credentials."


class Forbidden(LogsightException):
    status_code = 403
    message = "Forbidden: your credentials don't give you access to this resource."


class NotFound(LogsightException):
    status_code = 404


class Conflict(LogsightException):
    status_code = 409


class InternalServerError(LogsightException):
    status_code = 500


class ServiceUnavailable(LogsightException):
    status_code = 503


HTTP_EXCEPTION_MAP = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    409: Conflict,
    500: InternalServerError,
    503: ServiceUnavailable,
}


class DataCorruption(LogsightException):
    pass
