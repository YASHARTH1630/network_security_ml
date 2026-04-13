import sys
from networksecurity.logging import logging

class NetworkSecurityException(Exception):
    """Custom exception class for the network security package."""

    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)

        _, _, exc_tb = error_details.exc_info()

        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.lineno = exc_tb.tb_lineno

        self.error_message = self.get_detailed_error_message(error_message)

    def get_detailed_error_message(self, error_message):
        return str(error_message)

    def __str__(self):
        return f"Error occurred in file [{self.file_name}] at line [{self.lineno}] with message [{self.error_message}]"


if __name__ == "__main__":
    try:
        logging.info("This is a test log message.")
        x = 1 / 0   # force error
    except Exception as e:
        raise NetworkSecurityException(e, sys)