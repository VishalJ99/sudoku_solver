from sudoku_parser import SudokuParser
import pytest
import numpy as np
import os


def test_sudoku_board_rule_validation():
    # Check SudokuBoard class can detect invalid boards on initialisation
    # by checking that it raises a ValueError.
    invalid_input_1 = "test/sudoku_board_test_boards/invalid_input_1.txt"
    invalid_input_2 = "test/sudoku_board_test_boards/invalid_input_2.txt"
    invalid_input_3 = "test/sudoku_board_test_boards/invalid_input_3.txt"

    # .parse() returns an initialised SudokuBoard object.
    with pytest.raises(ValueError):
        # duplication in column
        SudokuParser(invalid_input_1).parse()
        # duplication in row
        SudokuParser(invalid_input_2).parse()
        # duplication in 3x3 square
        SudokuParser(invalid_input_3).parse()


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

    board = SudokuParser(INPUT).parse()
    assert np.array_equal(board._board, expected_answer)


def test_get_set():
    # Check that the board can be indexed like a numpy array.
    # Check the error handling for invalid values.
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

    board = SudokuParser(INPUT).parse()

    # Test setter.
    board[0, 0] = 1
    expected_answer[0, 0] = 1
    assert np.array_equal(board._board, expected_answer)

    # Test getter.
    assert board[0, 0] == 1

    # Test that the board cannot be set to an invalid value.
    with pytest.raises(ValueError):
        board[0, 0] = 10
        board[0, 0] = 1.1


def test_print_formatting():
    # Check that SudokuBoards string representation
    # allows the the board state to be shown in a nice format.

    INPUT = "test/sudoku_solver_test_boards/easy_1.txt"

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
    board = SudokuParser(INPUT).parse()

    assert str(board) == exp_str


@pytest.fixture
def setup_board():
    # use a fixture so that if test fails, the file is still deleted
    INPUT = "test/sudoku_solver_test_boards/easy_1_solution.txt"
    SAVE_PATH = "test/sudoku_solver_test_boards/temp_solution.txt"
    board = SudokuParser(INPUT).parse()

    yield board, SAVE_PATH, INPUT

    # Teardown: This runs after the test
    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)


# test board save method works
def test_save_method(setup_board):
    board, SAVE_PATH, INPUT = setup_board
    board.save(SAVE_PATH)

    with open(INPUT, "r") as f1, open(SAVE_PATH, "r") as f2:
        original_board_content = f1.read()
        saved_board_content = f2.read()

    assert original_board_content == saved_board_content


def test_reset_method():
    # Check that the board can be reset to its original state
    INPUT = "test/sudoku_solver_test_boards/easy_1.txt"
    board = SudokuParser(INPUT).parse()
    board[0, 0] = 1
    board.reset()
    assert np.array_equal(board._board, board._original_board)


def test_find_empty_method():
    # Check that the board can find the next empty space
    INPUT = "test/sudoku_solver_test_boards/easy_1.txt"
    board = SudokuParser(INPUT).parse()
    assert board.find_empty() == (0, 2)


def test_check_valid_method():
    # Check that the board can check if a move is valid
    INPUT = "test/sudoku_solver_test_boards/easy_1.txt"
    board = SudokuParser(INPUT).parse()
    assert board.check_valid(0, 2, 3)
    assert not board.check_valid(0, 2, 5)
