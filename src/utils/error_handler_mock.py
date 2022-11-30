"""Mock module for testing raised error ID's while checking types
and analysing ast"""


class ErrorHandlerMock:
    """Class for storing raised error ID's for testing type checking"""

    def __init__(self):
        self.error_ids = []

    def add_error(self, msg_id: int, lexspan, **_):  # pylint: disable = W0613
        """Add error ID"""
        self.error_ids.append(msg_id)

    def get_error_ids(self):
        """return list of error IDs"""
        return self.error_ids

    def check_id_is_in_errors(self, error_id):
        """check an error ID is in error list and returns boolean"""
        return error_id in self.error_ids
