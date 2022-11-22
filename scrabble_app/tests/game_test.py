import unittest

from scrabble_app.game_logic.models import Game, MoveRequestBody, ReplaceRequestBody
from scrabble_app.game_logic.exceptions import IncorrectMoveError, IncorrectWordError
from scrabble_app.logger import logger

game_token = "24m829t"


def make_move(game, move):
    try:
        game.make_move(MoveRequestBody(move=move, github_user="radosz99", issue_title=f"scrabble|move|{move}",issue_number="1"))
        game.print_board()
    except IncorrectMoveError as e:
        logger.info(f"Incorrect move = {str(e)}")
    except IncorrectWordError as e:
        logger.info(f"Incorrect words created with move = {str(e)}")


class Testing(unittest.TestCase):
    # @unittest.skip("Letters replacement")
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

    # @unittest.skip("Letters replacement")
    def test_game_2(self):
        game = Game(debug=True, token=game_token, skip_word_validation=True)
        make_move(game, "7:G:ab")
        make_move(game, "7:G:abp")
        print(game.get_short_status_in_json())

    def test_letters_replacement(self):
        game = Game(debug=True, token=game_token, skip_word_validation=True)
        game.letters_replacement(ReplaceRequestBody(letters="GD", github_user="radosz99", issue_title=f"scrabble|replace|GD",issue_number="1") )


if __name__ == "__main__":
    unittest.main()
