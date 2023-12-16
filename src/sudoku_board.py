import numpy as np
import copy
from typing import List, Set, Optional, Tuple


class SudokuBoard:
    """
    A class for representing a Sudoku puzzle board using a 2D numpy array and sets.
    Uses sets to represent numbers in each row, column, and 3x3 subgrid.
    Uses a 2D numpy array to represent the board state.

    Attributes
    ----------
    _board : np.ndarray
        A 2D array representing the current state of the Sudoku board.
    _original_board : np.ndarray
        A 2D array representing the original state of the Sudoku board.
    _all_possible_values : set
        A set containing all possible values that can be placed in the Sudoku board.
    rows : list of set
        A list containing sets, each representing numbers present in each row of the board.
    columns : list of set
        A list containing sets, each representing numbers present in each column of the board.
    subgrids : list of set
        A list containing sets, each representing numbers present in each 3x3 subgrid of the board.
    filled_values : int
        A count of the number of filled squares on the Sudoku board.

    Methods
    -------
    __init__(sudoku_board, verbose=False)
        Initialises the SudokuBoard with a given board state.
    reset()
        Resets the Sudoku board to its original state.
    __str__()
        Returns a formatted string representation of the Sudoku board.
    __getitem__(position)
        Returns the value at the specified position on the Sudoku board.
    __setitem__(position, value)
        Sets the value at the specified position on the Sudoku board.
    _validate_board_legality()
        Validates if the Sudoku board follows the basic rules of Sudoku.
    check_valid(row, col, num)
        Checks if a number can be legally placed in the specified row and column.
    place_number(row, col, num)
        Places a number on the Sudoku board at the specified row and column.
    remove_number(row, col, num)
        Removes a number from the Sudoku board at the specified row and column.
    get_related_cell_values(row, col)
        Finds values in cells that are related to the given cell.
    get_empty_cells()
        Finds the next empty square in the board.
    """

    def __init__(self, sudoku_board: List[List[int]]):
        """
        Initialise the SudokuBoard with a given board state.

        Parameters
        ----------
        sudoku_board : list of list or np.ndarray
            A 2D array-like object representing the initial state of the Sudoku board.
        verbose : bool, optional
            If True, additional information is printed (e.g., warnings about multiple solutions).

        Raises
        ------
        TypeError
            If the input array does not contain only integers.
        ValueError
            If the input array contains values not in the range 0-9 or if the board is not a valid.
        """

        board = np.asarray(sudoku_board)

        if not np.issubdtype(board.dtype, np.integer):
            raise TypeError("Input array must only contain integers")

        if board.shape != (9, 9):
            raise ValueError("Input array must be 9x9")

        # Create a copy of the board for resetting.
        self._board = board
        self._original_board = copy.deepcopy(sudoku_board)

        # Check board follows the rules of sudoku.
        self._validate_board_legality()

        # If less than 17 squares are filled, the puzzle has multiple solutions
        # src: https://arxiv.org/abs/1201.0749.
        if np.count_nonzero(self._board) < 17:
            print("[WARNING] Puzzle has multiple possible solutions.")

        # Initialise sets for each row, column, and 3x3 subgrid.
        self.rows = [set() for _ in range(9)]
        self.columns = [set() for _ in range(9)]
        self.subgrids = [set() for _ in range(9)]

        # Initalise counter for filled squares.
        self.filled_values = 0

        # Add the initial filled values to their respective sets.
        self._initialise_sets()

    def _initialise_sets(self):
        """
        Initialises the sets of numbers present in each row, column, and 3x3 subgrid of the board.
        This method is typically called during the initialisation of the SudokuBoard to set up
        the initial list of row, column and subgrid set attributes of the board.
        """
        self._all_possible_values = set(range(1, 10))
        for i in range(9):
            for j in range(9):
                num = self._board[i][j]
                if num != 0:
                    self.rows[i].add(num)
                    self.columns[j].add(num)
                    self.subgrids[(i // 3) * 3 + (j // 3)].add(num)

    def reset(self):
        """
        Reset the board to its original state.
        """
        self._board = copy.deepcopy(self._original_board)

    def __str__(self) -> str:
        """
        Formats the string representation of the board in a visually appealing format
        Use a . for a blank square instead of a 0 and adds some whitespace between the 3x3 squares.

        Examples
        --------
        >>> import sys
        >>> sys.path.append('src')
        >>> from sudoku_format_handler import SudokuFormatHandler
        >>> format_handler = SudokuFormatHandler()
        >>> board = format_handler.parse("test/sudoku_solver_test_boards/easy_1.txt")
        >>> print(type(board))
        <class 'sudoku_board.SudokuBoard'>
        >>> print(board)

        The output will be:

        9 1 . | . . . | 4 2 7
        . . . | . . 3 | 9 1 5
        2 5 4 | 7 . . | 6 8 .
        ------+-------+------
        4 7 . | . 8 6 | . 3 2
        . 6 . | 4 . . | . . 8
        5 . . | . 1 2 | . 6 .
        ------+-------+------
        3 4 . | 6 2 . | . . 1
        . . . | 3 . . | . . .
        . 2 6 | . . 8 | . . 9
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

    def __getitem__(self, position: Tuple[int, int]) -> int:
        """
        Returns the value of the board at the given position.

        Parameters
        ----------
        position : Tuple[int, int]
            A tuple representing the (row, column) position on the board.

        Returns
        -------
        int
            The value at the specified position on the board.
        """
        return self._board[position]

    def _validate_board_legality(self):
        """
        Validates if the Sudoku board follows the basic rules of Sudoku.

        This method checks if all elements in the board are integers between 0 and 9 and ensures
        that there are no duplicate values in any row, column, or 3x3 subgrid.
        An exception is raised if the board does not adhere to these rules.

        Raises
        ------
        ValueError
            If any element in the board is not between 0 and 9, or if there are duplicate values
            in anyrow, column, or 3x3 subgrid.

        Notes
        -----
        This method does not check that the elements of the board are integers. This is done in the
        __init__ method.
        """

        # Ensure all elements are in the range 0-9 (0 represents an empty cell).
        valid_elements = np.all(np.logical_and(self._board >= 0, self._board <= 9))
        if not valid_elements:
            error_message = (
                "[ERROR] Input string does not represent a valid Sudoku board\n"
                "All elements must be integers between 0 and 9"
            )
            raise ValueError(error_message)

        # Define a helper functions to check for duplicates in the sudoku board.
        def duplication_check_1d(arr):
            return len(np.unique(arr[arr > 0])) < np.count_nonzero(arr > 0)

        # Flatten each 3x3 subgrid into a row of a new board.
        flattened_subgrids_board = np.array(
            [
                self._board[i : i + 3, j : j + 3].flatten()
                for i in range(0, 9, 3)
                for j in range(0, 9, 3)
            ]
        )

        # Check for duplicates in rows, columns and subgrids of the board.
        duplicate_in_rows = np.apply_along_axis(duplication_check_1d, 1, self._board)
        duplicate_in_cols = np.apply_along_axis(duplication_check_1d, 0, self._board)
        duplicate_in_subgrids = np.apply_along_axis(
            duplication_check_1d, 1, flattened_subgrids_board
        )

        # If any of the above checks are true, the board is not valid.
        valid = not (
            np.any(duplicate_in_rows) or np.any(duplicate_in_cols) or np.any(duplicate_in_subgrids)
        )

        if not valid:
            error_message = (
                "[ERROR] Input string does not represent a valid Sudoku board\n"
                "Duplicate values found in rows, columns, or subgrids"
            )

            # Potential room for improvement: return the indices of the duplicates/print the board.
            raise ValueError(error_message)

    def check_valid(self, row: int, col: int, num: int) -> bool:
        """
        Checks if a given number can be legally placed at a specified row and column.

        It checks if the number already exists in the set representing the relevant row, column,
        or 3x3 subgrid.

        Parameters
        ----------
        row : int
            The row index where the number is to be placed (0-8).
        col : int
            The column index where the number is to be placed (0-8).
        num : int
            The number to be checked (1-9).

        Returns
        -------
        bool
            Returns `True` if the number can be placed without violating Sudoku rules,
            otherwise `False`.
        """
        subgrid_index = (row // 3) * 3 + (col // 3)
        return (
            num not in self.rows[row]
            and num not in self.columns[col]
            and num not in self.subgrids[subgrid_index]
        )

    def place_number(self, row: int, col: int, num: int):
        """
        Places a number on the Sudoku board at the specified row and column,
        ensuring that it adheres to the rules of Sudoku. The method updates
        the board state by adding the number to the respective row, column,
        and 3x3 subgrid sets. It also increments the filled_values counter
        attribute.

        Parameters
        ----------
        row : int
            The row index where the number is to be placed (0-based).
        col : int
            The column index where the number is to be placed (0-based).
        num : int
            The number to be placed on the board.

        Raises
        ------
        ValueError
            If the number is not an integer in the range 1-9.
        ValueError
            If the specified position is invalid or placing the number at the
            given position violates Sudoku rules.

        Notes
        -----
        Checking the number everytime its placed on the board probably adds a bit of unecessary
        overhead for the scope of the coursework, but in terms of SWE best practice, it embodies
        the principle of defensive programming. It is a trade-off that makes this class more robust
        to incorrect solver implementations.
        """
        # Ensure the number being placed is integer in the range 1-9.
        if not isinstance(num, int) or num < 1 or num > 9:
            raise ValueError("Number must be an integer in the range 1-9")

        # Ensure the position is valid.
        if self.check_valid(row, col, num):
            self._board[row][col] = num
            self.rows[row].add(num)
            self.columns[col].add(num)
            self.subgrids[(row // 3) * 3 + (col // 3)].add(num)
            self.filled_values += 1
        else:
            raise ValueError("Number violates sudoku rules at the specified position")

    def remove_number(self, row: int, col: int, num: int):
        """
        Removes a number from the Sudoku board at the specified row and column.
        Removes the number to the sets representing that row, column, and 3x3 subgrid.
        Decrements the filled_values counter attribute.

        Parameters
        ----------
        row : int
            The row index from which the number is to be removed (0-based).
        col : int
            The column index from which the number is to be removed (0-based).
        num : int
            The number to be removed from the board.

        Raises
        ------
        ValueError
            If the specified position is invalid or the number is not in the current board state.
        """

        self._board[row][col] = 0
        self.rows[row].remove(num)
        self.columns[col].remove(num)
        self.subgrids[(row // 3) * 3 + (col // 3)].remove(num)
        self.filled_values -= 1

    def find_possible_cell_values(self, row: int, col: int) -> Set[int]:
        """
        Determines the possible values that can be placed in a specific cell of the Sudoku board.
        It considers the values  present in the cell's row, column, and 3x3 subgrid.

        Parameters
        ----------
        row : int
            The row index of the cell.
        col : int
            The column index of the cell.

        Returns
        -------
        Set[int]
            A set of integers representing the possible values that can be placed in the cell.

        Raises
        ------
        ValueError
            If the specified row or column index is outside the valid range of the Sudoku board.
        """
        # Gather values already present in the same row, column, and subgrid.
        existing_values = set()
        existing_values.update(self.rows[row])
        existing_values.update(self.columns[col])
        existing_values.update(self.subgrids[(row // 3) * 3 + (col // 3)])

        # Calculate the set of values that are not yet present in related cells.
        potential_values = self._all_possible_values - existing_values
        return potential_values

    def get_empty_cells(self) -> Optional[Tuple[List[int], List[int]]]:
        """
        Finds the indices for the empty squares in the board
        order they are returned in is from left to right, top to bottom.

        Returns
        -------
        Optional[Tuple[int, int]]
            (row index, column index) of the next empty square,
            or (None, None) if there are no empty squares.
        """

        empty_cells = np.where(self._board == 0)
        if empty_cells[0].size > 0:
            return empty_cells
        else:
            return None, None
