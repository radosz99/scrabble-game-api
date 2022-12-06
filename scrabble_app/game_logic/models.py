import random
import copy
import shutil
from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from . import utils
from . import move_parser
from . import exceptions as exc
from . import word_finder
from . import cheater_service
from scrabble_app.images_updater import updater
from scrabble_app.logger import logger


class BaseRequestBody(BaseModel):
    github_user: str
    issue_title: str
    issue_number: str


class MoveRequestBody(BaseRequestBody):
    move: str


class ReplaceRequestBody(BaseRequestBody):
    letters: str


class GameStatus(Enum):
    IN_PROGRESS = 1
    FINISHED = 2


class Country(Enum):
    GB = 1
    PL = 2
    ES = 3


class Game:
    def __init__(self, token, country=Country.GB, debug=False, skip_word_validation=False, player_letters_mock=None):
        logger.info(f"Creating new Game instance, debug = {debug}, token = {token}, country = {country}")
        self.country = country
        self.token = token
        self.debug = debug
        self.skip_word_validation = skip_word_validation
        self.letters_bank = LettersBank(country)
        self.board = Board()
        if not player_letters_mock:
            player_letters_mock_1 = ['A', 'B', 'D', 'G', 'T', 'E', 'P']
            player_letters_mock_2 = ['A', 'B', 'D', 'G', 'T', 'E', 'P']
        else:
            player_letters_mock_1 = [*player_letters_mock]
            player_letters_mock_2 = [*player_letters_mock]

        # TODO: extend to max 4 players
        self.players = {
            0: Player("Tom", 0, player_letters_mock_1 if debug else self.letters_bank.get_x_letters(7)),
            1: Player("Jerry", 1, player_letters_mock_2 if debug else self.letters_bank.get_x_letters(7))
        }
        self.players_number = len(self.players)
        logger.info(f"Created players = {self.players}")
        self.whose_turn = 0
        self.first_turn = True
        self.initialize_timestamp = datetime.now()
        self.last_move_timestamp = None
        self.status = GameStatus.IN_PROGRESS
        self.winner_id = None
        self.create_images()
        self.moves = []

    def make_move(self, details):
        move_string = details.move

        if self.status == GameStatus.FINISHED:
            raise exc.GameIsOverError(f"Game is over, winner is = {self.players[self.winner_id].name}, points = {self.players[self.winner_id].points}")
        move = move_parser.parse_move(move_string, self.country)
        move.github_user = details.github_user
        move.issue_title = details.issue_title
        move.issue_number = details.issue_number
        logger.info(f"Player with id = {self.whose_turn} wants to make a move {move}")
        self.validate_move_legality(move)
        move.legal = True
        if not self.skip_word_validation:
            self.validate_words_from_move(move)
        logger.info(f"Gained points with this move = {move.evaluate()}")
        self.board.make_move(move)
        move.valid = True
        letters_before = "".join(self.get_letters_from_player_with_turn())
        self.proceed_after_turn(move)
        self.last_move_timestamp = datetime.now()
        msg = f"Valid move, points = {move.points}, created words = {move.list_of_words}, player's letters before the move = " \
               f"{letters_before}"
        if self.status == GameStatus.FINISHED:
            msg += f", game is over, winner = {self.players[self.winner_id].name}!"
        return msg

    def create_images(self):
        shutil.copyfile('resources/clear_board.png', f"resources/boards/board_{self.token}.png")
        letters_list = self.get_letters_from_player_with_turn()
        updater.update_rack_with_letters(self.token, letters_list, self.country.name)

    def validate_move_legality(self, move):
        contains_user_letters, contains_board_letters, middle_filled = False, False, False
        user_letters = self.get_letters_from_player_with_turn()
        original_letters = user_letters
        # TODO: refactor with method calls
        for letter_tile in move.tiles:
            logger.info(f"Validating letter tile = {letter_tile}")
            letter_from_board = self.board.get_tile_letter(letter_tile.x, letter_tile.y)
            logger.info(f"Letter on real board in cell with this coords = '{letter_from_board}'")
            if letter_from_board != ' ':
                if letter_from_board.lower() != letter_tile.letter.lower():
                    logger.info(f"Letters are not equal ({letter_from_board} != {letter_tile.letter}), illegal move")
                    raise exc.IncorrectMoveError("Inaccuracy between move and letters on board")
                letter_tile.mark_as_not_user_letter()
                contains_board_letters = True
                logger.info("Letter from board, has been marked as a not player letter")
            else:
                try:
                    logger.info("Checking if it in player's letters")
                    user_letters.remove(letter_tile.letter)
                    logger.info(f"Player's letters = {self.get_letters_from_player_with_turn()}")
                    logger.info("Letter is in player's letters")
                    if self.empty_board() and letter_tile.x == 7 and letter_tile.y == 7:
                        logger.info("Letter is in the middle - 7,7 coordinates")
                        middle_filled = True
                except ValueError:
                    logger.info("Letter is not in player's letters")
                    raise exc.IncorrectMoveError(f"Some illegal letters in move - {letter_tile.letter}, "
                                                 f"player letters = {original_letters}")
                contains_user_letters = True

        if self.empty_board():
            if not contains_user_letters:
                logger.info("No user letters")
                raise exc.IncorrectMoveError("Move should contain both - player and board letters (at least 1)")
            if not middle_filled:
                logger.info("No letter with the middle coordinates - 7,7")
                raise exc.IncorrectMoveError("Move should contain letter in the middle of the board")
        else:
            if not contains_board_letters or not contains_user_letters:
                logger.info(f"Wrong letters, contains board letters = {contains_board_letters}, player letters = "
                            f"{contains_user_letters}")
                raise exc.IncorrectMoveError("Move should contain both - player and board letters (at least 1)")

    def validate_words_from_move(self, move):
        list_of_words = self.find_new_words(move)
        move.list_of_words = list_of_words
        logger.info(f"List of new potential words = {list_of_words}")
        try:
            cheater_service.validate_words(list_of_words, self.country.name)
            logger.info("All words have passed validation")
        except (exc.NotParsableResponseError, exc.IncorrectWordError) as e:
            logger.info(f"Error during validation - {str(e)}")
            raise e

    def find_new_words(self, move):
        return word_finder.find_new_words(self.board, move)

    def put_letter_on_board(self, x, y, letter):
        self.board.put_letter(x, y, letter)

    def proceed_after_turn(self, move):
        player = self.get_current_player()

        if move.valid:
            if not self.debug:
                self.update_player_letters(player, move)
            logger.info(f"Player has got new letters, current player status = {player}")
            self.switch_turn()
            logger.info(f"Changing turn, it is turn of player with id = {self.whose_turn}")
            player.points += move.points
            logger.info(f"Player's points increased by {move.points}, currently {player.points}")
            self.update_images(move)
            self.first_turn = False
            if self.check_if_game_is_over():
                self.status = GameStatus.FINISHED
        else:
            logger.info("Move is not valid, so the turn won't be changed and letters remain the same")
        logger.info(f"Assigning move = {move} to player")
        move.player_id = player.id
        self.moves.append(move)

    def update_player_letters(self, player, move):
        used_letters = [letter_tile.letter for letter_tile in move.get_user_tiles()]
        logger.info(f"Removing letters from player's letters = {used_letters}")
        player.remove_letters([letter_tile.letter for letter_tile in move.get_user_tiles()])
        letters_to_give = 7 - len(player.get_letters())
        player.give_letters(self.letters_bank.get_x_letters(letters_to_give))

    def letters_replacement(self, details):
        logger.info(f"Replacing letters with details = {details}")
        letters_to_replace = details.letters.upper()
        player = self.get_current_player()
        valid_letters = player.check_if_letters_in_players_letters(letters_to_replace)
        if valid_letters:
            move = move_parser.Replace(letters_to_replace, details.github_user, details.issue_title, details.issue_number)
            player.remove_letters([*letters_to_replace.upper()])
            new_letters = self.letters_bank.replace_x_letters(letters_to_replace)
            player.give_letters(new_letters)
            move.new_letters = "".join(new_letters)
            self.switch_turn()
            move.valid = True
            move.player_id = player.id
            self.update_images()
            self.first_turn = False
            msg = f"New players letters = {new_letters}, old = {letters_to_replace}, current letters = {player.get_letters()}"
            logger.info(msg)
            self.moves.append(move)
            return msg
        else:
            raise exc.IncorrectMoveError(f"Invalid letters to replace, players letters = {player.get_letters()}")

    def get_current_player(self):
        logger.info(f"Getting current player with id = {self.whose_turn}")
        return self.players[self.whose_turn]

    def check_if_game_is_over(self):
        logger.info("Checking if game has finished")
        if self.letters_bank.empty():
            logger.info("Empty letters bank, checking players letters")
            for player in self.players.values():
                logger.info(f"Checking player {player.name}, has letters = {player.has_letters()}, letters = {player.get_letters_string()}")
                if not player.has_letters():
                    logger.info("No letters, game is over")
                    self.winner_id = self.get_winner()
                    logger.info(f"Winner id = {self.winner_id}, points = {self.players[self.winner_id].points}")
                    return True
        else:
            return False

    def get_winner(self):
        highest_score = 0
        player_id = None
        # TODO: read rules of counting points and update accordingly- http://www.pfs.org.pl/regulaminy.php
        # TODO: add skipping mechanism accordingly
        for player in self.players.values():
            if player.points > highest_score:
                player_id = player.id
                highest_score = player.points
        return player_id

    def update_images(self, move=None):
        if move is not None:
            updater.update_board_with_new_move(move, self.token, self.country.name)
        letters_list = self.get_letters_from_player_with_turn()
        updater.update_rack_with_letters(self.token, letters_list, self.country.name)

    def next_player_id(self):
        return self.whose_turn + 1 if self.players_number > self.whose_turn + 1 else 0

    def switch_turn(self):
        self.whose_turn = self.next_player_id()
        logger.info(f"Changing turn to player with id = {self.whose_turn}")

    def get_letters_from_player_with_turn(self):
        logger.info("Getting letters from player with turn")
        return self.get_current_player().get_letters()

    def empty_board(self):
        return self.board.empty_board()

    def get_best_moves(self):
        player_letters = self.get_current_player().get_letters_string()
        return cheater_service.get_best_moves(player_letters, self.board.get_board_copy(), self.country.name)

    def print_board(self):
        logger.info(f"Current board status: \n{self.board.get_board_string()}")

    def get_status_in_json(self):
        return {
            'initialize_timestamp': self.initialize_timestamp,
            'winner_id': self.winner_id,
            'status': self.status.name,
            'last_move_timestamp': self.last_move_timestamp,
            'whose_turn': self.whose_turn,
            'players': self.players,
            'board': self.board,
            'letters_bank': self.letters_bank,
            'moves': self.moves
        }

    def get_short_status_in_json(self):
        players = [self.players[player].get_status() for player in self.players.keys()]
        return {"token": self.token,
                "winner_id": self.winner_id,
                "players": players,
                "initialize_timestamp": self.initialize_timestamp,
                "last_move_timestamp": self.last_move_timestamp,
                "letters_bank": "".join(self.letters_bank.letters),
                "letters_on_board": self.board.count_letters_on_board(),
                "moves": self.moves}


class LettersBank:
    def __init__(self, country: Country):
        self.letters = []
        self.country = country
        occurrences = utils.occurrences[country.name]
        for key, value in occurrences.items():
            self.letters.extend([key for _ in range(value)])

    def __repr__(self):
        return self.letters

    def __str__(self):
        return f"{len(self.letters)} letters = {self.letters}"

    def get_x_letters(self, number):
        chosen_letters = []
        logger.info(f"Getting {number} letters from bank, current bank status is {len(self.letters)} letters = "
                    f"{self.letters}")
        for _ in range(number):
            if len(self.letters) > 0:
                index = random.randint(0, len(self.letters) - 1)
                letter = self.letters.pop(index)
                logger.info(f"'{letter}' has been drawn, letters left = {len(self.letters)}")
                chosen_letters.append(letter)
            else:
                logger.info("No more letters in bank")
                break
        return chosen_letters

    def replace_x_letters(self, old_letters):
        new_letters = self.get_x_letters(len(old_letters))
        difference = len(old_letters) - len(new_letters)
        for i in range(difference):
            letter = random.choice(old_letters)
            old_letters.remove(letter)
            new_letters.append(letter)
        self.letters.extend(old_letters)
        logger.info(f"Letters bank has been extended of {len(old_letters)} letters = {old_letters}")
        return new_letters

    def empty(self):
        return False if self.letters else True


class Board:
    def __init__(self):
        self.board = utils.get_empty_board()

    def get_board_string(self):
        board_string = "\n"
        for row in self.board:
            board_string += f"{str(row)}\n"
        return board_string

    def get_board_copy(self):
        return copy.deepcopy(self.board)

    def get_tile_letter(self, x, y):
        if x > 14 or y > 14 or x < 0 or y < 0:
            raise ValueError(f"Wrong coordinates, x = {x}, y = {y}")
        else:
            return self.board[x][y]

    def check_if_cell_empty(self, x, y):
        if x > 14 or y > 14 or x < 0 or y < 0:
            return True
        else:
            return self.board[x][y] == ' '

    def count_letters_on_board(self):
        counter = 0
        for row in self.board:
            for cell in row:
                if cell != ' ':
                    counter += 1
        return counter

    def transpose(self):
        self.board = [([self.board[y][14 - x] for y in range(15)]) for x in range(15)]

    def put_letter(self, x, y, letter):
        self.board[x][y] = letter

    def empty_board(self):
        for row in self.board:
            for letter in row:
                if letter != ' ':
                    return False
        return True

    def make_move(self, move):
        for letter_tile in move.get_user_tiles():
            self.board[letter_tile.x][letter_tile.y] = letter_tile.letter

    def __repr__(self):
        return self.get_board_string()


class Player:
    def __init__(self, name, id, letters):
        self.name = name
        self.id = id
        self.letters = letters
        self.points = 0

    def give_letters(self, letters):
        self.letters.extend(letters)

    def get_letters(self):
        return list(self.letters)

    def get_letters_string(self):
        return ''.join(self.letters)

    def has_letters(self):
        return True if self.letters else False

    def get_status(self):
        return {'name': self.name,
                'points': self.points,
                'letters': "".join(self.letters)}

    def check_if_letters_in_players_letters(self, letters_to_check):
        for letter in letters_to_check:
            if letter not in self.letters:
                return False
        return True

    def remove_letters(self, letters_list):
        logger.info(f"Removing letters from player's rack = {letters_list}")
        for letter in letters_list:
            try:
                self.letters.remove(letter)
            except ValueError:
                logger.info("Letter not in the list")
                return False
        return True

    def __str__(self):
        return f"Player '{self.name}' with id = {self.id}, letters = {self.letters}, points = {self.points}"

    def __repr__(self):
        return self.__str__()

