class ApiError:

    _message = None
    _error_code = None

    def __init__(self, message, error_code = None):
        self._message = message
        self._error_code = error_code

    def get_message(self):
        return self._message

    def get_error_code(self):
        return self._error_code
