import time
from sudoku_solvers import SudokuSolver
from sudoku_format_handlers import SudokuFormatHandler
from sudoku_board import SudokuBoard
from typing import Tuple
import argparse
from typing import Dict, Any


def solve_sudoku(
    sudoku_input: str,
    solver: SudokuSolver,
    format_handler: SudokuFormatHandler,
    format: str = "grid",
    input_type: str = "filepath",
) -> Tuple[SudokuBoard, float, str]:
    """
    Solves a sudoku puzzle from a string or file using a specified solver and format handler.

    This function reads the input sudoku board, processes it according to the specified
    format and input_type, and then attempts to solve it using the provided solver.
    It tracks the time taken to solve the puzzle and returns the solved board along with
    the solving status and time.

    Parameters
    ----------
    sudoku_input : str
        The file path or string containing the sudoku puzzle.
    solver : SudokuSolver
        An instance of the SudokuSolver class, which will be used to solve the sudoku.
    format_handler : SudokuFormatHandler
        An instance of the SudokuFormatHandler class, used to parse and process the input.
    format : str, optional
        The format in which the sudoku puzzle is presented (e.g., 'grid', 'line').
        Default is 'grid'.
    input_type : str, optional
        The type of input provided, dictating how it should be read (filepath or string).
        Default is 'filepath'.

    Returns
    -------
    Tuple[SudokuBoard, float, str]
        A tuple containing the solved sudoku board, the time taken to solve the puzzle in seconds,
        and the status of the solution (e.g., 'solved', 'unsolved', 'error').

    Raises
    ------
    FormatError
        If the input format is incorrect or not as expected.
    TimeoutException
        If the solving process exceeds the specified timeout.

    Notes
    -----
    The solver should be initialised before calling this function, i.e., solver.set_solver() should
    have been called already.

    Examples
    --------
    >>> solver = SudokuSolver()
    >>> solver.set_solver('bt_basic', {'timeout': 60})
    >>> format_handler = SudokuFormatHandler()
    >>> func_args = ('puzzle.txt', solver, format_handler, 'grid', 'filepath')
    >>> solved_board, solve_time, status = solve_sudoku(*func_args)
    >>> print(solve_time, status)
    """
    board = format_handler.parse(sudoku_input, format, input_type)
    start_time = time.time()
    solved_board, status = solver.solve(board)
    solve_time = time.time() - start_time
    return solved_board, solve_time, status


def get_solver_kwargs(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Get solver keyword arguments from a set of command-line arguments.

    This function currently has limited functionality as solvers implemented only
    support a single keyword argument (timeout). In the future, to get the solver kwargs for
    more complex solvers, this function is the place where a YAML configuration file can
    be parsed to get the solver kwargs for more complex solvers.

    Parameters
    ----------
    args : argparse.Namespace
        The command-line arguments or configuration file path.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the solver keyword arguments.

    Examples
    --------
    Using command-line arguments:
    >>> args = argparse.Namespace(...,timeout=10)
    >>> get_solver_kwargs(args)
    {'timeout': 10}

    Using a YAML configuration file:
    >>> args = argparse.Namespace(...,config='config.yaml')
    >>> get_solver_kwargs(args)
    {'timeout': 60, 'strategy': 'backtracking', 'log_level': 'info', 'max_attempts': 5}
    """
    # In the future, args will contain a path to a config file which will be parsed here to get
    # the solver kwargs.
    solver_kwargs = {"timeout": args.timeout}
    return solver_kwargs


def initialise_solver_and_format_handler(
    solver_method: str, solver_kwargs: Dict[str, Any]
) -> Tuple[SudokuFormatHandler, SudokuSolver]:
    """
    Initialise and configure the solver and format handler for Sudoku puzzles.

    Parameters
    ----------
    solver_method : str
        The name of the solving method to be used by the Sudoku solver.
    solver_kwargs : Dict[str, Any]
        A dictionary of keyword arguments to initialise the solver.

    Returns
    -------
    Tuple[SudokuFormatHandler, SudokuSolver]
        A tuple containing the initialised format handler and solver class instances.
        The format handler is used for parsing and formatting Sudoku puzzles,
        and the solver is configured based on the specified method and additional arguments.

    Notes
    -----
    This function does not take any arguments to initialise the format handler as that class
    does not need parameters to be initialised in the current design for that class.

    Examples
    --------
    >>> solver_method = 'bt_easiest_first'
    >>> solver_kwargs = {'timeout': 60}
    >>> format_handler, solver = initialise_solver_and_format_handler(solver_method, solver_kwargs)
    """
    format_handler = SudokuFormatHandler()
    solver = SudokuSolver()

    # Set solver backend.
    solver.set_solver(solver_method, solver_kwargs)
    return format_handler, solver
