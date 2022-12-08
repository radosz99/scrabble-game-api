import unittest
import os
import logging

from scrabble_app.readme_parser import parser as readme_parser
from scrabble_app.game_logic.models import Game, MoveRequestBody, ReplaceRequestBody
from scrabble_app.game_logic.exceptions import IncorrectMoveError, IncorrectWordError
from scrabble_app.logger import logger, console_handler


def make_move(game, move):
    try:
        game.make_move(MoveRequestBody(move=move, github_user="radosz99", issue_title=f"scrabble|move|{move}",issue_number="1"))
    except (IncorrectMoveError, IncorrectWordError) as e:
        logger.info(f"Error has occurred = {str(e)}")


def save_test_readme(readme):
    readme_path = "tests/results/readmes"
    try:
        os.mkdir(readme_path)
    except FileExistsError:
        pass

    with open(f"{readme_path}/readme.md", "w") as f:
        f.write(readme)


class Testing(unittest.TestCase):
    def setUp(self) -> None:
        console_handler.setLevel(logging.INFO)

    def test_saving_readme(self):
        game = Game(token="README_DEBUG_TOKEN", debug=True, skip_word_validation=True)
        make_move(game, "7:G:ab")
        game.letters_replacement(ReplaceRequestBody(letters="GD", github_user="radosz99", issue_title=f"scrabble|replace|GD",issue_number="1"))
        make_move(game, "7:G:abp")
        readme = readme_parser.get_readme_for_game(game, "radosz99/radosz99")
        save_test_readme(readme)
        self.assertTrue(os.path.exists("tests/results/readmes/readme.md"))


if __name__ == "__main__":
    unittest.main()
