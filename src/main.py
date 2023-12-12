import argparse
import os
import time
from sudoku_format_handler import SudokuFormatHandler
from sudoku_solvers import BacktrackingSolver


def solve_sudoku(file_path, solver, format_handler, format_type, timeout, verbose=False):
    board = format_handler.parse(file_path, format_type, "filepath")
    start_time = time.time()
    if verbose:
        print("Solving board:")
        print(board)
    solved_board = solver.solve(board, timeout)  # Assuming solve() can handle timeout
    solve_time = time.time() - start_time
    if verbose:
        print("Solved board:")
        print(solved_board if solved_board else "Ran out of time")
    return solved_board, solve_time


def main():
    parser = argparse.ArgumentParser(description="Sudoku Solver")
    parser.add_argument(
        "sudoku_input", type=str, help="Path to the Sudoku input file or directory for batch mode"
    )
    parser.add_argument(
        "--batch_mode", action="store_true", help="Enable batch mode for processing multiple files"
    )
    parser.add_argument("--file_type", type=str, help="Type of the input file", default="filepath")
    parser.add_argument(
        "--format_type", type=str, help="Format of the Sudoku input", default="grid"
    )
    parser.add_argument(
        "--output_path", type=str, help="Path to the output file or directory for batch mode"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="Maximum time allowed for solving a puzzle (in seconds)",
        default=10,
    )

    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose mode for printing the board"
    )

    args = parser.parse_args()

    format_handler = SudokuFormatHandler()
    solver = BacktrackingSolver()
    benchmark_results = []

    if args.batch_mode:
        # if output directory does not exist, create it
        if not os.path.exists(args.output_path):
            os.makedirs(args.output_path)

        # Loop through all files in the directory
        for file in os.listdir(args.sudoku_input):
            file_path = os.path.join(args.sudoku_input, file)
            solved_board, solve_time = solve_sudoku(
                file_path,
                solver,
                format_handler,
                args.format_type,
                args.timeout,
                verbose=args.verbose,
            )
            status = "Solved" if solved_board else "Timeout"
            output_file = os.path.join(args.output_path, f"solved_{file}")
            format_handler.save(
                solved_board, args.format_type, output_file
            ) if solved_board else None
            benchmark_results.append((file, solve_time, status))

        # Save benchmark report
        benchmark_report_path = os.path.join(args.output_path, "benchmark_report.txt")
        with open(benchmark_report_path, "w") as f:
            for file, time_taken, status in benchmark_results:
                f.write(f"{file},{time_taken},{status}\n")

        # Print summary statistics
        total_boards = len(benchmark_results)
        timeout_count = sum(1 for _, _, status in benchmark_results if status == "Timeout")
        solve_times = [
            time_taken for _, time_taken, status in benchmark_results if status != "Timeout"
        ]

        average_time = sum(solve_times) / len(solve_times) if solve_times else 0
        median_time = sorted(solve_times)[len(solve_times) // 2] if solve_times else 0
        min_time = min(solve_times, default=0)
        max_time = max(solve_times, default=0)
        std_deviation = (
            (sum((x - average_time) ** 2 for x in solve_times) / len(solve_times)) ** 0.5
            if solve_times
            else 0
        )

        print("\nSummary Statistics:")
        print(f"Total Boards Attempted: {total_boards}")
        print(f"Boards that hit Timeout: {timeout_count}")
        print(f"Percentage of Timeouts: {timeout_count / total_boards * 100:.5f}%")
        print(f"Average Solve Time: {average_time:.5f} seconds")
        print(f"Median Solve Time: {median_time:.5f} seconds")
        print(f"Min Solve Time: {min_time:.5f} seconds")
        print(f"Max Solve Time: {max_time:.5f} seconds")
        print(f"Standard Deviation of Solve Times: {std_deviation:.2f} seconds")

    else:
        board, solve_time = solve_sudoku(
            args.sudoku_input,
            solver,
            format_handler,
            args.format_type,
            args.timeout,
            verbose=args.verbose,
        )
        if args.output_path and board:
            format_handler.save(board, args.format_type, args.output_path)


if __name__ == "__main__":
    main()
