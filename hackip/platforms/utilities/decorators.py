import logging

from ...helpers import get_status_symbol
from rich import print as rprint

logger = logging.getLogger(__name__)


def fetch_info_wrapper(fetch_info_name):
    def actual_decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                if isinstance(result, (dict, list)):
                    rprint(
                        f"{get_status_symbol('pass')} Successfully Fetched {fetch_info_name}"
                    )
                else:
                    rprint(
                        f"{get_status_symbol('fail')} Error in fetching {fetch_info_name}"
                    )
                return result
            except Exception as error:
                rprint(
                    f"{get_status_symbol('fail')} Error in fetching {fetch_info_name}"
                )

        return wrapper

    return actual_decorator
