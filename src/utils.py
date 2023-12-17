import time
from sudoku_solvers import SudokuSolver
from sudoku_format_handlers import SudokuFormatHandler
from sudoku_board import SudokuBoard
from typing import Tuple
import argparse
from typing import Dict, Any, Optional
import os
import sys


def solve_sudoku(
    board: SudokuBoard,
    solver: SudokuSolver,
) -> Tuple[Optional[SudokuBoard], float, str]:
    """
    Solve a SudokuBoard object using a specified solver.

    Parameters
    ----------
    sudoku_input : str
        The file path or string containing the sudoku puzzle.
    solver : SudokuSolver
        An instance of the SudokuSolver class, which will be used to solve the sudoku.

    Returns
    -------
    Tuple[Optional[SudokuBoard], float, str]
        A tuple containing the solved sudoku board, the time taken to solve the puzzle in seconds,
        and the status of the solution (e.g., 'solved', 'unsolved', 'error').

    Raises
    ------
    ValueError
        If the solver is not initialised before calling this function.

    Notes
    -----
    This function is simple right now but defined for the sake of extensibility,
    where logic to handle more complex solvers or runtime statistics can be added in the future.

    The solver should be initialised before calling this function, i.e., solver.set_solver() should
    have been called already.

    Examples
    --------
    >>> solver = SudokuSolver()
    >>> format_handler = SudokuFormatHandler()
    >>> sudoku_input = 'test/sudoku_solver_test_boards/easy_1.txt'
    >>> board = format_handler.parse(sudoku_input)
    >>> solved_board, solve_time, status = solve_sudoku(board, solver)
    >>> print(solved_board)
    >>> print(solve_time)
    >>> print(status)
    """
    start_time = time.time()
    solved_board, status = solver.solve(board)
    solve_time = time.time() - start_time
    return solved_board, solve_time, status


def get_solver_kwargs(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Get solver keyword arguments from a set of command-line arguments.

    Parameters
    ----------
    args : argparse.Namespace
        The command-line arguments or configuration file path.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the solver keyword arguments.

    Notes
    -----
    This function currently is very basic right now as solvers implemented only need
    a single argument (timeout) for their initialisation, however future solvers may need
    more complex initialisation arguments. In which case this function can be used to get
    the solver kwargs via defining the parsing logic for a YAML configuration file.

    Examples
    --------
    # Using command-line arguments:
    >>> args = argparse.Namespace(...,timeout=10)
    >>> get_solver_kwargs(args)
    {'timeout': 10}

    # Future logic Using a YAML configuration file:
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

    Raises
    ------
    ValueError
        If `solver` is not a valid key in `solver_dict`.

     Notes
    -----
    This function does not take any arguments to initialise the format handler as that class
    does not need parameters to be initialised in the current design for that class.

    The ValueError is raised inside the set_solver() method of the SudokuSolver class.

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


def load_boards(
    board_path: str,
    format_handler: SudokuFormatHandler,
    format: str = "grid",
    input_type: str = "filepath",
) -> Tuple[Tuple[str, SudokuBoard]]:
    """
    Load a set of Sudoku boards from an input directory or file.

    Parameters
    ----------
    board_paths : str
        The file path or directory path containing the Sudoku boards.
    format_handler : SudokuFormatHandler
        An instance of the SudokuFormatHandler class, used to parse and process the input.
    format : str, optional
        The format in which the Sudoku boards are presented (e.g., 'grid', 'line').
        Default is 'grid'.
    input_type : str, optional
        The type of input (e.g., 'filepath', 'string'). Default is 'filepath'.

    Returns
    -------
    Tuple[str, ...]
        A tuple containing the Sudoku boards.

    Raises
    ------
    FileNotFound
        If the input file or directory does not exist. Only raised if `input_type` is 'filepath'.
    FormatError
        If the input format is incorrect or not as expected.
    ValueError
        If the input type is not supported or other parsing errors occur.

    Raises

    Notes
    -----
    The format handler should be initialised before calling this function, i.e.,
    format_handler = SudokuFormatHandler() should have been called already.

    Examples
    --------
    >>> format_handler = SudokuFormatHandler()
    >>> boards = load_boards('puzzles.txt', format_handler, 'grid')
    >>> print(boards)
    """

    if input_type == "filepath" and not os.path.exists(board_path):
        raise FileNotFoundError(f"File or directory {board_path} does not exist.")

    if os.path.isdir(board_path):
        # Get all non-hidden files in directory.
        board_paths = [
            os.path.join(board_path, f) for f in os.listdir(board_path) if not f.startswith(".")
        ]

    else:
        # Convert single file path to list for consistent handling.
        board_paths = [board_path]

    sudoku_boards = []
    exceptions = []

    for path in board_paths:
        try:
            board = format_handler.parse(path, format, input_type)
            sudoku_boards.append(board)
        except Exception as e:
            exceptions.append((path, e))

    if exceptions:
        if len(exceptions) == len(board_paths):
            print(f"[ERROR] Failed to parse any boards from {board_path}.")
            if len(exceptions) > 5:
                error_file = f"{board_path}.errors"
                with open(error_file, "w") as f:
                    for path, e in exceptions:
                        f.write(f"Error in {path}: {e}\n")
                print(f"[ERROR] Multiple errors occurred. See {error_file} for details.")
            else:
                for path, e in exceptions:
                    print(f"[ERROR] Following raised for {path}:\n{e}")
            sys.exit(1)
        else:
            for path, e in exceptions:
                print(f"[WARNING] Error in {path}:\n{e}")

    # Zip together the boards and their paths
    # i.e each element in the return tuple is (path, SudokuBoard).
    return tuple(zip(board_paths, sudoku_boards))
