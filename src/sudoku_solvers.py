class BacktrackingSolver:
    """
    Class for solving sudoku puzzles using a backtracking algorithm
    """

    def _backtrack(self):
        """
        Solve the sudoku puzzle using a backtracking algorithm

        Returns
        -------
        bool
            True if the puzzle was solved, False otherwise
        """
        # find the next empty square
        i, j = self.board.find_empty()

        # if there are no empty squares, the puzzle is solved
        if i is None:
            return True

        # check which numbers are valid in the empty square
        for num in range(1, 10):
            if self.board.check_valid(i, j, num):
                # make the move and repeat recursively
                self.board.place_number(i, j, num)
                if self._backtrack():
                    # puzzle was solved
                    return True

                # if the puzzle was not solved, undo the move
                self.board.remove_number(i, j, num)

        # if no numbers worked, an incorrect move was made somewhere
        # return False to backtrack
        return False

    def solve(self, board):
        """
        Solve the sudoku puzzle

        Returns
        -------
        bool
            True if the puzzle was solved, False otherwise
        """
        self.board = board
        self._backtrack()
        return self.board
