import json
import os

class ErrorHandler():
    
    def __init__(self, language = "ENG"):
        errors = []
        self.language = language

        self.lexer_error_messages = self._get_lexer_dict()
        print(self.lexer_error_messages)

    def _get_lexer_dict(self):
        dir_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), '../error_messages')
        lexer_errors_filepath = os.path.join(dir_path, 'lexer_errors.json')
        lexer_errors_file = open(lexer_errors_filepath)
        return json.load(lexer_errors_file)

    def add_error(self, id: int, row=None, column=None, **kwargs):
        try:
            obj = self.lexer_error_messages[str(id)][self.language]
        except KeyError as ke:
            print("Error id {id} could not be found from lexer_errors.json".format(id=id))
            return

        print("OBJ", obj)


default_error_handler = ErrorHandler()