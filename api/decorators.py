import functools
import logging
from typing import Callable

from .errors import QueryParamMissingError

logger = logging.getLogger(__name__)


def http_error_handler(func: Callable) -> Callable:
    """Decorator used to catch HTTP errors"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except QueryParamMissingError as error:
            logging.exception(error)
            return {"error": str(error)}, error.http_code
        return response

    return wrapper
