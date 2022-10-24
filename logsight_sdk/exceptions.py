from typing import Any, Dict
from http import HTTPStatus as status


class APIException(Exception):

    def __init__(self,
                 type_: str = None, title: str = None,
                 status: int = None, detail: str = None,
                 message: str = None, instance: str = None,
                 **kwargs: Dict) -> None:
        """Problem exception as defined in RFC 7807
        (https://tools.ietf.org/html/rfc7807).

        Args:
            status: HTTP status code generated by the remote server.
            title: Short, human-readable title for the general error type;
                the title should not change for given types.
            detail: Human-readable description of the specific error.
            type: URL to a document describing the error condition (optional,
                and "about:blank" is assumed if none is provided; should
                resolve to a human-readable document).
            instance: This optional key may be present, with a unique URI for
                the specific error; this will often point to an error log for
                that specific response.
            **kwargs: additional context information
        """
        self.type = type_
        self.status = status
        self.title = title
        self.detail = detail
        self.message = message
        self.instance = instance
        self.kwargs = kwargs

    def __str__(self):
        return f'Status: {self.status}, message: {self.message}'


class BadRequest(APIException):
    status_code = status.BAD_REQUEST
    message = """BadRequest: the server cannot or will not
    process the request  due to something that is perceived
    to be a client error."""


class Unauthorized(APIException):
    status_code = status.UNAUTHORIZED
    message = """Unauthorized: the request has not been applied
    because it lacks valid authentication credentials for the
    target resource."""


class Forbidden(APIException):
    status_code = status.FORBIDDEN
    message = """Forbidden: the server understands the request
    but refuses to authorize it."""


class NotFound(APIException):
    status_code = status.NOT_FOUND
    message = """NotFound: the server can't find the requested
    resource."""


class Conflict(APIException):
    status_code = status.CONFLICT
    message = """Conflict: a request conflict with current state
    of the target resource."""


class InternalServerError(APIException):
    status_code = status.INTERNAL_SERVER_ERROR
    message = """InternalServerError: the server has encountered
    a situation it does not know how to hand."""


class ServiceUnavailable(APIException):
    status_code = status.SERVICE_UNAVAILABLE
    message = """ServiceUnavailable: the server is not ready to
    handle the request."""


class BadGateway(APIException):
    status_code = status.BAD_GATEWAY
    message = """the server, while acting as a gateway or proxy,
    received an invalid response from the upstream server."""


class DataCorruption(APIException):
    message = """DataCorruption: the client was unable to parse a
    data structured received from the server."""


HTTP_EXCEPTION_MAP = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    409: Conflict,
    500: InternalServerError,
    502: BadGateway,
    503: ServiceUnavailable,
}


def from_dict(data: Dict[str, Any]) -> APIException:
    """Create a new APIException instance from a dictionary.

    This uses the dictionary as keyword arguments for the APIException
    constructor. If the given dictionary does not contain any fields
    matching those defined in the RFC7807 spec, it will use defaults
    where appropriate (e.g. status code 500) and use the dictionary
    members as supplemental context in the response.

    Args:
        data: The dictionary to convert into an APIException exception.

    Returns:
        A new APIException instance populated from the dictionary fields.
    """
    return HTTP_EXCEPTION_MAP[data['status']](**data)


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