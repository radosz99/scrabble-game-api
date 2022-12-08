from enum import Enum
from datetime import datetime

from scrabble_app.game_logic.exceptions import IncorrectMoveError
from scrabble_app.game_logic import utils
from scrabble_app.logger import logger


def validate_move_string(move):
    if not isinstance(move, str):
        raise IncorrectMoveError("Move should be formatted as a string")
    move_details = move.split(':')
    if len(move_details) != 3:
        raise IncorrectMoveError("Move should contain three part separated with colon")
    return move_details


def can_convert_to_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def parse_move(move_string, country):
    logger.debug(f"Parsing move = {move_string}")
    first_coord, second_coord, letters = validate_move_string(move_string)
    logger.debug(f"First coord = {first_coord}, second coord = {second_coord}, letters = {letters}")
    if can_convert_to_int(first_coord) and isinstance(second_coord, str) and len(second_coord) == 1:
        x_coord = int(first_coord)
        y_coord = ord(second_coord) - 65
        orientation = Orientation.HORIZONTAL
    elif can_convert_to_int(second_coord) and isinstance(first_coord, str) and len(first_coord) == 1:
        y_coord = ord(first_coord) - 65
        x_coord = int(second_coord)
        orientation = Orientation.VERTICAL
    else:
        raise IncorrectMoveError("Move should be formatted like this - 8:A:KNIFE or B:13:TREE")
    letters_list = parse_letters_to_list(country, letters)
    for letter in letters_list:
        if letter not in utils.legal_letters[country.name]:
            raise IncorrectMoveError(f"Move should contain only letters from {country.name} dictionary")
    logger.debug(f"Move parsed, x coord = {x_coord}, y coord = {y_coord}, letters = {letters}, orientation = {orientation}")
    return Move(x_coord, y_coord, letters_list, orientation, move_string, country)


def parse_letters_to_list(country, letters):
    letters = letters.lower()
    logger.debug(f"Parsing letters string - {letters}")
    letters_list = []
    skip_next = False
    for index, letter in enumerate(letters):
        if skip_next:
            skip_next = False
            continue
        if country.name == "ES" and index < len(letters) - 1:
            letter, skip_next = check_if_contains_spanish_doubles(letters, index)
        letters_list.append(letter)
    logger.debug(f"Parsed letters string - {letters_list}")
    return letters_list


def check_if_contains_spanish_doubles(word, index):
    word = word.lower()
    spanish_doubles = ['ll', 'rr', 'ch']
    if (double := word[index:index + 2]) in spanish_doubles:
        return double, True
    else:
        return word[index].lower(), False

class Replace:
    def __init__(self, letters, github_user, issue_title, issue_number):
        self.valid = False
        self.github_user = github_user
        self.issue_number = issue_number
        self.issue_title = issue_title
        self.creation_date = datetime.now()
        self.letters_to_replace = letters
        self.new_letters = None
        self.player_id = None


class Move:
    def __init__(self, x_start, y_start, letters_list, orientation, move_string, country):
        self.tiles = []
        for index, letter in enumerate([letter.upper() for letter in letters_list]):
            x = x_start if orientation == Orientation.HORIZONTAL else x_start + index
            y = y_start if orientation == Orientation.VERTICAL else y_start + index
            if y > 14 or x > 14:
                raise IncorrectMoveError("Borders have been exceeded, illegal move")
            self.tiles.append(LetterTile(x, y, letter, country))
        self.points = -1
        self.orientation = orientation
        self.valid = False
        self.legal = False
        self.country = country
        self.github_user = None
        self.issue_number = None
        self.issue_title = None
        self.creation_date = datetime.now()
        self.list_of_words = []
        self.player_id = None
        self.move_string = move_string

    def __str__(self):
        return f"Orientation = {self.orientation}, points = {self.points}, valid = {self.valid}, legal = {self.legal}" \
               f", date = {self.creation_date}, github nick = {self.github_user}, list of words = {self.list_of_words}" \
               f", letter tiles = {self.tiles}"

    def __repr__(self):
        return self.__str__()

    def get_word(self):
        word = ""
        for letter_tile in self.tiles:
            word += letter_tile.letter
        return word

    def get_user_tiles(self):
        return [tile for tile in self.tiles if tile.user_letter]

    def evaluate(self):
        self.points = 0
        for letter_tile in self.tiles:
            self.points += letter_tile.evaluate_letter_tile_overall_value()
        multiplier = self.calculate_overall_word_multiplier()
        seven_letters_bonus = 50 if self.check_if_seven_letters_move() else 0
        self.points = self.points * multiplier + seven_letters_bonus
        return self.points

    def check_if_seven_letters_move(self):
        counter = 0
        for letter_tile in self.tiles:
            if letter_tile.user_letter:
                counter += 1
        return counter == 7

    def calculate_overall_word_multiplier(self):
        multiplier = 1
        for letter_tile in self.tiles:
            if letter_tile.user_letter:
                multiplier *= self.get_field_word_multiplier(letter_tile.x, letter_tile.y)
        return multiplier

    def get_field_word_multiplier(self, x, y):
        return utils.word_multiplier[x][y]


class LetterTile:
    def __init__(self, x, y, letter, country):
        self.x = x
        self.y = y
        self.letter = letter
        self.user_letter = True
        self.country = country

    def __str__(self):
        return f"Letter = {self.letter}, coordinates = ({self.x}, {self.y}), user letter = {self.user_letter}"

    def __repr__(self):
        return self.__str__()

    def mark_as_not_user_letter(self):
        self.user_letter = False

    def evaluate_letter_tile_overall_value(self):
        letter_value = self.get_letter_value()
        if self.user_letter:
            letter_multiplier = self.get_field_letter_multiplier()
        else:
            letter_multiplier = 1
        return letter_multiplier * letter_value

    def get_letter_value(self):
        return utils.letters_values[self.country.name][self.letter]

    def get_field_letter_multiplier(self):
        return utils.letter_multiplier[self.x][self.y]

    def set_new_coordinates(self, x, y):
        self.x = x
        self.y = y


class Orientation(Enum):
    VERTICAL = 1
    HORIZONTAL = 2
