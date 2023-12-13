import time
from exceptions import TimeoutException
from abc import ABC, abstractmethod
from sudoku_board import SudokuBoard
from typing import Union


class Solver(ABC):
    @abstractmethod
    def solve(self, board: SudokuBoard) -> Union[SudokuBoard, None]:
        pass


class BacktrackingSolver(Solver):
    """
    Class for solving sudoku puzzles using a backtracking algorithm
    """

    def __init__(self, timeout):
        self.timeout = timeout

    def _backtrack(self):
        """
        Solve the sudoku puzzle using a backtracking algorithm

        Returns
        -------
        bool
            True if the puzzle was solved, False otherwise
        """
        # Check for timeout
        if self.timeout and (time.time() - self.start_time > self.timeout):
            raise TimeoutException  # Raise an exception when timeout occurs

        # find the next empty square
        I, J = self.board.get_empty_cells()

        # if there are no empty squares, the puzzle is solved
        if I is None:
            return True

        # related_cells_list = [len(board.get_related(I[idx], J[idx])) for
        # # loop over all empty cells
        # for idx in I:
        #     i, j = I[idx], J[idx]
        #     # related = {1,2,3,4}
        #     related =

        i, j = I[0], J[0]

        # check which numbers are valid in the empty square
        for num in range(1, 10):
            if self.board.check_valid(i, j, num):
                # make the move and repeat recursively
                self.board.place_number(i, j, num)
                if self._backtrack():
                    # puzzle was solved
                    return True

                # if the puzzle was not solved, undo the move
                self.board.remove_number(i, j, num)

        # if no numbers worked, an incorrect move was made somewhere
        # return False to backtrack
        return False

    def solve(self, board):
        """
        Solve the sudoku puzzle

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
        if self.timeout:
            self.start_time = time.time()
        try:
            self._backtrack()
        except TimeoutException:
            return None
        return self.board


# class BacktrackingSolverWithConstraints(BacktrackingSolver):
#     """
#     Class for solving sudoku puzzles using a backtracking algorithm with constraints
#     """
#     def reduce_sudoku():
#         stalled = False
#         while not stalled:
#             numbers_placed_before = self.board.filled_values


#     def solve(self, board):
#         """
#         Solve the sudoku puzzle

#         Returns
#         -------
#         bool
#             True if the puzzle was solved, False otherwise
#         """
#         self.board = board
#         self._backtrack()
#         return self.board


class SudokuSolver(Solver):
    def __init__(self):
        self.solver_dict = {
            "backtracking": BacktrackingSolver,
            # "backtracking_with_constraints": BacktrackingSolverWithConstraints,
        }

    def set_solver(self, solver: str, solver_kwargs):
        try:
            self.solver = self.solver_dict[solver](**solver_kwargs)
        except KeyError:
            raise ValueError(f"Solver {solver} is not valid")

    def solve(self, board: SudokuBoard) -> Union[SudokuBoard, None]:
        return self.solver.solve(board)