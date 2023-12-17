import time
from exceptions import TimeoutException
from abc import ABC, abstractmethod
from sudoku_board import SudokuBoard
from typing import Optional, List, Set, Tuple, Dict
import copy
import numpy as np


class Solver(ABC):
    """
    Abstract base class for Sudoku solvers.

    This class serves as a template for different Sudoku solving algorithms. It defines the basic
    structure for a Sudoku solver, by specifying the required method 'solve'.

    Subclasses are expected to implement the 'solve' method, providing the logic to solve a Sudoku
    puzzle given as a SudokuBoard object. The exact solving strategy and algorithm can vary
    depending on the specific implementation in the subclass.

    Methods
    -------
    solve(board: SudokuBoard) -> Optional[SudokuBoard]
        Abstract method to solve a Sudoku puzzle. Must be implemented by subclasses.
    """

    @abstractmethod
    def solve(self, board: SudokuBoard) -> Tuple[Optional[SudokuBoard], str]:
        """
        Abstract method to solve a Sudoku puzzle.

        Given a SudokuBoard object representing a Sudoku puzzle, this method should be implemented
        by subclasses to provide the logic for solving the puzzle. The method returns a solved
        SudokuBoard object if a solution is found or None along with a status message.

        Parameters
        ----------
        board : SudokuBoard
            The Sudoku puzzle to be solved, represented as a SudokuBoard object.

        Returns
        -------
        Tuple[Optional[SudokuBoard], str]
            A SudokuBoard object representing the solved puzzle, or None if the puzzle cannot be
            solved with the implemented solving algorithm. A status message is also returned as a
            string, indicating the outcome of the solving process.
        """
        pass


class BacktrackingSolverBasic(Solver):
    """
    Class for solving Sudoku puzzles using a backtracking algorithm.

    This class implements a standard backtracking algorithm for solving Sudoku puzzles.
    It explores possible solutions with depth first search strategy (DFS). Undoing moves
    that lead to a dead end, until it finds a valid solution or exhausts all possibilities.

    Parameters
    ----------
    timeout : int, optional
        The maximum time allowed for solving the puzzle, in seconds. If not set,
        the solver will have be initialised with a default timeout of 1 minute.

    Attributes
    ----------
    timeout : int or None
        The maximum duration in seconds allowed for the solver to run.

    Methods
    -------
    solve(board: SudokuBoard) -> Tuple[Optional[SudokuBoard], str]
        Solve the Sudoku puzzle using the backtracking algorithm. Sets the board attribute
        to the input board and calls the private method _backtrack().
    _backtrack() -> bool:
        Recursively solve the Sudoku puzzle by applying the backtracking algorithm.


    Examples
    --------
    >>> sudoku_board = SudokuBoard(...)
    >>> solver = BacktrackingSolver(timeout=120)
    >>> solved_board, status = solver.solve(sudoku_board)
    >>> print(solved_board)
    SudokuBoard(...)
    >>> print(status)
    "Solved"
    """

    def __init__(self, timeout: float = 60):
        """
        Initialise the BacktrackingSolverBasic with an optional timeout.

        Parameters
        ----------
        timeout : int, optional
            The maximum time, in seconds, allowed for the solver to run. The default is 60 seconds.
        """
        self.timeout = timeout

    def _backtrack(self) -> bool:
        """
        Apply a backtracking algorithm to a sudoku puzzle.

        This private method implements the core of the backtracking algorithm.
        It uses a recursive depth-first search to explore all possible solutions,
        starting from the initial state of the Sudoku board. This method systematically tries
        every valid option for each empty cell and backtracks when it reaches a state
        where it can’t make any valid moves.

        Returns
        -------
        bool
            True if the puzzle was solved successfully, False otherwise.
            For this solver, False means that the puzzle cannot be solved.

        Raises
        ------
        TimeoutException
            If the solution process exceeds the specified timeout duration.

        Notes
        -----
        Acts on the board attribute, which should be set prior by the solve() method which
        is expected to be the method which calls this private method.
        """
        # Check for timeout.
        if self.timeout and (time.time() - self.start_time > self.timeout):
            raise TimeoutException  # Raise an exception when timeout occurs

        # Get empty square indices.
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

    def solve(self, board: SudokuBoard) -> Tuple[Optional[SudokuBoard], str]:
        """
        Solve the Sudoku puzzle using a backtracking algorithm.

        This method attempts to solve the provided Sudoku puzzle by applying a backtracking
        algorithm.  It sets the board attribute to the input board and calls _backtrack().

        If a solution is found, it returns the solved board and a status message "Solved".
        If the board has no solution, it returns None and a status message "Board has no solution".
        If the solving process exceeds the specified timeout duration, it raises a TimeoutException
        and returns None and a status message "Timeout occurred".

        Parameters
        ----------
        board : SudokuBoard
            The Sudoku puzzle to be solved, represented as a SudokuBoard object.

        Returns
        -------
        Tuple[Optional[SudokuBoard], str]
            A tuple where the first element is the solved Sudoku board if a solution is found,
            otherwise None. The second element is a status message as a string, indicating the
            outcome of the solving process. Possible status messages are "Solved",
            "Timeout occurred" or "Board has no solution".

        Raises
        ------
        TimeoutException
            If the solving process exceeds the specified timeout duration.

        Notes
        -----
        This method sets the board attribute of the class instance. It makes a deep copy
        of the original board before starting the solving process, so that it can compare the
        original and processed boards to determine if a solution was found. As if the board has
        no solution, the backtracking process will leave the board in its original configuration.
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


class BacktrackingSolverEasiestFirst(BacktrackingSolverBasic):
    """
    Class for solving Sudoku puzzles using a backtracking algorithm, with a heuristic that
    chooses the cell with the fewest possible options at each step.

    This class implements a backtracking algorithm for solving Sudoku puzzles, with an added
    heuristic: at each step, it chooses the cell with the fewest possible options and only
    loops over those options. This heuristic can significantly speed up the solving process
    for harder puzzles, although it may slightly slow down the process for easier puzzles due
    to the overhead of finding the cell with the fewest options at each step.

    Methods
    -------
    _find_easiest_cell(board: SudokuBoard, row_idxs: List[int], col_idxs: List[int]) \
    -> Tuple[int, int, Set[int]]
        Identify the cell on a Sudoku board with the fewest possible options, and return a tuple
        containing the cell's row and column indices and the set of valid options for that cell.
        This method is used internally by the backtracking algorithm to pick the next cell to fill.

    _backtrack() -> bool:
        Recursively solve the Sudoku puzzle using the backtracking algorithm, choosing the next
        cell to fill based on the heuristic of fewest options. This method acts on the board
        attribute, which should be set prior to calling this method via the solve() method.

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
    ) -> Tuple[int, int, Set[int]]:
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
        Tuple[int, int, Set[int]]
            A tuple containing the row index, column index, and the set of possible values
            for the identified cell.

        Notes
        -----
        The method assumes that the lists `row_idxs` and `col_idxs` are found by calling
        `board.get_empty_cells()`. It relies on `board.find_possible_cell_values()`
        to determine the potential values for each cell.

        Examples
        --------
        >>> sudoku_board = SudokuBoard(...)
        >>> solver = BacktrackingSolverWithRules(timeout=60)
        >>> easiest_cell_tuple = solver._find_easiest_cell(sudoku_board, [0, 1, 2], [0, 1, 2])
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

    def _backtrack(self) -> bool:
        """
        Private method for recursively solving the Sudoku puzzle using a backtracking algorithm.

        This method applies a backtracking algorithm to solve the Sudoku puzzle. It starts by
        checking for a timeout. If the timeout has been exceeded, it raises a TimeoutException.

        Next, it retrieves the coordinates of the empty cells on the board. If there are no empty
        cells, it returns True, indicating that the puzzle is solved.

        If there are empty cells, it selects the one with the fewest possible values and loops
        over those values. For each value, it places the value in the cell and makes a recursive
        call to itself. If the recursive call returns True, it also returns True, indicating that
        the puzzle is solved.

        If none of the values result in a solved puzzle, it undoes the last move and returns False,
        triggering backtracking in the previous recursive call.

        Returns
        -------
        bool
            True if the puzzle is solved, False otherwise.

        Raises
        ------
        TimeoutException
            If the solving process exceeds the specified timeout duration.

        Notes
        -----
        This method acts on the board attribute of the class instance which should be set in the
        solve() method which is expected to be the method which calls this method.
        """
        # Check for timeout.
        if self.timeout and (time.time() - self.start_time > self.timeout):
            raise TimeoutException  # Raise an exception when timeout occurs

        # Get empty square row and col indices.
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

        # Incorrect move was made previously, backtrack.
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
        Sets the solving strategy to be used. The `solver` parameter should be a string
        representing the name of the solver, and `solver_kwargs` should be a dictionary
        of keyword arguments to pass to the solver's constructor.

    solve(board: SudokuBoard) -> Tuple[Optional[SudokuBoard], str]:
        Solves the Sudoku puzzle using the selected strategy. The `board` parameter should
        be an instance of the SudokuBoard class representing the puzzle to be solved.
        Returns the solved SudokuBoard if a solution is found, or None if no solution is found
        along with a status message.

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

        The solver_dict attribute is a dictionary that maps solver names (as strings) to their
        corresponding solver classes. This allows the solver to be easily selected by name.
        """
        # If a new solver is added, add it to this dictionary.
        # Will automatically be available as an option via the --solver flag in main.py.
        self.solver_dict = {
            "bt_basic": BacktrackingSolverBasic,
            "bt_easiest_first": BacktrackingSolverEasiestFirst,
        }

    def set_solver(self, solver: str, solver_kwargs: Dict = None):
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
                f"Solver {solver} is not a valid option, please choose from "
                f"{list(self.solver_dict.keys())}"
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
            If a solver has not been set prior to calling this method
            (i.e., if `self.solver` is None).

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
