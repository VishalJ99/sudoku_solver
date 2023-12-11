from sudoku_format_handler import SudokuFormatHandler
from sudoku_board import SudokuBoard
from exceptions import FormatError
import pytest
import numpy as np


def test_parser():
    # Define the paths to the test boards
    clean_input = "test/sudoku_parser_test_boards/good_input.txt"
    bad_input_1 = "test/sudoku_parser_test_boards/bad_input_1.txt"
    bad_input_2 = "test/sudoku_parser_test_boards/bad_input_2.txt"
    bad_input_3 = "test/sudoku_parser_test_boards/bad_input_3.txt"
    bad_input_4 = "test/sudoku_parser_test_boards/bad_input_4.txt"
    correctable_input = "test/sudoku_parser_test_boards/correctable_input.txt"
    wrong_extension = "test/sudoku_parser_test_boards/wrong_extension.txt"

    # Create a format handler object
    handler = SudokuFormatHandler()

    # this board should load without raising any errors
    assert type(handler.parse(clean_input, format="grid")) is SudokuBoard

    # this board should be corrected and load without raising any errors
    board = handler.parse(correctable_input, format="grid")
    assert type(board) is SudokuBoard

    # check that the board correction worked
    corrected_board_data = board._board
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

    assert np.array_equal(corrected_board_data, expected_answer)

    # these boards should raise FormatErrors
    with pytest.raises(FormatError):
        handler.parse(bad_input_1, format="grid")
        handler.parse(bad_input_2, format="grid")
        handler.parse(bad_input_3, format="grid")
        handler.parse(bad_input_4, format="grid")
        handler.parse(wrong_extension, format="grid")

    # these should raise FileNotFoundErrors
    with pytest.raises(FileNotFoundError):
        handler.parse("nonexistent_file.txt", format="grid")
