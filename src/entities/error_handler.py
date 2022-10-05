import json
import os
import sys

class ErrorHandler():
    
    def __init__(self, language = "FIN"):
        self.errors = []
        self.language = language
        self.error_dir = os.path.join(os.path.dirname(os.path.relpath(__file__)), '../error_messages')

    def _get_parser_dict(self):
        parser_errors_file = open(os.path.join(self.error_dir, 'parser_errors.json'))
        return json.load(parser_errors_file)

    def _get_message(self, id):
        if 1000 <= id <= 1999:
            pass
        elif 2000 <= id <= 2999:
            return self._get_parser_dict()[str(id)][self.language]
        elif 3000 <= id <= 3999:
            pass
        else:
            raise Exception("ID {id} was not found from error message files".format(id=id))

    def add_error(self, id: int, **kwargs):
        msg: str = self._get_message(id)
      
        for key, value in kwargs.items():
            msg = msg.replace(f"@{key}", str(value))
        print(msg + "\n")


default_error_handler = ErrorHandler()