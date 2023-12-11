from icecream import ic


def compare(old_lines, new_lines, msg):
    """
    Compare two lists of strings and print the differences
    """

    # TODO: replace with an actual method
    print(msg)
    ic(old_lines)
    ic(new_lines)


def remove_whitespace_and_empty_lines(board_data):
    """
    Cleans up the board data by removing any whitespace and empty lines.

    Iterates through each row in the `_board_data` attribute,
    removes all whitespace from each row, and excludes any rows
    that are empty after this removal. If any changes are made,
    the cleaned data is stored back into the `_board_data` attribute
    and a warning is generated.
    """
    processed_board_data = []
    for row in board_data:
        # Remove white spaces from row.
        row_ = "".join(row.split())

        # Skip empty rows.
        if not row_:
            continue

        processed_board_data.append(row_)

    return processed_board_data


def replace_dot_with_zero(board_data):
    """
    Replaces all dots in the board data with zeros.
    Some sudoku boards found on the internet will have dots
    instead of zeros, so this method will replace all dots
    in `board_data` with zeros.
    """
    processed_board_data = []
    for row in board_data:
        # Replace dots with zeros.
        row_ = row.replace(".", "0")
        processed_board_data.append(row_)

    return processed_board_data
