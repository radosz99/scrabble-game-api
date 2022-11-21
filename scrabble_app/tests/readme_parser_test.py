import unittest

import token_generator
from scrabble_app.readme_parser import parser as readme_parser
from scrabble_app.game_logic.models import Game
from scrabble_app.game_logic.exceptions import IncorrectMoveError, IncorrectWordError
from scrabble_app.logger import logger
token = token_generator.generate()


def make_move(game, move):
    try:
        game.make_move(move)
        # game.print_board()
    except IncorrectMoveError as e:
        logger.info(f"Incorrect move = {str(e)}")
    except IncorrectWordError as e:
        logger.info(f"Incorrect words created with move = {str(e)}")


class Testing(unittest.TestCase):
    def test_if_clear_board(self):
        game = Game(token=token, debug=True)
        make_move(game, "7:G:ab")
        make_move(game, "7:G:abp")
        print(readme_parser.get_readme_for_game(game))


if __name__ == "__main__":
    unittest.main()
