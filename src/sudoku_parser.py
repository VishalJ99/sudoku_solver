import re
from exceptions import FormatError
import copy
from sudoku_board import SudokuBoard
from utils import compare


class SudokuParser:
    """
    A class for parsing Sudoku puzzles from text files.

    This parser reads a Sudoku puzzle from a text file and processes it into
    a SudokuBoard object.

    The parser handles the reading, validation and correction of basic format
    errors in the input file. For more information on the expected input format
    and the  types of format errors that can be corrected, please see README.md.

    Parameters
    ----------
    file_path : str
        Path to the text file containing the Sudoku board.

    Attributes
    ----------
    _board_data : list of str
        List containing each line of the Sudoku board as read from the file.

    Methods
    -------
    parse()
        Parses the Sudoku board file into a SudokuBoard object.

    Raises
    ------
    FileNotFoundError
        If the file specified by `file_path` does not exist.
    FormatError
        If the input file is not in a text file format.

    Examples
    --------
    >>> parser = SudokuParser("test/test_validation_boards/good_input.txt")
    >>> sudoku_board = parser.parse()
    >>> print(sudoku_board)
    . . . | . . 7 | . . .
    . . . | . . 9 | 5 . 4
    . . . | . 5 . | 1 6 9
    ------+-------+------
    . 8 . | . . . | 3 . 5
    . 7 5 | . . . | 2 9 .
    4 . 6 | . . . | . 8 .
    ------+-------+------
    7 6 2 | . 8 . | . . .
    1 . 3 | 9 . . | . . .
    . . . | 6 . . | . . .
    """

    def __init__(self, file_path):
        """
        Constructs a SudokuParser object with the given file path.

        Parameters
        ----------
        file_path : str
            Path to the text file containing the Sudoku puzzle.
        """
        self.file_path = file_path
        self._board_data = self._read_file()

    def parse(self):
        """
        Parses a text file describing a sudoku board into a SudokuBoard object.

        Processes and validates the input data by removing white space and empty
        lines, validating the row count and format of each row.

        If the input data is not in the expected format, attempts to correct the
        format errors.

        If any unsupported format errors are found, raises a FormatError.
        For the types of format errors that can be corrected, please see README.md.

        If any modifications are made to the input data, prints a warning message.

        Returns
        -------
        SudokuBoard
            An object representing the parsed Sudoku puzzle.

        Raises
        ------
        FormatError
            If the board format is invalid or cannot be corrected.
        """

        self._remove_whitespace_and_empty_lines()
        self._validate_row_count()
        invlid_line_ids = self._validate_row_format()

        if invlid_line_ids:
            self._correct_row_format(invlid_line_ids)

        self._board = self._parse_to_2d_int_list()
        return SudokuBoard(self._board)

    def _read_file(self):
        """
        Reads the Sudoku puzzle from the specified file.

        Checks if the file specified in `file_path` exists and
        is a text file. If valid, it reads the file and returns its contents as a list
        of strings, where each string represents a line in the file.

        Returns
        -------
        list of str
            A list containing each line from the Sudoku puzzle file.

        Raises
        ------
        FormatError
            If the file is not a text file (does not have a '.txt' extension).
        FileNotFoundError
            If the file cannot be found at the specified `file_path`.
        """
        # Check if the file format is text; raise an error if not.
        if not self.file_path.endswith(".txt"):
            error_message = (
                f"Input file is not a text file: {self.file_path}"
                "Please check the file extension and try again."
            )
            raise FormatError(error_message)

        # Attempt to open the file; raise an error if the file does not exist.
        try:
            with open(self.file_path, "r") as f:
                return f.readlines()
        except FileNotFoundError:
            error_message = (
                f"[ERROR] File not found: {self.file_path} "
                "Please check the file path and try again."
            )
            raise FileNotFoundError(error_message)

    def _remove_whitespace_and_empty_lines(self):
        """
        Cleans up the board data by removing any whitespace and empty lines.

        Iterates through each row in the `_board_data` attribute,
        removes all whitespace from each row, and excludes any rows
        that are empty after this removal. If any changes are made,
        the cleaned data is stored back into the `_board_data` attribute
        and a warning is generated.
        """
        pre_processed_board_data = []
        for row in self._board_data:
            # Remove white spaces from row.
            row_ = "".join(row.split())

            # Skip empty rows.
            if not row_:
                continue

            pre_processed_board_data.append(row_)

        if pre_processed_board_data != self._board_data:
            warning_message = "[WARNING] White space or empty line found in input string\n"
            compare(self._board_data, pre_processed_board_data, warning_message)
            self._board_data = pre_processed_board_data

    def _validate_row_count(self):
        """
        Validates the number of rows in the Sudoku board data.

        Checks if the `_board_data` attribute has exactly 11 lines.
        This count includes 9 rows for the Sudoku numbers and 2 separator rows.

        Raises
        ------
        FormatError
            If the number of lines in `_board_data` is not equal to 11. The error message
            includes the actual content of `_board_data` for reference.
        """
        if len(self._board_data) != 11:
            error_message = "[ERROR] Input string does not have 11 rows\nInput string:\n"
            for i, row in enumerate(self._board_data, start=1):
                error_message += f"{i}: {row}\n"
            raise FormatError(error_message)

    def _validate_row_format(self):
        """
        Validates the format of each row in the Sudoku puzzle.

        Checks if each row matches the expected format. If a row does not match the format or an
        alternate valid format, it raises an error. If a row matches an alternate valid format, it
        adds the index of the row to a list of lines to correct.

        Returns:
            list: A list of indices of the rows that need to be corrected.

        Raises:
            FormatError: If a row does not match an acceptable pattern
        """
        number_row_pattern = re.compile(r"^\d{3}\|\d{3}\|\d{3}$")
        separator_row_pattern = re.compile(r"^---\+---\+---$")
        alternate_number_row_pattern = re.compile(r"^\D?\d{3}\D\d{3}\D\d{3}\D?$")

        lines_to_correct = []
        for i, line in enumerate(self._board_data):
            if i % 4 == 3:  # Separator rows
                if not separator_row_pattern.match(line):
                    if not bool(re.search(r"\d", line)):
                        lines_to_correct.append(i)
                    else:
                        error_message = (
                            f"[ERROR] Separator row does not match an acceptable pattern\n"
                            f"Found:\n{line}\n"
                            f"Expected:\n---+---+---\n\n"
                            f"Please see README.md for more information."
                        )
                        raise FormatError(error_message)
            else:  # Number rows
                if not number_row_pattern.match(line):
                    if alternate_number_row_pattern.match(line):
                        lines_to_correct.append(i)
                    else:
                        error_message = (
                            f"[ERROR] Number row does not match an acceptable pattern\n"
                            f"Found:\n{line}\n"
                            f"Expected format:\n123|456|789\n\n"
                            f"Please see README.md for more information."
                        )
                        raise FormatError(error_message)

        return lines_to_correct

    def _correct_row_format(self, lines_to_correct):
        """
        Corrects the format of the input board for the given row indices.
        Prints a warning message to show the modifications made.

        Parameters
        ----------
            lines_to_correct (list): A list of line indices to correct.
        """
        pre_corrected_board_data = copy.deepcopy(self._board_data)

        for line_idx in lines_to_correct:
            line = self._board_data[line_idx]
            if line_idx % 4 == 3:  # Separator rows
                self._board_data[line_idx] = "---+---+---"
            else:
                groups = re.findall(r"\d{3}", line)
                self._board_data[line_idx] = "|".join(groups)

        warning_message = "[WARNING] Input string corrected to match expected format\n"
        compare(pre_corrected_board_data, self._board_data, warning_message)

    def _parse_to_2d_int_list(self):
        """
        Parses the board data into a 2D list of integers.

        Returns:
            list: A 2D list representing the parsed matrix of integers.
        """
        parsed_matrix = []
        # Check each line against the appropriate pattern
        for i, line in enumerate(self._board_data):
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
