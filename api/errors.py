from http import HTTPStatus


class BaseError(Exception):
    """Base class for all errors"""

    pass


class BadRequestError(BaseError):
    """Base class for 400 Bad request errors"""

    http_code = HTTPStatus.BAD_REQUEST


class QueryParamMissingError(BadRequestError):
    """Exception raised when the query string is missing a required parameter"""


class InvalidSortByParameterError(BadRequestError):
    """Exception raised when the 'sortBy' query parameter is invalid - must be one of: (id,reads, likes, popularity)"""


class InvalidDirectionParameterError(BadRequestError):
    """Exception raised when the 'direction' query parameter is invalid - must be one of: (asc, desc)"""
