class InvalidAPIUsage(Exception):
    """
    Exception class for handling invalid API usage in a Flask application.

    Attributes:
        status_code (int): HTTP status code to be returned. Default is 400.
        message (str): The error message to be returned.
        payload (dict, optional): Additional data to include in the error response.

    Methods:
        __init__(self, message, status_code=None, payload=None):
            Initializes the InvalidAPIUsage instance with a message, an optional status code, and an optional payload.
        to_dict(self):
            Converts the exception instance to a dictionary suitable for JSON responses.

    Example usage:
        raise InvalidAPIUsage('This is an error message.', status_code=404, payload={'extra_info': 'details'})
    """
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv