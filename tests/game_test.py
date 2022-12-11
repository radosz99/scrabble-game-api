import unittest

from scrabble_app.game_logic.models import Game, MoveRequestBody, ReplaceRequestBody, Country
from scrabble_app.game_logic.exceptions import IncorrectMoveError, IncorrectWordError, NotEnoughLettersInRackError
from scrabble_app.logger import logger

def make_move(game, move):
    try:
        game.make_move(MoveRequestBody(move=move, github_user="radosz99", issue_title=f"scrabble|move|{move}",issue_number="1"))
    except IncorrectMoveError as e:
        logger.info(f"Incorrect move = {str(e)}")
    except IncorrectWordError as e:
        logger.info(f"Incorrect words created with move = {str(e)}")

def letters_exchange(game, letters):
    game.letters_replacement(ReplaceRequestBody(letters=letters,
                                                github_user="radosz99",
                                                issue_title=f"scrabble|replace|GD",
                                                issue_number="1"))

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
        player = game.get_current_player()
        game.letters_replacement(ReplaceRequestBody(letters="LL",
                                                    github_user="radosz99",
                                                    issue_title=f"scrabble|replace|LL",
                                                    issue_number="1") )
        self.assertNotEqual(player.get_letters(), ['CH', 'A', 'LL', 'RR', 'B', 'C', 'H'])  # will work only for 2 players

    def test_spanish_dict(self):
        game = Game(country=Country.ES, debug=True, token="ABC", skip_word_validation=True, player_letters_mock=['Ñ', 'A', 'C', 'A', 'B', 'A', 'A'])
        best_moves = game.get_best_moves()
        self.assertEqual("7:G:acabaña", best_moves[0]['move'])

    def test_raising_not_enough_letters_for_exchange_error(self):
        game = Game(country=Country.GB,  token="ABC")
        while len(game.letters_bank.letters) > 7:
            best_moves = game.get_best_moves()
            make_move(game, best_moves[0]['move'])
        logger.info(len(game.letters_bank.letters))
        logger.info(game.get_current_player().get_letters())
        self.assertRaises(NotEnoughLettersInRackError, letters_exchange, game, ''.join(game.get_current_player().get_letters()))


if __name__ == "__main__":
    unittest.main()
