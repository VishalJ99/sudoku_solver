import copy


class SudokuSolver:
    """
    Base class for all sudoku solvers
    """

    def __init__(self, board):
        """
        Initialize the SudokuSolver object

        Parameters
        ----------
        board : numpy.ndarray
            2D numpy array representing the sudoku board to be solved
        """
        self.board = copy.deepcopy(board)
        self.original_board = copy.deepcopy(board)

    def reset(self):
        """
        Reset the board to its original state
        """
        self.board = copy.deepcopy(self.original_board)

    def check_valid(self, row_i, col_j, num):
        """
        Check if a number is valid in the given position given the current state of the board

        Parameters
        ----------
        row_i : int
            row index
        col_j : int
            column index

        Returns
        -------
        bool
            True if the number is valid in the given position, False otherwise
        """
        assert num in range(1, 10)

        for i in range(9):
            # Check if the number is already in the row or column
            if (self.board[row_i, i] == num) or (self.board[i, col_j] == num):
                return False

        # find out which 3x3 square the number is in
        i_0 = (row_i // 3) * 3
        j_0 = (col_j // 3) * 3

        # Check if the number is already in the 3x3 square
        for i in range(3):
            for j in range(3):
                if self.board[i_0 + i, j_0 + j] == num:
                    return False

        # move is valid
        return True

    def find_empty(self):
        """
        Find the next empty square in the board

        Returns
        -------
        tuple
            (row index, column index) of the next empty square,
            or (None, None) if there are no empty squares
        """
        for i in range(9):
            for j in range(9):
                if self.board[i, j] == 0:
                    return i, j
        return None, None

    def __str__(self):
        """
        Formats the string representation of the board in a visually appealing format
        Use a . for a blank square instead of a 0. Add some whitespace between the 3x3 squares.
        """
        board_str = ""
        for i in range(9):
            for j in range(9):
                board_str += str(self.board[i][j]) if self.board[i][j] != 0 else "."
                if (j + 1) % 3 == 0 and j < 8:
                    board_str += " | " if j < 8 else ""
                elif j < 8:
                    board_str += " "
            if (i + 1) % 3 == 0 and i < 8:
                board_str += "\n------+-------+------\n"
            else:
                board_str += "\n"
        return board_str
