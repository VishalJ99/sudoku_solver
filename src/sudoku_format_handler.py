import re
from exceptions import FormatError
from abc import ABC, abstractmethod
from typing import List
from sudoku_board import SudokuBoard
from utils import remove_whitespace_and_empty_lines, replace_dot_with_zero
import os


class FormatHandler(ABC):
    @abstractmethod
    def parse(self, input: str, input_type: str) -> SudokuBoard:
        pass

    @abstractmethod
    def save(self, board: SudokuBoard, file: str):
        pass

    def _preprocess(self, board_input: str, input_type: str) -> List[str]:
        # Load the input data into a common format of a list of strings
        if input_type == "filepath":
            if not os.path.exists(board_input):
                raise FileNotFoundError(f"File not found: {board_input}")

            with open(board_input, "r") as f:
                board_data = f.readlines()

        elif input_type == "string":
            board_data = board_input.splitlines()

        else:
            raise TypeError("board_input must be a string or path to a file")

        # Perform some basic preprocessing on the input data
        board_data = remove_whitespace_and_empty_lines(board_data)
        board_data = replace_dot_with_zero(board_data)
        return board_data


class GridFormatHandler(FormatHandler):
    def _validate(self, board_data):
        # validate row count
        if len(board_data) != 11:
            error_message = "[ERROR] Input string does not have 11 rows\nInput string:\n"
            for i, row in enumerate(board_data, start=1):
                error_message += f"{i}: {row}\n"
            raise FormatError(error_message)

        # validate row format
        number_row_pattern = re.compile(r"^\d{3}\|\d{3}\|\d{3}$")
        separator_row_pattern = re.compile(r"^---\+---\+---$")
        alternate_number_row_pattern = re.compile(r"^\D?\d{3}\D\d{3}\D\d{3}\D?$")

        bad_line_ids = []
        for i, line in enumerate(board_data):
            if i % 4 == 3:
                if not separator_row_pattern.match(line):
                    if not bool(re.search(r"\d", line)):
                        bad_line_ids.append(i)
                    else:
                        error_message = (
                            f"[ERROR] Separator row does not match an acceptable pattern\n"
                            f"Found:\n{line}\n"
                            f"Expected:\n---+---+---\n\n"
                            f"Please see README.md for more information."
                        )
                        raise FormatError(error_message)
            else:
                if not number_row_pattern.match(line):
                    if alternate_number_row_pattern.match(line):
                        bad_line_ids.append(i)
                    else:
                        error_message = (
                            f"[ERROR] Number row does not match an acceptable pattern\n"
                            f"Found:\n{line}\n"
                            f"Expected format:\n123|456|789\n\n"
                            f"Please see README.md for more information."
                        )
                        raise FormatError(error_message)

        return board_data, bad_line_ids

    def _correct_row_format(self, board_data, bad_line_ids):
        """
        Corrects the format of the input board for the given row indices.
        Prints a warning message to show the modifications made.

        Parameters
        ----------
            lines_to_correct (list): A list of line indices to correct.
        """

        for id_ in bad_line_ids:
            line = board_data[id_]
            if id_ % 4 == 3:  # Separator rows
                board_data[id_] = "---+---+---"
            else:
                groups = re.findall(r"\d{3}", line)
                board_data[id_] = "|".join(groups)

        warning_message = "[WARNING] Input string corrected to match expected format\n"
        print(warning_message)
        return board_data

    def parse(self, board_input: str, input_type: str) -> SudokuBoard:
        self._check_input_type_valid(board_input, input_type)
        board_data = self._preprocess(board_input, input_type)
        board_data, bad_line_ids = self._validate(board_data)
        if bad_line_ids:
            board_data = self._correct_row_format(board_data, bad_line_ids)
        board_data = self._parse_to_2d_int_list(board_data)
        return SudokuBoard(board_data)

    def _check_input_type_valid(self, board_input: str, input_type: str = "filepath"):
        if input_type == "filepath":
            # get file extension
            _, file_extension = os.path.splitext(board_input)
            if file_extension == ".txt":
                return True
            else:
                error_msg = (
                    "[ERROR] Input file does not have a .txt extension\n",
                    "Only support file input for text files, please see README.md",
                )
                raise TypeError(error_msg)

        elif isinstance(board_input, str):
            return True
        else:
            error_msg = (
                "[ERROR] Input must be a string or path to a file\n",
                "Only support file input for text files, please see README.md",
            )
            raise TypeError(error_msg)

    def save(self, board: SudokuBoard, file_path: str):
        """
        Formats the board back into the input format and saves it as a text file
        with the given filename.

        Parameters
        ----------
        filename : str
            name of the file to save the board to
        """
        # check that the file path is describes a .txt file
        _, file_extension = os.path.splitext(file_path)
        if file_extension != ".txt":
            error_message = (
                "[ERROR] Output file does not have a .txt extension\n",
                "Only support file output for text files, please see README.md",
            )
            raise TypeError(error_message)

        with open(file_path, "w") as file:
            for i in range(9):
                for j in range(9):
                    file.write(str(board[i][j]))
                    if (j + 1) % 3 == 0 and j < 8:
                        file.write("|")
                file.write("\n")
                if (i + 1) % 3 == 0 and i < 8:
                    file.write("---+---+---\n")

    def _parse_to_2d_int_list(self, board_data):
        """
        Parses the board data into a 2D list of integers.

        Returns:
            list: A 2D list representing the parsed matrix of integers.
        """
        parsed_matrix = []
        # Check each line against the appropriate pattern
        for i, line in enumerate(board_data):
            # Every fourth line is a separator row so skip it
            if i % 4 == 3:
                continue
            else:
                # extract the triple digits groupings from the row
                triplet_digit_groups = re.findall(r"\d{3}", line)

                # flatten the list of triplets into a list of digits
                row = [int(digit) for digit in "".join(triplet_digit_groups)]
                parsed_matrix.append(row)

        return parsed_matrix


class FlatFormatHandler(FormatHandler):
    def parse(self, input_data, input_type="filepath"):
        # takes an a string of 81 digits and returns a 2D list of integers
        # representing the board
        input_data = self._preprocess(input_data, input_type)
        input_data = input_data[0]
        self._check_valid_input(input_data)

        # convert the input string into a 2D list of integers
        board_data = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(int(input_data[i * 9 + j]))
            board_data.append(row)

        return SudokuBoard(board_data)

    def save(self, board: SudokuBoard, file: str):
        # takes a 2D list of integers representing the board and saves it to a file
        with open(file, "w") as f:
            for i in range(9):
                for j in range(9):
                    f.write(str(board[i][j]))

    def _check_valid_input(self, input_data):
        # check that the input is a string
        if not isinstance(input_data, str):
            raise TypeError("Input must be a string")

        # check that the input contains only digits
        if not input_data.isdigit():
            raise ValueError("Input must contain only digits")

        # check that the input is 81 characters long
        if len(input_data) != 81:
            raise ValueError("Input must be 81 characters long")


class SudokuFormatHandler:
    def _get_handler(self, format: str):
        handler_dict = {
            "grid": GridFormatHandler(),
            "flat": FlatFormatHandler(),
        }

        # Check that specified format is supported.
        if format not in handler_dict.keys():
            error_message = (
                f"[ERROR] Specified format: {format}, is not supported\n"
                f"Currently supported formats: {list(handler_dict.keys())}\n"
                "Please see README.md for more information."
            )
            raise ValueError(error_message)

        return handler_dict[format]

    def parse(self, input: str, format: str, input_type: str = "filepath"):
        handler = self._get_handler(format)
        return handler.parse(input, input_type)

    def save(self, board: SudokuBoard, format: str, file: str):
        handler = self._get_handler(format)
        handler.save(board, file)
