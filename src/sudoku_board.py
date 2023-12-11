import numpy as np
import copy


class SudokuBoard:
    def __init__(self, sudoku_board, verbose=False):
        board = np.asarray(sudoku_board)

        # check dtype of board
        if not np.issubdtype(board.dtype, np.integer):
            raise TypeError("Input array must only contain integers")

        self._board = board
        self._original_board = copy.deepcopy(sudoku_board)

        # check board follows the rules of sudoku
        self._validate_board_legality()

        # if less than 17 squares are filled, the puzzle has multiple solutions
        # src: https://arxiv.org/abs/1201.0749
        if np.count_nonzero(self._board) < 17:
            raise ValueError("Puzzle has multiple solutions")

        self.rows = [set() for _ in range(9)]
        self.columns = [set() for _ in range(9)]
        self.subgrids = [set() for _ in range(9)]

        self._initialize_sets()

    def _initialize_sets(self):
        for i in range(9):
            for j in range(9):
                num = self._board[i][j]
                if num != 0:
                    self.rows[i].add(num)
                    self.columns[j].add(num)
                    self.subgrids[(i // 3) * 3 + (j // 3)].add(num)

    def reset(self):
        """
        Reset the board to its original state
        """
        self._board = copy.deepcopy(self._original_board)

    def __str__(self):
        """
        Formats the string representation of the board in a visually appealing format
        Use a . for a blank square instead of a 0.
        Add some whitespace between the 3x3 squares.
        """
        board_str = ""
        for i in range(9):
            for j in range(9):
                board_str += str(self._board[i][j]) if self._board[i][j] != 0 else "."
                if (j + 1) % 3 == 0 and j < 8:
                    board_str += " | " if j < 8 else ""
                elif j < 8:
                    board_str += " "
            if (i + 1) % 3 == 0 and i < 8:
                board_str += "\n------+-------+------\n"
            else:
                board_str += "\n"
        return board_str

    def __getitem__(self, position: tuple()):
        """
        Returns the value of the board at the given position.
        """
        return self._board[position]

    def __setitem__(self, position: tuple(), value: int):
        """
        Sets the value of the board at the given position.
        """

        if not isinstance(value, int) or not 0 <= value <= 9:
            raise ValueError("Value must be an integer between 0 and 9")
        self._board[position] = value

    def _validate_board_legality(self):
        # check they all elements in the board are in range 0-9
        valid_elements = np.all(np.logical_and(self._board >= 0, self._board <= 9))
        if not valid_elements:
            error_message = (
                "[ERROR] Input string does not represent a valid Sudoku board\n"
                "All elements must be integers between 0 and 9"
            )
            raise ValueError(error_message)

        # define a helper functions to check for duplicates in the sudoku board
        def duplication_check_1d(arr):
            # if duplicates present in arr
            # number of unique els greater than 0 will be less than the number of non-zero els
            return len(np.unique(arr[arr > 0])) < np.count_nonzero(arr > 0)

        # check for duplicates in rows and columns of the board
        duplicate_in_rows = np.apply_along_axis(duplication_check_1d, 1, self._board)
        duplicate_in_cols = np.apply_along_axis(duplication_check_1d, 0, self._board)

        # flatten each 3x3 subgrid into a row of a new board
        flattened_subgrids_board = np.array(
            [
                self._board[i : i + 3, j : j + 3].flatten()
                for i in range(0, 9, 3)
                for j in range(0, 9, 3)
            ]
        )

        # check for any duplicates in the flattened subgrid board's rows to
        duplicate_in_subgrids = np.apply_along_axis(
            duplication_check_1d, 1, flattened_subgrids_board
        )

        # if any of the above checks are true, the board is not valid
        valid = not (
            np.any(duplicate_in_rows) or np.any(duplicate_in_cols) or np.any(duplicate_in_subgrids)
        )

        if not valid:
            error_message = (
                "[ERROR] Input string does not represent a valid Sudoku board\n"
                "Duplicate values found in rows, columns, or subgrids"
            )
            # potential room for improvement: return the indices of the duplicates/print the board
            raise ValueError(error_message)

    def check_valid(self, row, col, num):
        subgrid_index = (row // 3) * 3 + (col // 3)
        return (
            num not in self.rows[row]
            and num not in self.columns[col]
            and num not in self.subgrids[subgrid_index]
        )

    def place_number(self, row, col, num):
        self._board[row][col] = num
        self.rows[row].add(num)
        self.columns[col].add(num)
        self.subgrids[(row // 3) * 3 + (col // 3)].add(num)

    def remove_number(self, row, col, num):
        self._board[row][col] = 0
        self.rows[row].remove(num)
        self.columns[col].remove(num)
        self.subgrids[(row // 3) * 3 + (col // 3)].remove(num)

    def find_empty(self):
        """
        Finds the next empty square in the board (left to right, top to bottom)

        Returns
        -------
        tuple
            (row index, column index) of the next empty square,
            or (None, None) if there are no empty squares
        """
        empty_cells = np.where(self._board == 0)
        if empty_cells[0].size > 0:
            return empty_cells[0][0], empty_cells[1][0]
        else:
            return None, None
