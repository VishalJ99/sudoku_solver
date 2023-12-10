class FormatError(Exception):
    """Exception raised for errors in the input format.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Input format is incorrect"):
        self.message = message
        super().__init__(self.message)
