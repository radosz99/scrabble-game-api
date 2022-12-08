import unittest

from scrabble_app.game_logic.word_finder import find_new_words
from scrabble_app.game_logic.models import Country, Board, Game
from scrabble_app.game_logic import move_parser, cheater_service, exceptions


class Testing(unittest.TestCase):
    def test_number_of_created_words(self):
        game = Game(token="XD", country=Country.ES, debug=True, player_letters_mock=['RR', 'R', 'S', 'E', 'E', 'A', 'I'])

        board = [[" ", "x", " ", " ", "h", "e", "n", " ", "u", "t", " ", " ", "o", "n", " "],
                 [" ", "u", "e", "r", " ", " ", "o", "r", " ", "a", "m", "a", "s", " ", "j"],
                 [" ", " ", "l", "e", "d", " ", " ", "a", " ", " ", "e", "r", " ", " ", "a"],
                 [" ", " ", "k", "i", " ", " ", " ", "i", " ", " ", "l", "f", " ", " ", "c"],
                 [" ", " ", "s", "n", "o", "t", " ", "n", " ", " ", "i", "s", " ", " ", "u"],
                 [" ", " ", " ", "t", " ", "o", " ", "w", " ", "d", "o", " ", " ", " ", "l"],
                 [" ", " ", " ", "e", " ", "m", "o", "a", " ", "e", "r", " ", " ", " ", "a"],
                 [" ", " ", " ", "r", " ", " ", " ", "s", "o", "l", "a", "r", " ", " ", "t"],
                 [" ", " ", " ", "v", " ", " ", " ", "h", " ", " ", "t", " ", " ", " ", "i"],
                 [" ", " ", " ", "i", " ", " ", " ", "i", " ", "b", "i", "t", "t", "e", "n"],
                 [" ", " ", " ", "e", " ", " ", " ", "n", " ", " ", "v", " ", " ", " ", "g"],
                 [" ", " ", " ", "w", " ", " ", " ", "g", " ", " ", "e", " ", " ", " ", " "],
                 [" ", " ", " ", "e", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", " ", " ", "a", " ", " ", " ", " ", " ", " ", " ", " ", " "]]
        country = Country.ES
        board_instance = Board()
        board_instance.board = board
        game.board = board_instance
        move_string = "14:A:arriera"
        move = move_parser.parse_move(move_string, country)
        game.validate_move_legality(move)
        new_words = find_new_words(board_instance, move)
        try:
            cheater_service.validate_words(new_words, country.name)
        except exceptions.IncorrectWordError as e:
            print(e)
        print(move.evaluate())
        self.assertEqual(len(board), 15)


if __name__ == "__main__":
    unittest.main()
