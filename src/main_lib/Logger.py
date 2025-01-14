import logging
import os


class Logger:
    file_path = os.path.join(os.path.dirname(__file__), 'Excel_Tables/logger.log')
    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    logging.basicConfig(
        level=logging.INFO, format='%(message)s', filename=file_path, filemode='w'
    )

    @staticmethod
    def log_method_call(message):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                try:
                    result = func(self, *args, **kwargs)
                    if result == True:
                        logging.info(f"{message} successfully")
                    else:
                        logging.info(f"{message} fail")
                    return result
                except Exception as e:
                    logging.error(f"{message} fail")
                    raise

            return wrapper

        return decorator

    @staticmethod
    def log_add_message(message):
        logging.info(message)
