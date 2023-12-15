import re
from exceptions import FormatError
from abc import ABC, abstractmethod
from typing import List
from sudoku_board import SudokuBoard
import os

# TODO: think about how corrections are shown to the user
# Think about replacing dots with zeros not being logged as a correction


class FormatHandler(ABC):
    """
    An abstract base class for handling different formats of Sudoku boards.

    A FormatHandler is responsible for parsing and saving Sudoku boards from a specific
    format. It must implement the parse and save methods.

    Common preprocessing steps are implemented in this class and are expected to be called
    by subclasses in their parse method. These steps are expected to be common to all formats.
    """

    @abstractmethod
    def parse(self, input: str, input_type: str) -> SudokuBoard:
        """
        Parses the input into a SudokuBoard object.

        This method must be implemented by subclasses. The method should handle
        errors in input format gracefully, throwing relevant exceptions.

        Parameters
        ----------
        input : str
            The string representation of the Sudoku board or a file path containing the board.
        input_type : str
            The type of the input: 'filepath' for file paths and 'string' for direct string inputs.

        Returns
        -------
        SudokuBoard
            The parsed Sudoku board.

        Examples
        --------
        >>> handler.parse("path/to/board.txt", "filepath")
        SudokuBoard(...)
        >>> handler.parse("4...3....", "string")
        SudokuBoard(...)
        """
        pass

    @abstractmethod
    def save(self, board: SudokuBoard, file_path: str) -> None:
        """
        Saves a SudokuBoard object to a file.

        This method must be implemented by subclasses and should handle file-related errors.

        Parameters
        ----------
        board : SudokuBoard
            The Sudoku board to be saved.
        file_path : str
            The file path where the board is to be saved.

        Returns
        -------
        None

        Examples
        --------
        >>> handler.save(board, "path/to/save.txt")

        """
        pass

    def _preprocess(self, board_input: str, input_type: str) -> List[str]:
        """
        Performs common preprocessing steps on the input data to prepare it for parsing.
        The methods called here are expected to be common to all formats.
        This method is expected to be the first called in the parse method of any FormatHandler
        subclass. As this method takes the input of the parse method, the input file path or
        string input and returns a list of strings representing the board data which can then be
        further validated and corrected before being parsed into a SudokuBoard object.

        Parameters
        ----------
        board_input : str
            The input string or file path for the Sudoku board.
        input_type : str
            The type of input ('filepath' or 'string').

        Returns
        -------
        List[str]
            Preprocessed board data as a list of strings.
        """
        # Add any common preprocessing steps here
        board_data = self._load_data(board_input, input_type)
        board_data = self._remove_whitespace_and_empty_lines(board_data)
        board_data = self._replace_dots_with_zeros(board_data)
        return board_data

    def _load_data(self, board_input: str, input_type: str) -> List[str]:
        """
        Loads the input data into a common format of a list of strings, based on the input type.

        If the input type is 'filepath', the method reads the file at the given path and returns
        its contents as a list of strings. If the input type is 'string', it splits the input
        string into lines and returns the list of these lines.

        Parameters
        ----------
        board_input : str
            The input string or file path for the Sudoku board. If it's a file path,
            the file should be readable and in a format that can be split into lines.
        input_type : str
            The type of input: 'filepath' for a file path, and 'string' for a direct string
            representation of the Sudoku board.

        Returns
        -------
        List[str]
            Loaded data as a list of strings, representing the Sudoku board.

        Raises
        ------
        FileNotFoundError
            If the specified file is not found when input_type is 'filepath'.
        TypeError
            If the input_type is neither 'filepath' nor 'string'.

        Examples
        --------
        >>> self._load_data("path/to/board.txt", "filepath")
        ["530070000", "600195000", ...]  # Example output for a file
        >>> self._load_data("530070000\n600195000", "string")
        ["530070000", "600195000"]  # Example output for a string
        """
        if input_type == "filepath":
            if not os.path.exists(board_input):
                raise FileNotFoundError(f"File not found: {board_input}")
            with open(board_input, "r") as f:
                return f.readlines()

        elif input_type == "string":
            return board_input.splitlines()

        else:
            raise TypeError("Input type must be either 'filepath' or 'string'.")

    def _remove_whitespace_and_empty_lines(self, board_data: List[str]) -> List[str]:
        """
        Cleans up the board data by removing whitespace and empty lines.

        Parameters
        ----------
        board_data : List[str]
            The list of strings representing the board data.

        Returns
        -------
        List[str]
            The cleaned list of strings.
        """
        processed_board_data = []
        for row in board_data:
            row_ = "".join(row.split())
            if not row_:
                continue
            processed_board_data.append(row_)

        return processed_board_data

    def _replace_dots_with_zeros(self, board_data: List[str]) -> List[str]:
        """
        Replaces all dots in the board data with zeros.

        Parameters
        ----------
        board_data : List[str]
            The list of strings representing the board data.

        Returns
        -------
        List[str]
            The list of strings with dots replaced by zeros.
        """
        return [row.replace(".", "0") for row in board_data]


class GridFormatHandler(FormatHandler):
    def _validate_rows(self, board_data):
        # TODO: collect all errors and raise them at once
        # TODO: Find a way to decouple error throwing from validation
        # validate row count
        if len(board_data) != 11:
            error_message = f"Expected input board to have 11 rows, it has {len(board_data)}\n"
            if len(board_data) > 81:
                error_message += (
                    "Input board is very long, may contain multiple puzzles\n"
                    "this is not supported, please ensure only 1 board per input file"
                )
                raise FormatError(error_message)
            elif len(board_data) == 1:
                error_message += (
                    "Input board is one line, if you meant to run with the flat format handler\n"
                    "please specify --input_format_type flat when running the program"
                )
                raise FormatError(error_message)
            else:
                error_message += "Input Board:\n"
                for i, row in enumerate(board_data, start=1):
                    # add some padding to the line number to make it easier to read
                    padding = " " * (3 - len(str(i)))
                    error_message += f"{i}:{padding}{row}\n"
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

    def _correct_rows(self, board_data, bad_line_ids):
        """
        Corrects the format of the input board for the given row indices.
        Prints a warning message to show the modifications made.
        Expects _validate to have been called first, so that the bad_line_ids
        are known to be correctable.
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
        board_data, bad_line_ids = self._validate_rows(board_data)
        if bad_line_ids:
            board_data = self._correct_rows(board_data, bad_line_ids)
        board_array = self._parse_to_2d_int_list(board_data)
        return SudokuBoard(board_array)

    def _check_input_type_valid(self, board_input: str, input_type: str = "filepath"):
        if input_type == "filepath":
            # get file extension
            _, file_extension = os.path.splitext(board_input)
            if file_extension == ".txt":
                return True
            else:
                error_msg = (
                    "[ERROR] Input file does not have a .txt extension. "
                    "Only support file input for text files. Please see README.md"
                    "for more information."
                )

                raise ValueError(error_msg)

        elif isinstance(board_input, str):
            return True
        else:
            error_msg = (
                "[ERROR] Input must be a string or path to a file. "
                "Only support file input for text files, please see README.md"
            )

            raise ValueError(error_msg)

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
                "[ERROR] Output file does not have a .txt extension\n"
                "Only support file output for text files, please see README.md"
            )

            raise ValueError(error_message)

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
    def parse(self, input_data, input_type="filepath") -> SudokuBoard:
        """
        Parses a flat format Sudoku board string into a SudokuBoard object.

        Parameters
        ----------
        input_data : str
            The Sudoku board input string or file path.
        input_type : str
            The type of input, either 'filepath' or 'string'.

        Returns
        -------
        SudokuBoard
            An instance of SudokuBoard parsed from the input.

        Raises
        ------
        ValueError
            If the input data is not valid.
        """
        input_data = self._preprocess(input_data, input_type)[0]
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


class SudokuFormatHandler(FormatHandler):
    """
    Handles the parsing and saving of Sudoku boards in different formats.


    Attributes
    ----------
    handler_dict : dict
        A dictionary mapping format types to their respective handlers.
    """

    def __init__(self):
        """
        Initialises the SudokuFormatHandler with available format handlers.
        """
        # If a new format is added, add it to this dictionary
        # Will automatically be available via the --input(/output)_format_type flag in main.py.
        self.handler_dict = {
            "grid": GridFormatHandler(),
            "flat": FlatFormatHandler(),
        }

    def _get_handler(self, format: str):
        """
        Retrieves the handler for the specified format.

        Parameters
        ----------
        format : str
            The format type for which the handler is to be retrieved.

        Returns
        -------
        handler
            An instance of the handler corresponding to the specified format.

        Raises
        ------
        KeyError
            If the format type is unsupported.
        """
        try:
            handler = self.handler_dict[format]
            return handler
        except KeyError:
            raise KeyError(
                f"Unsupported format type: {format}, options are: {list(self.handler_dict.keys())}"
            )

    def parse(self, input: str, format: str = "grid", input_type: str = "filepath") -> SudokuBoard:
        """
        Parses a Sudoku board input into a SudokuBoard object.

        Parameters
        ----------
        input : str
            The Sudoku board input.
        format : str
            The format of the Sudoku board input.
        input_type : str, optional
            The type of input (e.g., 'filepath' or 'string'). Defaults to 'filepath'.

        Returns
        -------
        SudokuBoard
            An instance of SudokuBoard parsed from the input.
        """
        parse_handler = self._get_handler(format)
        return parse_handler.parse(input, input_type)

    def save(self, board: SudokuBoard, format: str, file: str):
        """
        Saves a SudokuBoard object to a file in the specified format.

        Parameters
        ----------
        board : SudokuBoard
            The SudokuBoard to be saved.
        format : str
            The format in which to save the board.
        file : str
            The file path where the board is to be saved.
        """
        save_handler = self._get_handler(format)
        save_handler.save(board, file)
