import unittest

import token_generator
from scrabble_app.readme_parser import parser as readme_parser
from scrabble_app.game_logic.models import Game, MoveRequestBody, ReplaceRequestBody
from scrabble_app.game_logic.exceptions import IncorrectMoveError, IncorrectWordError
from scrabble_app.logger import logger

token = token_generator.generate()


def make_move(game, move):
    try:
        game.make_move(MoveRequestBody(move=move, github_user="radosz99", issue_title=f"scrabble|move|{move}",issue_number="1"))
        # game.print_board()
    except IncorrectMoveError as e:
        logger.info(f"Incorrect move = {str(e)}")
    except IncorrectWordError as e:
        logger.info(f"Incorrect words created with move = {str(e)}")


class Testing(unittest.TestCase):
    def test_if_clear_board(self):
        game = Game(token="README_DEBUG_TOKEN", debug=True, skip_word_validation=True)
        make_move(game, "7:G:ab")
        game.letters_replacement(ReplaceRequestBody(letters="GD", github_user="radosz99", issue_title=f"scrabble|replace|GD",issue_number="1"))
        make_move(game, "7:G:abp")
        print(readme_parser.save_readme_for_game(game, "radosz99/test_repo"))


if __name__ == "__main__":
    unittest.main()
