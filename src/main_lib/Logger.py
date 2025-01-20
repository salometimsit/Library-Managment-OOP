import logging
import os

import pandas as pd

from src.main_lib.FilesHandle import FilesHandle


class Logger:
    """
    This is a logger class that document all the actions of the librarian to a logger
    """

    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',filename=FilesHandle().get_logger_file(), filemode='a')

    @staticmethod
    def log_method_call(message):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                try:
                    result = func(self, *args, **kwargs)
                    if result is None or result == "" or result== [] or result == False:
                        logging.info(f"{message} fail")
                    else:
                        logging.info(f"{message} successfully")
                    return result
                except Exception as e:
                    logging.error(f"{message} fail")
                    raise
            return wrapper
        return decorator

    @staticmethod
    def log_add_message(message):
        logging.info(message)
