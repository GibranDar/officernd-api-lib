class HttpException(Exception):
    """Base class for HTTP exceptions."""

    def __init__(self, message, status_code=500):
        """Initialize the exception."""
        super().__init__(message)
        self.status_code = status_code


class ValidationException(Exception):
    """Base class for validation exceptions."""

    def __init__(self, message, status_code=400):
        """Initialize the exception."""
        super().__init__(message)
        self.status_code = status_code
