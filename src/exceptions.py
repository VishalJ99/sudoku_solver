class FormatError(Exception):
    """Exception raised for errors in the input format.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Input format is incorrect"):
        self.message = message
        super().__init__(self.message)


class TimeoutException(Exception):
    """Exception used to signal a timeout in the solver.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Solver reached timeout"):
        self.message = message
        super().__init__(self.message)
