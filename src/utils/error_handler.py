"""error_handler.py is responsible for getting error messages from json files
and storing error messages in a list when they occur during compiling
"""

import json
import os
from utils.console_io import default_console_io

FIN = "fin"
ENG = "eng"
DEFAULT_NAME = "errors"
PATH = os.path.join(os.path.dirname(os.path.relpath(__file__)), "../../src/errors/")
ERROR_MESSAGES_PATH = os.path.join(os.path.dirname(os.path.relpath(__file__)), "../../src/language/")


class ErrorHandler:
    """ErrorHandler class takes all error messages when running the compiler.
    The messages are stored in a list
    """

    def __init__(self, console_io=default_console_io, language=FIN, name=DEFAULT_NAME):
        if language.lower() not in (FIN, ENG):
            raise Exception(f"Language {language} is not defined")
        self.errors = []
        self.console_io = console_io
        self.language = language.lower()
        
        self.fin_messages_dict = self._get_fin_messages()
        self.eng_messages_dict = self._get_eng_messages()
        
        self._err_msg_filename = name

    def _get_fin_messages(self):
        with open(os.path.join(ERROR_MESSAGES_PATH, "fin/fin_error_messages.json"), encoding="utf-8") as file:
            return json.load(file)
    
    def _get_eng_messages(self):
        with open(os.path.join(ERROR_MESSAGES_PATH, "eng/eng_error_messages.json"), encoding="utf-8") as file:
            return json.load(file)

    def _get_message_by_id(self, msg_id: str):
        msg_dict = {
            FIN: self.fin_messages_dict[msg_id],
            ENG: self.eng_messages_dict[msg_id],
        }
        return msg_dict

    def add_error(self, msg_id: str, lexspan, **kwargs):
        """Gets the error message frame in the defined language (ENG/FIN),
        replaces the @-tags with the params given as **kwargs.
        These messages are then added to a list of messages.

        Args:
            msg_id (int): ID of the error defined in the error.json files
        """
        msg_dict = self._get_message_by_id(msg_id)

        fin_msg = msg_dict[FIN]
        eng_msg = msg_dict[ENG]

        for key, value in kwargs.items():
            fin_msg = fin_msg.replace(f"@{key}", str(value))
            eng_msg = eng_msg.replace(f"@{key}", str(value))

        err_msgs = {
            FIN: fin_msg,
            ENG: eng_msg,
            "start": lexspan[0],
            "end": lexspan[1]
        }

        # Lexer is ran multiple times in the program
        # and causes the same error messages to occur
        if err_msgs not in self.errors:
            self.errors.append(err_msgs)

    def get_error_messages(self):
        """Returns error messages"""
        return self.errors

    def create_json_file(self):
        fin_dict = {}
        eng_dict = {}
        for index, msg in enumerate(self.errors, start=1):
            fin_dict[index] = {
                "message": msg[FIN],
                "start": msg["start"],
                "end": msg["end"]
            }
            eng_dict[index] = {
                "message": msg[ENG],
                "start": msg["start"],
                "end": msg["end"]
            }

        try:
            fin_path = PATH + FIN + "_" + self._err_msg_filename + ".json"
            eng_path = PATH + ENG + "_" + self._err_msg_filename + ".json"

            with open(fin_path, mode="w+", encoding="utf-8") as file:
                json_object = json.dumps(fin_dict, ensure_ascii=False).encode("utf8")
                file.write(json_object.decode())

            with open(eng_path, mode="w+", encoding="utf-8") as file:
                json_object = json.dumps(eng_dict, ensure_ascii=False).encode("utf8")
                file.write(json_object.decode())

        except Exception as error:
            print(f"An error occurred when writing {self._err_msg_filename}.json file:\n{error}")
            raise

    def write_errors_to_console(self):
        """Writes error messages to console in the selected language"""
        for msg in self.errors:
            self.console_io.write(msg[self.language])


default_error_handler = ErrorHandler()
