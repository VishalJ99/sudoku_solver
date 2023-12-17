from sudoku_format_handlers import SudokuFormatHandler
from sudoku_solvers import BacktrackingSolverBasic, BacktrackingSolverEasiestFirst
import os
import pytest

EASY_BOARD_1_PATH = "test/sudoku_solver_test_boards/easy_1.txt"
EASY_BOARD_1_SOLUTION_PATH = "test/sudoku_solver_test_boards/easy_1_solution.txt"
TEST_SAVE_PATH = "test/sudoku_solver_test_boards/easy_1_bt_sol.txt"


@pytest.fixture
def setup_basic_solver_and_board():
    # Setup: Load the board and prepare the solver
    format_handler = SudokuFormatHandler()

    board = format_handler.parse(EASY_BOARD_1_PATH, format="grid")
    bt_solver = BacktrackingSolverBasic(timeout=10)

    yield board, bt_solver, EASY_BOARD_1_SOLUTION_PATH, TEST_SAVE_PATH

    # Teardown: This runs after the test
    if os.path.exists(TEST_SAVE_PATH):
        os.remove(TEST_SAVE_PATH)


@pytest.fixture
def setup_easiest_first_solver_and_board():
    # Setup: Load the board and prepare the solver
    format_handler = SudokuFormatHandler()

    board = format_handler.parse(EASY_BOARD_1_PATH, format="grid")
    bt_solver = BacktrackingSolverEasiestFirst(timeout=10)

    yield board, bt_solver, EASY_BOARD_1_SOLUTION_PATH, TEST_SAVE_PATH

    # Teardown: This runs after the test
    if os.path.exists(TEST_SAVE_PATH):
        os.remove(TEST_SAVE_PATH)


def test_backtracking_solver_basic(setup_basic_solver_and_board):
    # Tes
    board, bt_solver, known_solution_path, test_save_path = setup_basic_solver_and_board
    format_handler = SudokuFormatHandler()

    with open(known_solution_path, "r") as f:
        known_solution = f.read()

    solved_board, status = bt_solver.solve(board)
    format_handler.save(solved_board, "grid", test_save_path)

    with open(test_save_path, "r") as f:
        bt_solution = f.read()

    assert bt_solution == known_solution


def test_backtracking_solver_easiest_first(setup_easiest_first_solver_and_board):
    # Tes
    board, bt_solver, known_solution_path, test_save_path = setup_easiest_first_solver_and_board
    format_handler = SudokuFormatHandler()

    with open(known_solution_path, "r") as f:
        known_solution = f.read()

    solved_board, status = bt_solver.solve(board)
    format_handler.save(solved_board, "grid", test_save_path)

    with open(test_save_path, "r") as f:
        bt_solution = f.read()

    assert bt_solution == known_solution
