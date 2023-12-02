from src import utils


def test_sudoku_board_validation():
    with open("test/test_boards/good_input.txt", "r") as f:
        input_string = f.readlines()

    assert utils.validate_sudoku_input(input_string)


def test_sudoku_parser():
    pass


def test_backtracking_solver():
    pass
