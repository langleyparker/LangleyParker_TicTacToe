import pytest

from backend.app.game import UltimateTicTacToe


def test_game_starts_with_x():
    game = UltimateTicTacToe()

    assert game.current_player == "X"
    assert game.next_board is None
    assert game.winner is None


def test_first_move_sends_opponent_to_correct_board():
    game = UltimateTicTacToe()

    game.make_move(0, 4)

    assert game.boards[0][4] == "X"
    assert game.current_player == "O"
    assert game.next_board == 4


def test_player_must_play_on_required_board():
    game = UltimateTicTacToe()

    game.make_move(0, 4)

    with pytest.raises(ValueError, match="required board"):
        game.make_move(0, 0)


def test_player_cannot_use_occupied_cell():
    game = UltimateTicTacToe()

    game.make_move(0, 4)

    # Board 4 is required, so make a valid O move there first.
    game.make_move(4, 0)

    with pytest.raises(ValueError, match="already occupied"):
        game.make_move(0, 4)


def test_player_can_win_small_board():
    game = UltimateTicTacToe()

    # X -> board 0, cell 0
    game.make_move(0, 0)

    # O -> board 0, cell 1
    game.make_move(0, 1)

    # X -> board 1, cell 3
    game.make_move(1, 3)

    # O -> board 3, cell 2
    game.make_move(3, 2)

    # X -> board 2, cell 6
    game.make_move(2, 6)

    # O -> board 6, cell 4
    game.make_move(6, 4)

    # X -> board 4, cell 0
    game.make_move(4, 0)

    # O -> board 0, cell 2
    game.make_move(0, 2)

    # X -> board 2, cell 3
    game.make_move(2, 3)

    # O -> board 3, cell 0
    game.make_move(3, 0)

    # X -> board 0, cell 3
    game.make_move(0, 3)

    assert game.board_winners[0] == "X"


def test_winning_small_board_updates_overall_board():
    game = UltimateTicTacToe()

    game.board_winners = [
        "X", "X", None,
        None, None, None,
        None, None, None
    ]

    game.boards[2][0] = "X"
    game.boards[2][1] = "X"
    game.boards[2][2] = "X"

    game.current_player = "X"
    game.next_board = 2

    game.make_move(2, 3)

    assert game.board_winners[2] == "X"
    assert game.winner == "X"
