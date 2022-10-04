import json
import os

class ErrorHandler():
    
    def __init__(self, language = "ENG"):
        errors = []
        self.language = language

        self.parser_error_messages = self._get_parser_dict()
        #print(self.parser_error_messages)

    def _get_parser_dict(self):
        dir_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), '../error_messages')
        parser_errors_filepath = os.path.join(dir_path, 'parser_errors.json')
        parser_errors_file = open(parser_errors_filepath)
        return json.load(parser_errors_file)

    def add_error(self, id: int, **kwargs):
        try:
            msg = self.parser_error_messages[str(id)][self.language]
        except KeyError as ke:
            print("Error id {id} could not be found from parser_errors.json".format(id=id))
            return

        print(msg)
        #msg = msg.format(row=kwargs["row"], column=kwargs["column"], prodval=kwargs["prodval"])
        for key, value in kwargs.items():
            msg = msg.replace(f"@{key}", str(value))
        print(msg)
        #for key, value in kwargs.items():
        #    print("KWARG ITEM", key, value)


default_error_handler = ErrorHandler()