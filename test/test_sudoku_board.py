from sudoku_format_handlers import SudokuFormatHandler
import pytest
import numpy as np


def test_sudoku_board_rule_validation():
    # Check SudokuBoard class can detect invalid boards on initialisation
    # by checking that it raises a ValueError.
    invalid_input_1 = "test/sudoku_board_test_boards/invalid_input_1.txt"
    invalid_input_2 = "test/sudoku_board_test_boards/invalid_input_2.txt"
    invalid_input_3 = "test/sudoku_board_test_boards/invalid_input_3.txt"

    format_handler = SudokuFormatHandler()

    # .parse() returns an initialised SudokuBoard object.
    with pytest.raises(ValueError):
        # duplication in column
        format_handler.parse(invalid_input_1, format="grid")
        # duplication in row
        format_handler.parse(invalid_input_2, format="grid")
        # duplication in 3x3 square
        format_handler.parse(invalid_input_3, format="grid")


def test_board_representation():
    # Check that the board is correctly loaded as a numpy array.
    INPUT = "test/sudoku_parser_test_boards/good_input.txt"
    expected_answer = np.asarray(
        [
            [0, 0, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 5, 0, 4],
            [0, 0, 0, 0, 5, 0, 1, 6, 9],
            [0, 8, 0, 0, 0, 0, 3, 0, 5],
            [0, 7, 5, 0, 0, 0, 2, 9, 0],
            [4, 0, 6, 0, 0, 0, 0, 8, 0],
            [7, 6, 2, 0, 8, 0, 0, 0, 0],
            [1, 0, 3, 9, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 0],
        ]
    )
    format_handler = SudokuFormatHandler()
    board = format_handler.parse(INPUT, format="grid")
    assert np.array_equal(board._board, expected_answer)


def test_board_manipulation():
    # Check that the board can be indexed like a numpy array.
    # Check the board manipulation logic works as expected.
    INPUT = "test/sudoku_parser_test_boards/good_input.txt"

    format_handler = SudokuFormatHandler()
    board = format_handler.parse(INPUT, format="grid")

    # Test that the board cannot be set to an invalid value.
    with pytest.raises(ValueError):
        board.place_number(0, 0, 10)
        board.place_number(0, 0, 0.2)
        board.place_number(0, 0, -1)
        # Invalid move.
        board.place_number(0, 0, 1)

    original_number_filled = board.filled_values

    # Test that the board can be set to a valid value.
    board.place_number(0, 0, 2)

    # Test the board can be indexed like a numpy array.
    assert board[0, 0] == 2

    # Test that the attributes are properly updated.
    assert board.rows[0] == set([2, 7])
    assert board.columns[0] == set([1, 2, 4, 7])
    assert board.subgrids[0] == set([2])
    assert board.filled_values == original_number_filled + 1

    # Test that numbers can be removed from the board.
    board.remove_number(0, 0)
    assert board[0, 0] == 0

    # Test that the attributes are properly updated.
    assert board.rows[0] == set([7])
    assert board.columns[0] == set([1, 4, 7])
    assert board.subgrids[0] == set([])
    assert board.filled_values == original_number_filled


def test_print_formatting():
    # Check that SudokuBoards string representation
    # allows the the board state to be shown in a nice format.
    INPUT = "test/sudoku_solver_test_boards/easy_1.txt"
    format_handler = SudokuFormatHandler()

    exp_str = (
        "9 1 . | . . . | 4 2 7\n"
        ". . . | . . 3 | 9 1 5\n"
        "2 5 4 | 7 . . | 6 8 .\n"
        "------+-------+------\n"
        "4 7 . | . 8 6 | . 3 2\n"
        ". 6 . | 4 . . | . . 8\n"
        "5 . . | . 1 2 | . 6 .\n"
        "------+-------+------\n"
        "3 4 . | 6 2 . | . . 1\n"
        ". . . | 3 . . | . . .\n"
        ". 2 6 | . . 8 | . . 9\n"
    )
    board = format_handler.parse(INPUT, format="grid")

    assert str(board) == exp_str


def test_reset_method():
    # Check that the board can be reset to its original state.
    INPUT = "test/sudoku_solver_test_boards/easy_1.txt"
    format_handler = SudokuFormatHandler()
    board = format_handler.parse(INPUT, format="grid")
    board.place_number(0, 2, 3)
    board.reset()
    assert np.array_equal(board._board, board._original_board)


def test_find_empty_method():
    # Check that the board can find the next empty space.
    INPUT = "test/sudoku_solver_test_boards/easy_1.txt"
    format_handler = SudokuFormatHandler()
    board = format_handler.parse(INPUT, format="grid")
    I, J = board.get_empty_cells()
    assert (I[0], J[0]) == (0, 2)


def test_check_valid_method():
    # Check that the board can check if a move is valid.
    INPUT = "test/sudoku_solver_test_boards/easy_1.txt"
    format_handler = SudokuFormatHandler()
    board = format_handler.parse(INPUT, format="grid")
    assert board.check_valid(0, 2, 3)
    assert not board.check_valid(0, 2, 5)


def test_get_related_method():
    # Check that the board can find the options available to a cell
    # given values filled in related cells.
    INPUT = "test/sudoku_solver_test_boards/easy_1.txt"
    format_handler = SudokuFormatHandler()
    board = format_handler.parse(INPUT, format="grid")
    vals = board.find_possible_cell_values(0, 2)
    expected_vals = set([3, 8])
    assert vals == expected_vals
