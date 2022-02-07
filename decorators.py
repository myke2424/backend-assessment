import functools
import logging
from typing import Callable

import errors

logger = logging.getLogger(__name__)


def http_error_handler(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except errors.QueryParamMissingError as error:
            logging.exception(error)
            return {"error": str(error)}, error.http_code
        return response

    return wrapper
