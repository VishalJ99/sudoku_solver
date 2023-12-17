class FormatError(Exception):
    """
    Exception for errors in input format.

    This exception is raised when an input does not match the expected format,
    used primarily in the context of the error handling in the parse method of
    FormatHandler classes.

    Parameters
    ----------
    message : str, optional
        A human-readable message indicating the error. Default is "Input format is incorrect".

    Attributes
    ----------
    message : str
        Human-readable message indicating the error.
    """

    def __init__(self, message="Input format is incorrect"):
        self.message = message
        super().__init__(self.message)


class TimeoutException(Exception):
    """
    Exception for signaling a timeout in a solver.

    Used primarily in the context of error handling in the Solver classes to
    indicate that a specified timeout has been reached during execution.

    Parameters
    ----------
    message : str, optional
        A human-readable message indicating the timeout. Default is "Solver reached timeout".

    Attributes
    ----------
    message : str
        Human-readable message indicating the timeout.
    """

    def __init__(self, message="Solver reached timeout"):
        self.message = message
        super().__init__(self.message)
