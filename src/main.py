import argparse
from sudoku_format_handler import SudokuFormatHandler
from sudoku_solvers import BacktrackingSolver


def main():
    parser = argparse.ArgumentParser(description="Sudoku Input Parser")
    parser.add_argument("sudoku_input", type=str, help="Path to the Sudoku input file")
    parser.add_argument("--file_type", type=str, help="Type of the input file", default="filepath")
    parser.add_argument(
        "--format_type", type=str, help="Format of the Sudoku input", default="grid"
    )
    parser.add_argument("--output_path", type=str, help="Path to the output file")

    args = parser.parse_args()

    format_handler = SudokuFormatHandler()
    board = format_handler.parse(args.sudoku_input, args.format_type, args.file_type)
    print("Input Board:")
    print(board)
    solver = BacktrackingSolver()
    solved_board = solver.solve(board)
    print("Solved Board:")
    print(solved_board)
    if args.output_path:
        format_handler.save(solved_board, args.format_type, args.output_path)


if __name__ == "__main__":
    main()
