import re


def validate_sudoku_input(input_string, verbose=False):
    """
    TODO:
    - Merge white space and new line removal into one loop
    - Improve print statements to format sudoku board properly when showing corrections
    - Reject obviously incorrect boards (e.g. 2 numbers in same row)
    - Warning messages should display row number (e.g. [WARNING] White space found in row 1)

    Validates a list of strings describing rows of a sudoku board.
    Uses regex pattern matching to check input against format in README.md.

    Will correct for:
        - Whitespace in the input string
        - Empty lines in the input string
        - Incorrect separator rows (raises error if digits in row)
        - Incorrect delimiters in num rows (raises error if num digits between delimiters != 3)

    Logic used for seperator row correction involves first checking if the row contains any digits.
    If it does not, seperator row is assumed to be valid and is reformatted to the correct pattern.
    If it does, ValueError is raised.

    Logic used for number row correction involves first checking if the row matches an alternate
    valid pattern. Alternate valid patterns are rows that match against the following regex:
    r"^\\D?\\d{3}\\D\\d{3}\\D\\d{3}\\D?$"  (note that backslashes are escaped).
    i.e rows that contain triplets of integers separated by any non-digit character.
    If the row matches an alternate valid pattern, the triplets are extracted and joined with |.
    If it does not, ValueError is raised.

    Parameters
    ----------
    input_string : list
        List of strings, where each string element represents a row of the sudoku board txt file.
        A typical argument for this param would be the output of f.readlines() on the board file.
    verbose : bool, optional
        If True, prints warning messages when correcting input string, by default False.

    Returns
    -------
    bool
        Returns True if the input string is a valid Sudoku board representation.
        Else raises ValueError if the input contains irrecoverable formatting issues.

    Raises
    ------
    ValueError
        If the number of rows after basic cleaning is not equal to 11,
        or if any row does not match the expected pattern, and cannot be corrected.


    Examples
    --------
    >>> with open("test/test_boards/good_input.txt", "r") as f:
    ...     good_input = f.readlines()
    >>> validate_sudoku_input(good_input)
    True

    >>> with open("test/test_boards/bad_input_1.txt", "r") as f:
    ...     bad_input_1 = f.readlines()
    >>> validate_sudoku_input(bad_input_1)
    Traceback (most recent call last):

    ValueError: [ERROR] Number row does not match expected pattern
    Found:
    000|600|00
    Expected format:
    123|456|789

    >>> with open("test/test_boards/correctable_input.txt", "r") as f:
    ...     correctable_input = f.readlines()
    >>> validate_sudoku_input(correctable_input)
    True
    """
    # define a regex pattern for the desired numerical row
    number_row_pattern = re.compile(r"^\d{3}\|\d{3}\|\d{3}$")

    # define a regex pattern an alternate general numerical row
    alt_number_row_pattern = re.compile(r"^\D?\d{3}\D\d{3}\D\d{3}\D?$")

    # define a regex pattern for the desired separator row
    separator_row_pattern = re.compile(r"^---\+---\+---$")

    white_space_found = False
    empty_line_found = False

    # remove any white spaces
    for idx, row in enumerate(input_string):
        if bool(re.search(r"\s", row.rstrip())):
            input_string[idx] = "".join(row.split())
            white_space_found = True

    if white_space_found and verbose:
        warning_message = (
            f"[WARNING] White space found in input string\n"
            f"Found:\n{input_string}\n"
            f"Replacing with:\n{input_string}\n"
        )
        print(warning_message)

    # remove any empty lines
    for idx, row in enumerate(input_string):
        if not row.rstrip():
            input_string.pop(idx)
            empty_line_found = True

    if empty_line_found and verbose:
        warning_message = (
            f"[WARNING] Empty lines found in input string\n"
            f"Found:\n{input_string}\n"
            f"Removing empty lines\n"
            f"Result:\n{input_string}\n"
        )
        print(warning_message)

    # Check if there are 11 lines (9 rows of numbers and 2 separators)
    if len(input_string) != 11:
        error_message = "[ERROR] Input string does not have 11 rows\nInput string:\n"
        for i, row in enumerate(input_string, start=1):
            error_message += f"{i}: {row}\n"
        raise ValueError(error_message)

    # Check each line against the appropriate pattern
    for i, line in enumerate(input_string):
        # Every fourth line should match separator pattern
        if i % 4 == 3:
            if not separator_row_pattern.match(line):
                # check separator row does not contain any digits
                if not bool(re.search(r"\d", line)):
                    # replace the incorrect separator with the correct one
                    input_string[i] = "---+---+---"
                    if verbose:
                        warning_message = (
                            f"[WARNING] Separator row does not match expected pattern\n"
                            f"Found:\n{line}\n"
                            f"Replacing with:\n{input_string[i]}\n"
                        )
                        print(warning_message)
                else:
                    error_message = (
                        f"[ERROR] Separator row does not match expected pattern\n"
                        f"Found:\n{line}\n"
                        f"Expected:\n---+---+---\n\n"
                        f"Please see README.md for more information."
                    )
                    raise ValueError(error_message)
        else:
            # Other lines should match the number row pattern
            if not number_row_pattern.match(line):
                # check if row matches an alternate valid pattern
                if alt_number_row_pattern.match(line):
                    # extract the triple digits groupings rom the row
                    groups = re.findall(r"\d{3}", line)

                    # join the groups with the correct delimiter
                    input_string[i] = "|".join(groups)
                    if verbose:
                        warning_message = (
                            f"[WARNING] Number row does not match expected pattern\n"
                            f"Found:\n{line}\n"
                            f"Replacing with:\n{input_string[i]}\n"
                        )
                        print(warning_message)
                else:
                    error_message = (
                        f"[ERROR] Number row does not match expected pattern\n"
                        f"Found:\n{line}\n"
                        f"Expected format:\n123|456|789\n\n"
                        f"Please see README.md for more information."
                    )
                    raise ValueError(error_message)

    # If all checks pass
    return True


def parse_input(lines):
    pass