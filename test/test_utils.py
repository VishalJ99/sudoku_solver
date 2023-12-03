from src import utils
import numpy as np
import pytest


def test_sudoku_board_validation():
    with open("test/test_boards/good_input.txt", "r") as f:
        good_input = f.readlines()
    with open("test/test_boards/bad_input_1.txt", "r") as f:
        bad_input_1 = f.readlines()
    with open("test/test_boards/bad_input_2.txt", "r") as f:
        bad_input_2 = f.readlines()
    with open("test/test_boards/bad_input_3.txt", "r") as f:
        bad_input_3 = f.readlines()
    with open("test/test_boards/bad_input_4.txt", "r") as f:
        bad_input_4 = f.readlines()
    with open("test/test_boards/correctable_input.txt", "r") as f:
        correctable_input = f.readlines()

    assert utils.validate_sudoku_input(good_input)
    assert utils.validate_sudoku_input(correctable_input)

    with pytest.raises(ValueError):
        utils.validate_sudoku_input(bad_input_1)
        utils.validate_sudoku_input(bad_input_2)
        utils.validate_sudoku_input(bad_input_3)
        utils.validate_sudoku_input(bad_input_4)


def test_sudoku_parser():
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
    with open("test/test_boards/good_input.txt", "r") as f:
        good_input = f.readlines()

    assert np.array_equal(utils.parse_sudoku_input(good_input), expected_answer)


def test_backtracking_solver():
    pass
