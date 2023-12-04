from src import solvers, utils
import numpy as np
import os


def test_sudoku_solver_class():
    EASY_BOARD_1_PATH = "test/test_solver_boards/easy_1.txt"
    TEST_SAVE_PATH = "test/test_solver_boards/test_save.txt"

    # load in a board
    with open(EASY_BOARD_1_PATH, "r") as f:
        good_input = f.readlines()
    board = utils.parse_sudoku_input(good_input)

    # initialize a solver object
    solver = solvers.SudokuSolver(board)

    # check that the board is the same
    assert np.array_equal(solver.board, board)

    # make a move and check that the board is different
    solver.board[0, 0] = 1
    assert not np.array_equal(solver.board, board)

    # reset the board and check that it is the same as the original
    solver.reset()
    assert np.array_equal(solver.board, board)

    # check that the solver can check if a move is valid
    assert solver.check_valid(0, 2, 5)

    # check that the solver can check if a move is invalid
    assert not solver.check_valid(0, 2, 3)

    # check that the solver can find the next empty space
    assert solver.find_empty() == (0, 2)

    # check that the solver can print the board in a nice format
    exp_str = (
        "9 1 . | 3 4 . | . . 7\n"
        ". 8 3 | . 9 7 | . 5 .\n"
        "4 2 7 | . . . | . 1 .\n"
        "------+-------+------\n"
        ". . 2 | 6 8 . | 4 . .\n"
        "7 . 4 | 2 . 9 | . . .\n"
        ". . 8 | . 3 4 | 1 6 .\n"
        "------+-------+------\n"
        "8 . . | . . . | . 4 .\n"
        ". . 9 | . . . | 7 2 6\n"
        ". 5 6 | . . 3 | 8 . 1\n"
    )

    assert str(solver) == exp_str

    solver.reset()

    solver.save_board(TEST_SAVE_PATH)

    with open(EASY_BOARD_1_PATH, "r") as f1:
        original_board_content = f1.read()
    with open(TEST_SAVE_PATH, "r") as f2:
        saved_board_content = f2.read()

    assert original_board_content == saved_board_content
    os.remove(TEST_SAVE_PATH)
