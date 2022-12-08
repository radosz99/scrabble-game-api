import unittest

from scrabble_app.game_logic.models import Game, MoveRequestBody, ReplaceRequestBody, Country
from scrabble_app.game_logic.exceptions import IncorrectMoveError, IncorrectWordError
from scrabble_app.logger import logger

def make_move(game, move):
    try:
        game.make_move(MoveRequestBody(move=move, github_user="radosz99", issue_title=f"scrabble|move|{move}",issue_number="1"))
    except IncorrectMoveError as e:
        logger.info(f"Incorrect move = {str(e)}")
    except IncorrectWordError as e:
        logger.info(f"Incorrect words created with move = {str(e)}")


class Testing(unittest.TestCase):
    # @unittest.skip("")
    def test_game(self):
        game = Game(debug=True, token="ABC", skip_word_validation=True)
        make_move(game, "H:7:abdg")
        game.put_letter_on_board(8, 3, 'G')
        game.put_letter_on_board(7, 2, 'P')
        game.put_letter_on_board(9, 2, 'P')
        game.put_letter_on_board(4, 5, 'P')
        game.put_letter_on_board(4, 3, 'D')
        make_move(game, "8:A:abdgtep")
        make_move(game, "E:4:abdgtpe")
        best_moves = game.get_best_moves()
        self.assertEqual("A:6:abated", best_moves[0]['move'])

    # @unittest.skip("")
    def test_letters_replacement(self):
        game = Game(debug=True, token="ABC", skip_word_validation=True, player_letters_mock=['G', 'D', 'C', 'R', 'B', 'C', 'H'])
        game.letters_replacement(ReplaceRequestBody(letters="GD",
                                                    github_user="radosz99",
                                                    issue_title=f"scrabble|replace|GD",
                                                    issue_number="1") )

    def test_letters_replacement_in_spanish(self):
        game = Game(country=Country.ES, debug=True, token="ABC", skip_word_validation=True, player_letters_mock=['CH', 'A', 'LL', 'RR', 'B', 'C', 'H'])
        game.letters_replacement(ReplaceRequestBody(letters="LL",
                                                    github_user="radosz99",
                                                    issue_title=f"scrabble|replace|LL",
                                                    issue_number="1") )


if __name__ == "__main__":
    unittest.main()
