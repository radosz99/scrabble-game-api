import unittest

from scrabble_app.game_logic.models import Board


class Testing(unittest.TestCase):
    def test_if_clear_board(self):
        board = Board()
        board.print_board()


if __name__ == "__main__":
    unittest.main()
