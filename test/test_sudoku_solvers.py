from sudoku_parser import SudokuParser
from sudoku_solvers import BacktrackingSolver
import os
import pytest

EASY_BOARD_1_PATH = "test/sudoku_solver_test_boards/easy_1.txt"
EASY_BOARD_1_SOLUTION_PATH = "test/sudoku_solver_test_boards/easy_1_solution.txt"
TEST_SAVE_PATH = "test/sudoku_solver_test_boards/easy_1_bt_sol.txt"


@pytest.fixture
def setup_solver_and_board():
    # Setup: Load the board and prepare the solver
    board = SudokuParser(EASY_BOARD_1_PATH).parse()
    bt_solver = BacktrackingSolver(board)

    yield board, bt_solver, EASY_BOARD_1_SOLUTION_PATH, TEST_SAVE_PATH

    # Teardown: This runs after the test
    if os.path.exists(TEST_SAVE_PATH):
        os.remove(TEST_SAVE_PATH)


def test_backtracking_solver(setup_solver_and_board):
    # Tes
    board, bt_solver, known_solution_path, test_save_path = setup_solver_and_board

    with open(known_solution_path, "r") as f:
        known_solution = f.read()

    solved_board = bt_solver.solve()
    solved_board.save(test_save_path)

    with open(test_save_path, "r") as f:
        bt_solution = f.read()

    assert bt_solution == known_solution
