from sudoku_board import SudokuBoard


class BacktrackingSolver:
    """
    Class for solving sudoku puzzles using a backtracking algorithm
    """

    def __init__(self, board: SudokuBoard):
        """
        Initialize the BacktrackingSolver object

        Parameters
        ----------
        board : numpy.ndarray
            2D numpy array representing the sudoku board to be solved
        """
        self.board = board

    def _backtrack(self, log=False):
        """
        Solve the sudoku puzzle using a backtracking algorithm

        Returns
        -------
        bool
            True if the puzzle was solved, False otherwise
        """
        # find the next empty square
        i, j = self.board.find_empty()

        # if there are no empty squares, the puzzle is solved
        if i is None:
            return True

        # check which numbers are valid in the empty square
        for num in range(1, 10):
            if self.board.check_valid(i, j, num):
                # make the move and repeat recursively
                self.board[i, j] = num
                if self._backtrack():
                    # puzzle was solved
                    return True

                # if the puzzle was not solved, undo the move
                self.board[i, j] = 0

        # if no numbers worked, an incorrect move was made somewhere
        # return False to backtrack
        if log:
            print(f"\r{self.board}", end="")
        return False

    def solve(self):
        """
        Solve the sudoku puzzle

        Returns
        -------
        bool
            True if the puzzle was solved, False otherwise
        """
        self._backtrack()
        print(self.board)
        return self.board
