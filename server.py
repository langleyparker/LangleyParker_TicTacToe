from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

HOST = "localhost"
PORT = 8000

# 9 small boards, each with 9 cells
boards = [[""] * 9 for _ in range(9)]

# The big board records who won each small board
big_board = [""] * 9

current_player = "X"

# Which small board the next player must use
next_board = None

game_over = False
winner = None


def check_winner(board):
    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in winning_combinations:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if all(board):
        return "T"

    return None


def available_boards():
    return [
        i for i in range(9)
        if big_board[i] == "" and "" in boards[i]
    ]


def reset_game():
    global boards, big_board, current_player
    global next_board, game_over, winner

    boards = [[""] * 9 for _ in range(9)]
    big_board = [""] * 9
    current_player = "X"
    next_board = None
    game_over = False
    winner = None


def make_move(board_index, cell_index):
    global current_player, next_board
    global game_over, winner

    if game_over:
        return

    # Make sure the board and cell are valid
    if board_index not in range(9):
        return

    if cell_index not in range(9):
        return

    # The player must play in the required board
    if next_board is not None and board_index != next_board:
        return

    # Cannot play in a completed board
    if big_board[board_index] != "":
        return

    # Cannot play in an occupied cell
    if boards[board_index][cell_index] != "":
        return

    # Make the move
    boards[board_index][cell_index] = current_player

    # Check whether the small board was won
    result = check_winner(boards[board_index])

    if result == "X" or result == "O":
        big_board[board_index] = result

    elif result == "T":
        big_board[board_index] = "T"

    # Check whether the entire game was won
    overall_result = check_winner(big_board)

    if overall_result == "X" or overall_result == "O":
        winner = overall_result
        game_over = True
        return

    if overall_result == "T":
        winner = "T"
        game_over = True
        return

    # The cell chosen determines the next board
    target_board = cell_index

    # If that board is available, the opponent must play there
    if target_board in available_boards():
        next_board = target_board
    else:
        # If it is unavailable, the opponent can choose any board
        next_board = None

    # Switch players
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"


def create_page():
    if game_over:
        if winner == "T":
            status = "It's a tie!"
        else:
            status = f"Player {winner} wins!"
    else:
        status = f"Player {current_player}'s turn"

    if game_over:
        instructions = "Game over! Click New Game to play again."

    elif next_board is None:
        instructions = "Choose any available board."

    else:
        instructions = f"You must play on Board {next_board + 1}."

    board_html = ""

    for board_index in range(9):

        if next_board == board_index and not game_over:
            board_class = "small-board forced"
        else:
            board_class = "small-board"

        # Show X or O if this small board has been won
        if big_board[board_index] == "X":
            board_html += f"""
            <div class="{board_class}">
                <div class="board-title">Board {board_index + 1}</div>
                <div class="winner">X</div>
            </div>
            """
            continue

        if big_board[board_index] == "O":
            board_html += f"""
            <div class="{board_class}">
                <div class="board-title">Board {board_index + 1}</div>
                <div class="winner">O</div>
            </div>
            """
            continue

        if big_board[board_index] == "T":
            board_html += f"""
            <div class="{board_class}">
                <div class="board-title">Board {board_index + 1}</div>
                <div class="winner tie">Tie</div>
            </div>
            """
            continue

        cells_html = ""

        for cell_index in range(9):

            value = boards[board_index][cell_index]

            disabled = False

            if game_over:
                disabled = True

            if value != "":
                disabled = True

            if next_board is not None:
                if board_index != next_board:
                    disabled = True

            if disabled:
                cells_html += f"""
                <button class="cell" disabled>
                    {value}
                </button>
                """
            else:
                cells_html += f"""
                <button
                    class="cell"
                    name="move"
                    value="{board_index},{cell_index}">
                    {value}
                </button>
                """

        board_html += f"""
        <div class="{board_class}">
            <div class="board-title">Board {board_index + 1}</div>

            <div class="mini-board">
                {cells_html}
            </div>
        </div>
        """

    return f"""
<!DOCTYPE html>

<html>

<head>

    <title>Ultimate Tic-Tac-Toe</title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            background-color: #111827;
            color: white;
            text-align: center;
            margin: 0;
            padding: 30px;
        }}

        h1 {{
            font-size: 36px;
            margin-bottom: 10px;
        }}

        .status {{
            font-size: 24px;
            margin-bottom: 10px;
        }}

        .instructions {{
            color: #cbd5e1;
            margin-bottom: 25px;
        }}

        .game {{
            width: 700px;
            max-width: 95vw;
            margin: auto;

            display: grid;
            grid-template-columns: repeat(3, 1fr);

            gap: 8px;
        }}

        .small-board {{
            background-color: #1f2937;

            border: 3px solid #374151;

            padding: 8px;

            position: relative;
        }}

        .small-board.forced {{
            border-color: #38bdf8;
        }}

        .board-title {{
            font-size: 12px;
            color: #94a3b8;
            margin-bottom: 5px;
        }}

        .mini-board {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 3px;
        }}

        .cell {{
            aspect-ratio: 1;

            background-color: #0f172a;

            border: 1px solid #475569;

            color: white;

            font-size: 28px;

            font-weight: bold;

            cursor: pointer;
        }}

        .cell:hover:not(:disabled) {{
            background-color: #334155;
        }}

        .cell:disabled {{
            cursor: default;
        }}

        .winner {{
            height: 120px;

            display: flex;

            align-items: center;

            justify-content: center;

            font-size: 100px;

            font-weight: bold;

            color: #38bdf8;
        }}

        .winner.tie {{
            font-size: 35px;
            color: #94a3b8;
        }}

        .new-game {{
            margin-top: 25px;

            padding: 12px 25px;

            font-size: 16px;

            font-weight: bold;

            border: none;

            border-radius: 6px;

            background-color: #38bdf8;

            cursor: pointer;
        }}

        .new-game:hover {{
            background-color: #7dd3fc;
        }}

    </style>

</head>


<body>

    <h1>Ultimate Tic-Tac-Toe</h1>

    <div class="status">
        {status}
    </div>

    <div class="instructions">
        {instructions}
    </div>


    <form method="POST">

        <div class="game">

            {board_html}

        </div>


        <br>

        <button
            class="new-game"
            name="reset"
            value="1">

            New Game

        </button>

    </form>

</body>

</html>
"""


class GameHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            page = create_page()

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.end_headers()

            self.wfile.write(
                page.encode("utf-8")
            )

        else:

            self.send_error(404)


    def do_POST(self):

        content_length = int(
            self.headers.get("Content-Length", 0)
        )

        body = self.rfile.read(
            content_length
        ).decode("utf-8")

        data = parse_qs(body)


        if "reset" in data:

            reset_game()


        elif "move" in data:

            try:

                board_index, cell_index = map(
                    int,
                    data["move"][0].split(",")
                )

                make_move(
                    board_index,
                    cell_index
                )

            except ValueError:

                pass


        self.send_response(303)

        self.send_header(
            "Location",
            "/"
        )

        self.end_headers()


if __name__ == "__main__":

    print(
        f"Ultimate Tic-Tac-Toe running at "
        f"http://{HOST}:{PORT}"
    )

    print("Press Ctrl+C to stop the server.")

    server = HTTPServer(
        (HOST, PORT),
        GameHandler
    )

    server.serve_forever()