from src.sudoku_parser import SudokuParser
from sudoku_board import SudokuBoard
from exceptions import FormatError
import pytest


def test_parser():
    # Define the paths to the test boards
    clean_input = "test/sudoku_parser_test_boards/good_input.txt"
    bad_input_1 = "test/sudoku_parser_test_boards/bad_input_1.txt"
    bad_input_2 = "test/sudoku_parser_test_boards/bad_input_2.txt"
    bad_input_3 = "test/sudoku_parser_test_boards/bad_input_3.txt"
    bad_input_4 = "test/sudoku_parser_test_boards/bad_input_4.txt"
    correctable_input = "test/sudoku_parser_test_boards/correctable_input.txt"
    wrong_extension = "test/sudoku_parser_test_boards/wrong_extension.txt"

    # this boards should load without raising any errors
    assert type(SudokuParser(clean_input).parse()) is SudokuBoard

    # this board should be corrected and load without raising any errors
    parser = SudokuParser(correctable_input)
    parser.parse()

    # check that the board correction worked
    corrected_board_data = parser._board_data
    expected_answer = [
        "000|007|000",
        "000|009|504",
        "000|050|169",
        "---+---+---",
        "080|000|305",
        "075|000|290",
        "406|000|080",
        "---+---+---",
        "762|080|000",
        "103|900|000",
        "000|600|000",
    ]

    assert corrected_board_data == expected_answer

    # these boards should raise FormatErrors
    with pytest.raises(FormatError):
        SudokuParser(bad_input_1).parse()
        SudokuParser(bad_input_2).parse()
        SudokuParser(bad_input_3).parse()
        SudokuParser(bad_input_4).parse()
        SudokuParser(wrong_extension).parse()

    # these should raise FileNotFoundErrors
    with pytest.raises(FileNotFoundError):
        SudokuParser("nonexistent_file.txt").parse()
