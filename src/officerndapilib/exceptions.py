class HttpException(Exception):
    """Base class for HTTP exceptions."""

    def __init__(self, message, status_code):
        """Initialize the exception."""
        super().__init__(message)
        self.status_code = status_code
