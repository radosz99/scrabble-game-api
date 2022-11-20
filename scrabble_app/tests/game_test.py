import unittest

from scrabble_app.game_logic.models import Game
from scrabble_app.game_logic.exceptions import IncorrectMoveError, IncorrectWordError
from scrabble_app.logger import logger

game_token = "24m829t"


def make_move(game, move):
    try:
        game.make_move(move)
        game.print_board()
    except IncorrectMoveError as e:
        logger.info(f"Incorrect move = {str(e)}")
    except IncorrectWordError as e:
        logger.info(f"Incorrect words created with move = {str(e)}")


class Testing(unittest.TestCase):
    def test_game(self):
        game = Game(debug=True, token=game_token, skip_word_validation=True)
        make_move(game, "H:7:abdg")
        game.put_letter_on_board(8, 3, 'G')
        game.put_letter_on_board(7, 2, 'P')
        game.put_letter_on_board(9, 2, 'P')
        game.put_letter_on_board(4, 5, 'P')
        game.put_letter_on_board(4, 3, 'D')
        # game.put_letter_on_board(8, 8, 'G')
        make_move(game, "8:A:abdgtep")
        make_move(game, "E:4:abdgtpe")
        print(game.get_best_moves())
        print(game.get_status_in_json())

    def test_game_2(self):
        game = Game(debug=True, token=game_token)
        make_move(game, "7:G:ab")
        print(game.players)
        make_move(game, "7:G:abp")
        print(game.players)

    def test_letters_replacement(self):
        game = Game(debug=True, token=game_token)
        game.letters_replacement("GD")