from src import solvers, utils
import numpy as np


def test_sudoku_solver_class():
    # load in a board
    with open("test/test_boards/good_input.txt", "r") as f:
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
    assert solver.check_valid(0, 0, 2)

    # check that the solver can check if a move is invalid
    assert not solver.check_valid(0, 0, 1)
