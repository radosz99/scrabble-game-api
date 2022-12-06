import unittest

from scrabble_app.game_logic.word_finder import find_new_words
from scrabble_app.game_logic.models import Country, Board, Game
from scrabble_app.game_logic import move_parser, cheater_service


class Testing(unittest.TestCase):
    def test_amount_of_returned_letters(self):
        game = Game(token="XD", debug=True, player_letters_mock="OYPBAZE")

        board = [[" ", "x", " ", " ", "h", "e", "n", " ", "u", "t", " ", " ", "o", "n", " "],
                 ["p", "u", "e", "r", " ", " ", "o", "r", " ", "a", "m", "a", "s", " ", "j"],
                 ["a", " ", "l", "e", "d", " ", " ", "a", " ", " ", "e", "r", " ", " ", "a"],
                 ["c", " ", "k", "i", " ", " ", " ", "i", " ", " ", "l", "f", " ", " ", "c"],
                 ["i", " ", "s", "n", "o", "t", " ", "n", " ", " ", "i", "s", " ", " ", "u"],
                 ["f", " ", " ", "t", " ", "o", " ", "w", " ", "d", "o", " ", " ", " ", "l"],
                 ["y", " ", " ", "e", " ", "m", "o", "a", " ", "e", "r", " ", " ", " ", "a"],
                 ["i", " ", " ", "r", " ", " ", " ", "s", "o", "l", "a", "r", " ", " ", "t"],
                 ["n", " ", " ", "v", " ", " ", " ", "h", " ", " ", "t", " ", " ", " ", "i"],
                 ["g", " ", " ", "i", " ", " ", " ", "i", " ", "b", "i", "t", "t", "e", "n"],
                 [" ", " ", " ", "e", " ", " ", " ", "n", " ", " ", "v", " ", " ", " ", "g"],
                 [" ", " ", " ", "w", " ", " ", " ", "g", " ", " ", "e", " ", " ", " ", " "],
                 [" ", " ", " ", "e", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", "d", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]
        country = Country.GB
        board_instance = Board()
        board_instance.board = board
        game.board = board_instance
        move_string = "0:A:oxyphenbutazone"
        move = move_parser.parse_move(move_string, Country.GB)
        game.validate_move_legality(move)
        new_words = find_new_words(board_instance, move)
        validation_status, incorrect_words = cheater_service.validate_words(new_words, country.name)
        print(validation_status)
        print(incorrect_words)
        print(move.evaluate())
        self.assertEqual(len(board), 15)



if __name__ == "__main__":
    unittest.main()
