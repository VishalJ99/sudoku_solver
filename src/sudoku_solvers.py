import time
from exceptions import TimeoutException
from abc import ABC, abstractmethod
from sudoku_board import SudokuBoard
from typing import Optional, List, Set, Tuple
import copy
import numpy as np


class Solver(ABC):
    @abstractmethod
    def solve(self, board: SudokuBoard) -> Optional[SudokuBoard]:
        pass


class BacktrackingSolver(Solver):
    """
    Class for solving Sudoku puzzles using a backtracking algorithm.

    This class implements a standard backtracking algorithm for solving Sudoku puzzles.
    It explores possible solutions with depth first search strategy (DFS). Undoing moves
    that lead to a dead end, until it finds a valid solution or exhausts all possibilities.

    Parameters
    ----------
    timeout : int, optional
        The maximum time allowed for solving the puzzle, in seconds. If not set,
        the solver will not have a defined timeout of 1 minute.

    Attributes
    ----------
    timeout : int or None
        The maximum duration in seconds allowed for the solver to run.

    Methods
    -------
    solve(board)
        Solve the Sudoku puzzle using the backtracking algorithm.

    Examples
    --------
    >>> sudoku_board = SudokuBoard(...)
    >>> solver = BacktrackingSolver(timeout=120)
    >>> solved_board, status = solver.solve(sudoku_board)
    >>> print(solved_board)
    SudokuBoard(...)  # Example output of the solved board
    >>> print(status)
    "Solved"  # Example status message
    """

    def __init__(self, timeout=60):
        self.timeout = timeout

    def _backtrack(self):
        """
        Solve the sudoku puzzle using a backtracking algorithm

        Returns
        -------
        bool
            True if the puzzle was solved, False otherwise
        """
        # Check for timeout.
        if self.timeout and (time.time() - self.start_time > self.timeout):
            raise TimeoutException  # Raise an exception when timeout occurs

        # Get empty square coordinates.
        I, J = self.board.get_empty_cells()

        # If there are no empty squares, the puzzle is solved.
        if I is None:
            return True

        # Select the first empty square.
        i, j = I[0], J[0]

        # Check which numbers are valid in the empty square.
        for num in range(1, 10):
            if self.board.check_valid(i, j, num):
                # Make the move and repeat recursively.
                self.board.place_number(i, j, num)
                if self._backtrack():
                    # Puzzle was solved.
                    return True

                # Puzzle was not solved, undo the move and try new number.
                self.board.remove_number(i, j, num)

        # Incorrect move was made previously, backtrack.
        return False

    def solve(self, board):
        """
        Solve the sudoku puzzle using a backtracking algorithm

        Parameters
        ----------
        board : SudokuBoard
            The sudoku board to be solved
        timeout : int, optional
            The maximum time allowed for solving the puzzle, in seconds

        Returns
        -------
        bool
            True if the puzzle was solved, False otherwise
        """

        self.board = board
        original_board = copy.deepcopy(board)

        if self.timeout:
            self.start_time = time.time()

        try:
            self._backtrack()
            if np.array_equal(original_board._board, self.board._board):
                # Input board has no solution.
                return None, "Board has no solution"
            else:
                return self.board, "Solved"
        except TimeoutException:
            return None, "Timeout occurred"


class BacktrackingSolverEasiestFirst(BacktrackingSolver):
    """
    Class for solving Sudoku puzzles using a backtracking algorithm, with a heuristic that
    chooses the cell with the fewest possible options at each step and only loops over those
    options.

    For easy puzzles, this method is slightly slower than the basic backtracking algorithm due
    to the increased overhead of finding the easiest cell at each step. However, for harder
    puzzles, this method is significantly faster than the basic backtracking algorithm.

    Methods
    -------
    _find_easiest_cell(board, row_idxs, col_idxs)
        Identify the cell on a Sudoku board with the fewest possible options, and which
        options are valid for that cell.
    _backtrack()
        Recursively solve the Sudoku puzzle, choosing the next cell based on the fewest options.

    Examples
    --------
    >>> sudoku_board = SudokuBoard(...)
    >>> solver = BacktrackingSolverEasiestFirst(timeout=60)
    >>> solved_board, status = solver.solve(sudoku_board)
    >>> print(solved_board)
    SudokuBoard(...)  # Example output of the solved board
    >>> print(status)
    "Solved"  # Example status message
    """

    def _find_easiest_cell(
        self, board: SudokuBoard, row_idxs: List[int], col_idxs: List[int]
    ) -> tuple[int, int, Set[int]]:
        """
        Identify the cell on a Sudoku board with the fewest possible options from the given list of
        cell indices.

        Parameters
        ----------
        board : SudokuBoard
            The Sudoku board instance to analyse.
        row_idxs : List[int]
            A list of row indices for cells to consider in the search.
        col_idxs : List[int]
            A list of column indices for cells to consider in the search.

        Returns
        -------
        tuple of (int, int, int) or None
            A tuple containing the row index, column index, and the number of possible values
            for the identified cell.

        Notes
        -----
        The method assumes that the lists `row_idxs` and `col_idxs` are found by calling
        `board.get_empty_cells()`. It relies on `board.find_possible_cell_values`
        to determine the potential values for each cell.

        Examples
        --------
        >>> sudoku_board = SudokuBoard(...)
        >>> solver = BacktrackingSolverWithRules(timeout=60)
        >>> easiest_cell_tuple = solver.find_easiest_cell(sudoku_board, [0, 1, 2], [0, 1, 2])
        >>> print(easiest_cell_tuple)
        (1, 2, {4})  # Example output
        """

        cell_options = []
        cell_options_num = []

        for i, j in zip(row_idxs, col_idxs):
            options = board.find_possible_cell_values(i, j)
            cell_options.append(options)
            cell_options_num.append(len(options))

        min_options_idx = cell_options_num.index(min(cell_options_num))

        min_options = cell_options[min_options_idx]
        min_i, min_j = row_idxs[min_options_idx], col_idxs[min_options_idx]

        return min_i, min_j, min_options

    def _backtrack(self):
        # Check for timeout.
        if self.timeout and (time.time() - self.start_time > self.timeout):
            raise TimeoutException  # Raise an exception when timeout occurs

        # Get empty square coordinates.
        I, J = self.board.get_empty_cells()

        # If there are no empty squares, the puzzle is solved.
        if I is None:
            return True

        # Select the empty square with the fewest possible values.
        i, j, cell_options = self._find_easiest_cell(self.board, I, J)

        # Check which numbers are valid in the empty square.
        for num in cell_options:
            # Make the move and repeat recursively.
            self.board.place_number(i, j, num)
            if self._backtrack():
                # Puzzle was solved.
                return True

            # Puzzle was not solved, undo the move and try new number.
            self.board.remove_number(i, j, num)

        # Incorrect move was made previously, backtrack
        return False


class SudokuSolver(Solver):
    """
    A class that facilitates solving Sudoku puzzles using various solving strategies.

    This class acts as a wrapper class to interface with implemented Sudoku solving algorithms.
    It allows the user to select a specific solving strategy and use it to solve a Sudoku board.

    Attributes
    ----------
    solver_dict : dict
        A dictionary mapping solver names to their corresponding classes.

    Methods
    -------
    set_solver(solver: str, solver_kwargs=None):
        Sets the solving strategy to be used.

    solve(board: SudokuBoard) -> Union[SudokuBoard, None]:
        Solves the Sudoku puzzle using the selected strategy.

    Examples
    --------
    >>> sudoku_board = SudokuBoard(...)
    >>> sudoku_solver = SudokuSolver()
    >>> sudoku_solver.set_solver('bt_easiest_first', {'timeout': 60})
    >>> solved_board, status = sudoku_solver.solve(sudoku_board)
    >>> print(solved_board)
    SudokuBoard(...)  # Example output
    >>> print(status)
    "Solved"  # Example status message

    Raises
    ------
    ValueError
        If an invalid solver name is specified.
    """

    def __init__(self):
        """
        Initialises the SudokuSolver with available solving strategies.
        """
        # If a new solver is added, add it to this dictionary.
        # Will automatically be available as an option via the --solver flag in main.py.
        self.solver_dict = {
            "bt_basic": BacktrackingSolver,
            "bt_easiest_first": BacktrackingSolverEasiestFirst,
        }

    def set_solver(self, solver: str, solver_kwargs=None):
        """
        Sets the solving strategy to be used.

        Parameters
        ----------
        solver : str
            The name of the solver to use. Should be a key in `solver_dict`.
        solver_kwargs : dict, optional
            A dictionary of keyword arguments to be passed to the solver's constructor.

        Raises
        ------
        ValueError
            If `solver` is not a valid key in `solver_dict`.

        Examples
        --------
        >>> sudoku_solver = SudokuSolver()
        >>> sudoku_solver.set_solver('bt_easiest_first', {'timeout': 60})
        """
        try:
            self.solver = self.solver_dict[solver](**solver_kwargs if solver_kwargs else {})
        except KeyError:
            raise ValueError(
                f"Solver {solver} is not valid option, please choose from \
                              {list(self.solver_dict.keys())}"
            )

    def solve(self, board: SudokuBoard) -> Tuple[Optional[SudokuBoard], str]:
        """
        Solves the Sudoku board using the selected strategy.

        Parameters
        ----------
        board : SudokuBoard
            The Sudoku board to solve.

        Returns
        -------
        tuple of (SudokuBoard or None, str)
            A tuple where the first element is the solved Sudoku board if a solution is found,
            otherwise None. The second element is a status message as a string, indicating the
            outcome of the solving process.

        Raises
        ------
        ValueError
            If a solver has not been set prior to calling this method.

        Examples
        --------
        >>> sudoku_board = SudokuBoard(...)
        >>> sudoku_solver = SudokuSolver()
        >>> sudoku_solver.set_solver('bt_basic')
        >>> solved_board, status = sudoku_solver.solve(sudoku_board)
        >>> print(solved_board)
        SudokuBoard(...)  # Example output
        >>> print(status)
        "Solved"  # Example status message
        """
        if self.solver is None:
            raise ValueError("Solver has not been set, please call set_solver()")
        board, status = self.solver.solve(board)
        return board, status
