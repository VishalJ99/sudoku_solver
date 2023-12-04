from src import solvers, utils
import numpy as np
import os

EASY_BOARD_1_PATH = "test/test_solver_boards/easy_1.txt"
EASY_BOARD_1_SOLUTION_PATH = "test/test_solver_boards/easy_1_solution.txt"
TEST_SAVE_PATH = "test/test_solver_boards/test_save.txt"


def test_sudoku_solver_class():
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
    assert solver.check_valid(0, 2, 3)

    # check that the solver can check if a move is invalid
    assert not solver.check_valid(0, 2, 5)

    # check that the solver can find the next empty space
    assert solver.find_empty() == (0, 2)

    # check that the solver can print the board in a nice format
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

    assert str(solver) == exp_str

    solver.reset()

    solver.save_board(TEST_SAVE_PATH)

    with open(EASY_BOARD_1_PATH, "r") as f1:
        original_board_content = f1.read()
    with open(TEST_SAVE_PATH, "r") as f2:
        saved_board_content = f2.read()

    assert original_board_content == saved_board_content
    os.remove(TEST_SAVE_PATH)


def test_backtracking_solver():
    # load in a board
    with open(EASY_BOARD_1_PATH, "r") as f:
        good_input = f.readlines()

    with open(EASY_BOARD_1_SOLUTION_PATH, "r") as f:
        known_solution = f.read()

    board = utils.parse_sudoku_input(good_input)
    bt_solver = solvers.BacktrackingSolver(board)
    bt_solver.solve()
    bt_solver.save_board(TEST_SAVE_PATH)

    with open(TEST_SAVE_PATH, "r") as f:
        bt_solution = f.read()

    assert bt_solution == known_solution
    os.remove(TEST_SAVE_PATH)
