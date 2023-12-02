import re


def validate_sudoku_input(input_string):
    """
    Validates an input string for a sudoku board using regex pattern matching,
    ensuring it matches format specified in README.md.

    Will correct for:
        - Whitespace in the input string
        - Empty lines in the input string
        - Incorrect separator rows (raises error if digits in row)
        - Incorrect delimiters in num rows (raises error if num digits between delimiters != 3)

    Parameters
    ----------
    input_string : list
        list of strings, each string representing a row of the sudoku board txt file

    Returns
    -------
    bool : True if input string is valid, False otherwise
    """
    # Define a regex pattern for the desired numerical row
    number_row_pattern = re.compile(r"^\d{3}\|\d{3}\|\d{3}$")

    # Define a regex pattern an alternate general numerical row
    alt_number_row_pattern = re.compile(r"^\D?\d{3}\D\d{3}\D\d{3}\D?$")

    # Define a regex pattern for the desired separator row
    separator_row_pattern = re.compile(r"^---\+---\+---$")

    for row in input_string:
        if bool(re.search(r"\s", row.rstrip())):
            # Remove all white spaces from the input
            print("[WARNING] Input string contains whitespace. Removing whitespace...")
            input_string = "".join(row.split())
            print(f"[INFO] Input string after removing whitespace:\n{input_string}")

            # Check if empty string
            if not input_string:
                print("[INFO] Removing empty row...")
                # remove row from input string
                input_string.remove(row)

    # Check if there are 11 lines (9 rows of numbers and 2 separators)
    if len(input_string) != 11:
        raise ValueError("[ERROR] Input string does not have 11 rows")
        return False

    # Check each line against the appropriate pattern
    for i, line in enumerate(input_string):
        # Every fourth line should match separator pattern
        if i % 4 == 3:
            if not separator_row_pattern.match(line):
                # check separator row does not contain any digits
                if not bool(re.search(r"\d", line)):
                    # replace the incorrect separator with the correct one
                    input_string[i] = "---+---+---"
                    print(
                        f"""[WARNING] Separator row does not match expected pattern,
                            Found:\n{line}\nReplacing with:\n{input_string[i]}"""
                    )
                else:
                    raise ValueError(
                        f"""[ERROR] Separator row does not match expected pattern,
                                        Found:\n{line}\nExpected:\n---+---+---\n
                                        Please see README.md for more information."""
                    )
        else:
            # Other lines should match the number row pattern
            if not number_row_pattern.match(line):
                # check if row matches a generally acceptable pattern
                if alt_number_row_pattern.match(line):
                    # extract the triple digits groupings rom the row
                    groups = re.findall(r"\d{3}", line)

                    # join the groups with the correct delimiter
                    input_string[i] = "|".join(groups)

                    print(
                        f"""[WARNING] Number row does not match expected pattern, Found:\n{line}'
                            f'\nReplacing with:\n{input_string[i]}"""
                    )
                else:
                    raise ValueError(
                        f"""[ERROR] Number row does not match expected pattern,
                                        Found:\n{line}\nExpected:\n123|456|789\n
                                        Please see README.md for more information."""
                    )
    # If all checks pass
    return True


def parse_input(lines):
    pass


# with open('test/test_boards/good_input.txt', 'r') as f:
#     input_string = f.readlines()
#     if validate_sudoku_input(input_string):
#         print('Input string is valid')

# for row in input_string:
#     print(row.rstrip())
#     print(bool(re.search(r'\s', row.rstrip())))
