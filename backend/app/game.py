class UltimateTicTacToe:
    def __init__(self):
        # 9 small boards, each containing 9 cells.
        # None means the cell is empty.
        self.boards = [
            [None for _ in range(9)]
            for _ in range(9)
        ]

        # The winner of each small board.
        # None means the board has not been won.
        self.board_winners = [None for _ in range(9)]

        # X always starts.
        self.current_player = "X"

        # The first player can choose any small board.
        self.next_board = None

        # Overall winner.
        self.winner = None

    def make_move(self, board_index, cell_index):
        """Make a move on a small board."""

        if self.winner is not None:
            raise ValueError("The game is already over.")

        if not 0 <= board_index < 9:
            raise ValueError("Invalid board.")

        if not 0 <= cell_index < 9:
            raise ValueError("Invalid cell.")

        # Check whether the player is being forced
        # to play on a particular board.
        if (
            self.next_board is not None
            and self.board_winners[self.next_board] is None
            and any(cell is None for cell in self.boards[self.next_board])
            and board_index != self.next_board
        ):
            raise ValueError("You must play on the required board.")

        # A board that has already been won cannot be played.
        if self.board_winners[board_index] is not None:
            raise ValueError("That board has already been won.")

        # A full board cannot be played.
        if all(cell is not None for cell in self.boards[board_index]):
            raise ValueError("That board is full.")

        # The selected cell must be empty.
        if self.boards[board_index][cell_index] is not None:
            raise ValueError("That cell is already occupied.")

        # Make the move.
        self.boards[board_index][cell_index] = self.current_player

        # Check whether this move won the small board.
        small_board_winner = self.check_winner(
            self.boards[board_index]
        )

        if small_board_winner is not None:
            self.board_winners[board_index] = small_board_winner

            # Check whether winning this small board
            # also won the entire game.
            if self.check_winner(self.board_winners) is not None:
                self.winner = small_board_winner

        # The cell that was selected determines
        # the board the next player should play on.
        self.next_board = cell_index

        # If that board is already won or completely full,
        # the next player can choose another available board.
        if (
            self.board_winners[self.next_board] is not None
            or all(cell is not None for cell in self.boards[self.next_board])
        ):
            self.next_board = None

        # Change players unless the game has ended.
        if self.winner is None:
            self.current_player = (
                "O" if self.current_player == "X" else "X"
            )

    @staticmethod
    def check_winner(board):
        """Return X or O if the board has a winner."""

        winning_combinations = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]

        for a, b, c in winning_combinations:
            if (
                board[a] is not None
                and board[a] == board[b] == board[c]
            ):
                return board[a]

        return None

    def get_state(self):
        """Return the current game state."""

        return {
            "boards": self.boards,
            "board_winners": self.board_winners,
            "current_player": self.current_player,
            "next_board": self.next_board,
            "winner": self.winner,
        }
