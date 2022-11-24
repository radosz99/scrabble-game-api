import unittest

from scrabble_app.game_logic.models import LettersBank, Country
from scrabble_app.game_logic import utils


class Testing(unittest.TestCase):
    def setUp(self):
        self.letters_bank = LettersBank(Country.PL)
    #
    # def test_amount_of_returned_letters(self):
    #     letters_number = 7
    #     letters = self.letters_bank.get_x_letters(letters_number)
    #     self.assertEqual(letters_number, len(letters))
    #
    # def test_if_letters_have_been_removed_from_bank(self):
    #     letters_number = 7
    #     number_of_letters_in_bank_before = len(self.letters_bank.letters)
    #     _ = self.letters_bank.get_x_letters(letters_number)
    #     number_of_letters_in_bank_after = len(self.letters_bank.letters)
    #     self.assertEqual(number_of_letters_in_bank_after + letters_number, number_of_letters_in_bank_before)
    #
    # def test_replacing(self):
    #     _ = self.letters_bank.get_x_letters(96)
    #     players_letters = "DFFKKOP"
    #     new_letters = self.letters_bank.replace_x_letters([*players_letters])
    #     print(new_letters)

    def test_amount_of_letters(self):
        counter = 0
        occurrences = utils.occurrences[self.letters_bank.country.name]
        for key, value in occurrences.items():
            counter += value
        print(counter)


if __name__ == "__main__":
    unittest.main()
