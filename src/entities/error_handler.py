"""error_handler.py is responsible for getting error messages from json files
and storing error messages in a list when they occur during compiling
"""

import json
import os
from utils.console_io import default_console_io as console


class ErrorHandler:
    """ErrorHandler class takes all error messages when running the compiler.
    The messages are stored in a list
    """

    def __init__(self, language="FIN"):
        self.errors = []
        self.language = language
        self.error_dir = os.path.join(
            os.path.dirname(os.path.relpath(__file__)), "../error_messages"
        )

    def _get_parser_dict(self):
        with open(os.path.join(self.error_dir, "parser_errors.json"), encoding="utf-8") as file:
            return json.load(file)

    def _get_message(self, msg_id):
        # if 1000 <= msg_id <= 1999:
        #     pass
        if 2000 <= msg_id <= 2999:
            return self._get_parser_dict()[str(msg_id)][self.language]
        # if 3000 <= msg_id <= 3999:
        #     pass
        raise Exception(f"Message id {msg_id} was not found from error message files")

    def add_error(self, msg_id: int, **kwargs):
        """Gets the error message frame, replaces the @-tags with the params given as **kwargs.
        Error message is then added to a list of messages.

        Args:
            id (int): ID of the error defined in the error.json files
        """
        msg: str = self._get_message(msg_id)

        for key, value in kwargs.items():
            msg = msg.replace(f"@{key}", str(value))
        self.errors.append(msg)

    def get_error_messages(self):
        """Returns error messages"""
        return self.errors

    def write_errors_to_console(self):
        """Writes error messages to console"""
        for msg in self.errors:
            console.write(msg)


default_error_handler = ErrorHandler()
