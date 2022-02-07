from http import HTTPStatus


class BaseError(Exception):
    """Base class for all errors"""

    pass


class QueryParamMissingError(BaseError):
    """Exception raised when the query string is missing a required parameter"""

    http_code = HTTPStatus.BAD_REQUEST
