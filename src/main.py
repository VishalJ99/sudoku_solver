import argparse
import os
import time
from sudoku_format_handler import SudokuFormatHandler
from sudoku_solvers import SudokuSolver
import json


def solve_sudoku(file_path, solver, format_handler, format_type, file_type, timeout):
    board = format_handler.parse(file_path, format_type, file_type)
    start_time = time.time()
    solved_board, status = solver.solve(board)
    solve_time = time.time() - start_time
    return solved_board, solve_time, status


def validate_args(args):
    """
    validates the arguments passed to the program
    """
    # Input file checks.
    # -----------------
    # File must exist if input_type is filepath.
    if not os.path.exists(args.sudoku_input) and args.input_type == "filepath":
        error_msg = (
            "Input file (or dir for batch) does not exist. If you are trying to pass"
            "a string as input, please set --input_type to 'string' when calling the script."
        )

        raise FileNotFoundError(error_msg)

    # Batch mode checks.
    # -----------------
    if args.batch:
        # Input path checks.
        # -----------------
        if not os.path.isdir(args.sudoku_input):
            raise ValueError("Input path must be a valid directory in batch mode")
        elif not os.listdir(args.sudoku_input):
            raise ValueError("Input directory must not be empty in batch mode")

        # Output path checks.
        # ------------------
        if not args.output_path:
            raise ValueError("Output path is required in batch mode")
        elif os.path.exists(args.output_path) and not os.path.isdir(args.output_path):
            raise ValueError("Output path must be a directory in batch mode")
        elif os.path.exists(args.output_path) and os.listdir(args.output_path):
            raise ValueError("Output directory must be empty in batch mode")
        elif not os.path.exists(args.output_path):
            print("[INFO] Output directory does not exist... Creating output directory")
            os.makedirs(args.output_path)

        # Conflicting argument checks.
        # ----------------------------
        if args.input_type != "filepath":
            raise ValueError("input_type must be set to 'filepath' in batch mode")

    # Single mode checks.
    # ------------------
    else:
        # Input path checks.
        # -----------------
        if args.input_type == "string" and os.path.isfile(args.sudoku_input):
            raise ValueError("input_type is set to string but sudoku_input describes a file path")

        if not args.batch and os.path.isdir(args.sudoku_input):
            raise ValueError("Please run with --batch to process a directory of Sudoku files")

        # output file checks.
        # -----------------
        if args.output_path and os.path.exists(args.output_path):
            raise ValueError("Output file already exists, not overwriting...")

    # Stats file checks.
    # -----------------
    if args.stats_path:
        if os.path.exists(args.stats_path):
            raise ValueError("Stats file already exists, not overwriting...")
        if not args.stats_path.endswith(".txt") and not args.stats_path.endswith(".csv"):
            raise ValueError("Stats file path must be a .txt or .csv file")
        # If batch mode enabled, check summary file name doesnt already exist.
        if os.path.exists(args.stats_path[:-4] + "_summary.txt") and args.batch:
            raise ValueError("Summary file already exists, not overwriting...")
        if not os.path.exists(os.path.dirname(args.stats_path)):
            raise ValueError("Stats file directory does not exist")

    # Solver parameter checks.
    # -----------------------
    # Checks Timeout value is valid.
    if args.timeout <= 0:
        args.timeout = 10
        print("[WARNING] Timeout must be a positive integer, setting to default value of 10")

    return args


def get_solver_kwargs(args):
    # In the future, args will contain a path to a config file which will be parsed here to get
    # the solver kwargs.
    solver_kwargs = {"timeout": args.timeout}
    return solver_kwargs


def initialise_solver_and_format_handler(solver_method, solver_kwargs):
    format_handler = SudokuFormatHandler()
    solver = SudokuSolver()

    # Set solver backend.
    solver.set_solver(solver_method, solver_kwargs)
    return format_handler, solver


def main(args):
    args = validate_args(args)

    solver_kwargs = get_solver_kwargs(args)

    format_handler, solver = initialise_solver_and_format_handler(args.solver, solver_kwargs)

    # Initialise list tracking solve time and status.
    solve_stats = []

    # If saving statistics, fetch git commit hash and save to environment variable.
    if args.stats_path:
        os.environ["GIT_COMMIT_HASH"] = os.popen("git rev-parse HEAD").read().strip()

    # Solve sudoku(s).
    if args.batch:
        # Fetch all files in the directory, excluding hidden files.
        sudoku_files = [file for file in os.listdir(args.sudoku_input) if not file.startswith(".")]

        # Loop through all files in the directory.
        for idx, file in enumerate(sudoku_files):
            file_path = os.path.join(args.sudoku_input, file)

            solved_board, solve_time, status = solve_sudoku(
                file_path,
                solver,
                format_handler,
                args.input_format_type,
                args.input_type,
                args.timeout,
            )

            print(f"\rSolved {idx}/{len(sudoku_files)} boards", end="")

            # Save solved board.
            output_file = os.path.join(args.output_path, f"solved_{file}")
            format_handler.save(
                solved_board, args.output_format_type, output_file
            ) if solved_board else None

            # Save run statistics.
            solve_stats.append((file, solve_time, status))

        # Calculate summary statistics.
        total_boards = len(solve_stats)
        timeout_count = sum(1 for _, _, status in solve_stats if status == "Timeout")
        solve_times = [time_taken for _, time_taken, status in solve_stats if status != "Timeout"]

        # If all boards timed out, set all time related statistic values to 0.
        average_time = sum(solve_times) / len(solve_times) if solve_times else 0
        median_time = sorted(solve_times)[len(solve_times) // 2] if solve_times else 0
        min_time = min(solve_times, default=0)
        max_time = max(solve_times, default=0)
        std_deviation = (
            (sum((x - average_time) ** 2 for x in solve_times) / len(solve_times)) ** 0.5
            if solve_times
            else 0
        )

        summary_stats = (
            f"Total Boards Attempted: {total_boards}\n"
            f"Boards that hit Timeout: {timeout_count}\n"
            f"Percentage of Timeouts: {timeout_count / total_boards * 100:.7f}%\n"
            f"Average Solve Time: {average_time:.7f} seconds\n"
            f"Median Solve Time: {median_time:.7f} seconds\n"
            f"Min Solve Time: {min_time:.7f} seconds\n"
            f"Max Solve Time: {max_time:.7f} seconds\n"
            f"Standard Deviation of Solve Times: {std_deviation:.7f} seconds\n"
        )

        print("\nSummary Statistics:")
        print("-------------------")
        print(summary_stats)

        # Put summary and other important run information into a dictionary.
        output_summary_dict = {
            "git_commit_hash": os.environ["GIT_COMMIT_HASH"],
            "args": json.dumps(vars(args)),
            "total_boards": total_boards,
            "timeout_count": timeout_count,
            "percentage_timeouts": timeout_count / total_boards * 100,
            "average_solve_time": average_time,
            "median_solve_time": median_time,
            "min_solve_time": min_time,
            "max_solve_time": max_time,
            "std_deviation_solve_time": std_deviation,
        }

        # Save time statistics of each board to save_stats file.
        if args.stats_path:
            with open(args.stats_path, "w") as f:
                f.write(
                    "Board,Time (s),Status\n"
                    + "\n".join(",".join(str(x) for x in stat) for stat in solve_stats)
                )

        # Save summary statistics to summary_stats json.
        if args.stats_path:
            with open(args.stats_path[:-4] + "_summary.json", "w") as f:
                json.dump(output_summary_dict, f, indent=4)

    else:
        # Load board.
        board = format_handler.parse(args.sudoku_input, args.input_format_type, args.input_type)
        print("Input:")
        print(board)

        # Solve board.
        start_time = time.time()
        solved_board = solver.solve(board)
        solve_time = time.time() - start_time
        status = "Solved" if board else "Timeout"

        # If board was solved and output path is set, save the solved board.
        if args.output_path and board:
            format_handler.save(board, args.out_format_type, args.output_path)

        print("\nSolution:")
        print(solved_board)

        print("\nSummary Statistics:")
        print("Time taken to solve: ", solve_time)
        print("Status: ", status)

        # Save statistics to file. if save_stats is set.
        if args.stats_path:
            with open(args.stats_path, "w") as f:
                f.write(f"git_commit_hash, {os.environ['GIT_COMMIT_HASH']}\n")
                f.write(f"args, {json.dumps(vars(args))}\n")
                f.write(f"Time (s), {solve_time}\n")
                f.write(f"Status, {status}\n")


if __name__ == "__main__":
    # Get supported formats and solvers.
    supported_formats = list(SudokuFormatHandler().handler_dict.keys())
    supported_solvers = list(SudokuSolver().solver_dict.keys())

    parser = argparse.ArgumentParser(
        description="Advanced Sudoku Solver: This command-line tool offers robust functionality \
        for solving Sudoku puzzles, either individually or in batch mode. It supports diverse \
        input formats (file paths or strings) and varied Sudoku board layouts. Designed to be \
        easily extended to support new input formats and solvers."
    )

    parser.add_argument(
        "sudoku_input",
        type=str,
        help="Path to the Sudoku input file, or directory of files in batch mode. Can also accept \
                a Sudoku board string if --input_type is set to 'string'.",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Enable batch mode for processing multiple Sudoku files in a directory.",
    )
    parser.add_argument(
        "--input_type",
        type=str,
        choices=["filepath", "string"],
        default="filepath",
        help="Specifies the type of input provided: 'filepath' for file paths or 'string' for \
              direct Sudoku board strings. Defaults to 'filepath'.",
    )
    parser.add_argument(
        "--input_format_type",
        type=str,
        choices=supported_formats,
        default="grid",
        help="Format of the Sudoku board in the input. 'grid' for normal grid layout or 'flat' \
              for a single row of 81 digits. Defaults to 'grid'.",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        help="filepath to save the solved Sudoku board. For batch mode, this is a path to a \
          directory to save solved boards. Solutions filenames will be the original prepended \
            with solved_. Required in batch mode.",
    )
    parser.add_argument(
        "--output_format_type",
        type=str,
        choices=supported_formats,
        default="grid",
        help="Format of the solved Sudoku board in the output file. 'grid' for normal grid layout \
          or 'flat' for a single row of 81 digits. Defaults to 'grid'.",
    )
    parser.add_argument(
        "--stats_path",
        type=str,
        help="Path to a txt or csv file to save the statistics about the solving process,\
          if batch mode is enabled, saves statistics for all boards in the file along with a \
          summary file with the same name but ending in '_summary.txt'.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Maximum time allowed in seconds for solving a single board. Defaults to 10 seconds.\
          Must be a positive integer.",
    )

    parser.add_argument(
        "--solver",
        type=str,
        choices=supported_solvers,
        default="bt_basic",
        help="Solver to use for solving the Sudoku board. Defaults to 'backtracking'.",
    )

    args = parser.parse_args()
    main(args)
