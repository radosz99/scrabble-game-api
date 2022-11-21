import unittest

import token_generator
from scrabble_app.readme_parser import parser as readme_parser
from scrabble_app.game_logic.models import Game

token = token_generator.generate()


class Testing(unittest.TestCase):
    def test_if_clear_board(self):
        game = Game(token=token)
        print(readme_parser.get_readme_for_game(game))


if __name__ == "__main__":
    unittest.main()
