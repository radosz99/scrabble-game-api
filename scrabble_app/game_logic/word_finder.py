import copy

from scrabble_app.game_logic import move_parser
from scrabble_app.logger import logger


def find_new_words(board, move):
    list_of_words = []
    logger.info("Finding new words created with move")
    if board.empty_board():
        logger.info("Empty board, so there is just one word")
        list_of_words.append(move.get_word())
    else:
        if move.orientation is move_parser.Orientation.HORIZONTAL:
            logger.info("Horizontal move")
            list_of_words = get_words_from_horizontal_move(board, move)
        elif move.orientation is move_parser.Orientation.VERTICAL:
            logger.info("Vertical move")
            list_of_words = get_words_from_vertical_move(board, move)
    return list_of_words


def get_words_from_horizontal_move(board, move, transposed=False):
    list_of_words = [get_horizontal_word(board, move)]
    list_of_words.extend(get_vertical_words_from_horizontal_move(board, move, transposed))
    return list_of_words


def get_words_from_vertical_move(board, move):
    board = copy.deepcopy(board)
    move = copy.deepcopy(move)
    board.transpose()
    move = transpose_move(move)
    logger.info("Transposing board and move")
    logger.info(f"Transposed board: \n{board.get_board_string()}")
    logger.info(f"Transposed move = {move}")
    return get_words_from_horizontal_move(board, move, transposed=True)


def get_horizontal_word(board, move):
    word = move.get_word()
    start_x, start_y = move.tiles[0].x, move.tiles[0].y
    end_x, end_y = move.tiles[-1].x, move.tiles[-1].y
    letters_before, letters_after = 0, 0
    while not board.check_if_cell_empty(start_x, start_y - 1 - letters_before):
        letters_before += 1
        word = board.get_tile_letter(start_x, start_y - letters_before) + word
    while not board.check_if_cell_empty(start_x, end_y + 1 + letters_after):
        letters_after += 1
        word = word + board.get_tile_letter(start_x, end_y + letters_after)
    logger.info(f"Letters before = {letters_before}, after = {letters_after}, created word = '{word}'")
    return word


def get_vertical_words_from_horizontal_move(board, move, transposed=False):
    words = []
    for letter_tile in move.get_user_tiles():
        logger.info(f"Searching for vertical words for letter tile = {letter_tile}")
        word = letter_tile.letter
        x, y = letter_tile.x, letter_tile.y
        letters_before, letters_after = 0, 0
        while not board.check_if_cell_empty(x - 1 - letters_before, y):
            letters_before += 1
            word = board.get_tile_letter(x - letters_before, y) + word
        while not board.check_if_cell_empty(x + 1 + letters_after, y):
            letters_after += 1
            word = word + board.get_tile_letter(x + letters_after, y)
        logger.info(f"Letters before = {letters_before}, after = {letters_after}, created word = '{word}'")
        word = word[::-1] if transposed else word
        if len(word) > 1:
            logger.info("Word has been added to the list")
            words.append(word)
    return words


def transpose_move(move):
    for letter_tile in move.tiles:
        x, y = transpose_letters_coordinates(letter_tile.x, letter_tile.y)
        letter_tile.set_new_coordinates(x, y)
    return move


def transpose_letters_coordinates(x, y):
    return 14 - y, x


def untranspose_letters_coordinates(x, y):
    return y, 14 - x

