import unittest

from scrabble_app.game_logic.word_finder import find_new_words
from scrabble_app.game_logic.models import Country, Board, Game
from scrabble_app.game_logic import move_parser, cheater_service, exceptions
from scrabble_app.logger import logger


class Testing(unittest.TestCase):
    def test_first(self):
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
        new_words = ["".join(word) for word in new_words]
        logger.info(f"New words = {new_words}")
        try:
            cheater_service.validate_words(new_words, country.name)
        except exceptions.IncorrectWordError as e:
            logger.info(e)
        logger.info(f"Points: {move.evaluate()}")
        self.assertEqual(len(board), 15)

    def test_one_letter_move(self):
        game = Game(token="XD", debug=True, player_letters_mock="BRIDE")

        board = [[' ' for _ in range(15)] for _ in range(15)]
        board[7][8] = 'R'
        board[7][9] = 'I'
        board[7][10] = 'D'
        board[7][11] = 'E'
        country = Country.GB
        board_instance = Board()
        board_instance.board = board
        game.board = board_instance
        move_string = "7:H:BRIDE"
        move = move_parser.parse_move(move_string, Country.GB)
        game.validate_move_legality(move)
        new_words = find_new_words(board_instance, move)
        new_words = ["".join(word) for word in new_words]
        logger.info(f"New words = {new_words}")
        try:
            cheater_service.validate_words(new_words, country.name)
        except exceptions.IncorrectWordError as e:
            print(e)
        print(move.evaluate())
        self.assertEqual(len(board), 15)



if __name__ == "__main__":
    unittest.main()
