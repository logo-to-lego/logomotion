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

    def _get_messages_from_json_files(self, msg_id):
        # if 1000 <= msg_id <= 1999:
        #     pass
        if 2000 <= msg_id <= 2999:
            return self._get_parser_dict()[str(msg_id)]
        # if 3000 <= msg_id <= 3999:
        #     pass
        raise Exception(
            f"Message id {msg_id} was not found from error message files")

    def add_error(self, msg_id: int, **kwargs):
        """Gets the error message frame in the defined language (ENG/FIN),
        replaces the @-tags with the params given as **kwargs.
        These messages are then added to a list of messages.

        Args:
            msg_id (int): ID of the error defined in the error.json files
        """
        msg_dict = self._get_messages_from_json_files(msg_id)

        fin_msg = msg_dict["FIN"]
        eng_msg = msg_dict["ENG"]

        for key, value in kwargs.items():
            fin_msg = fin_msg.replace(f"@{key}", str(value))
            eng_msg = eng_msg.replace(f"@{key}", str(value))

        # All language options are saved, even though only the errors in the selected language
        # will be written to the console. Reason for this is to make testing simple.
        # We want to have only one test file for error testing, and because in this parser,
        # there is only one instance of the Shared class (defined in parser/globals.py), only
        # one parser object can be defined in the testing setup.
        err_msgs = {"FIN": fin_msg, "ENG": eng_msg}
        self.errors.append(err_msgs)

    def get_error_messages(self):
        """Returns error messages"""
        return self.errors

    def write_errors_to_console(self):
        """Writes error messages to console in the selected language"""
        for msg in self.errors:
            console.write(msg[self.language])


default_error_handler = ErrorHandler()
