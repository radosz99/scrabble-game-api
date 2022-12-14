from PIL import Image, ImageDraw

from scrabble_app import constants as const
from scrabble_app.logger import logger


def get_clear_board():
    return Image.open("resources/clear_board.png")


def get_game_board_via_token(game_token):
    return Image.open(f"resources/boards/board_{game_token}.png")


def save_board(image, game_token):
    image.save(f"resources/boards/board_{game_token}.png")


def save_rack(image, game_token):
    image.save(f"resources/racks/rack_{game_token}.png")


def get_image_coordinates(x, y):
    new_x = const.START_X + const.FRAME_THICKNESS * (x + 1) + const.CELL_SIZE * x
    new_y = const.START_Y + const.FRAME_THICKNESS * (y + 1) + const.CELL_SIZE * y
    return new_x, new_y


def update_board_with_new_move(move, game_token, country):
    board = get_game_board_via_token(game_token)
    logger.info(f"Updating board image with move = {move.tiles}")
    for letter_tile in move.tiles:
        x_pixel, y_pixel = get_image_coordinates(letter_tile.x, letter_tile.y)
        tile = Image.open(f"resources/tiles/{country}/{letter_tile.letter.upper()}.png").convert("RGBA")
        board.paste(tile, (y_pixel, x_pixel), tile)
    save_board(board, game_token)


def update_rack_with_letters(game_token, letters_list, country):
    logger.info(f"Updating rack image with letters = {letters_list}")
    img = Image.new('RGB', (46*7, 46), color=(230, 230, 230))
    draw = ImageDraw.Draw(img)
    for index, letter in enumerate(letters_list):
        try:
            tile = Image.open(f"resources/tiles/{country}/{letter.upper()}.png").convert("RGBA")
            img.paste(tile, (46 * index, 0), tile)
            draw.line((46 * index, 0, 46 * index, 46) + img.size, fill=256)
        except FileNotFoundError as e:
            logger.info(f"Could not find file with tile - {str(e)}")
    save_rack(img, game_token)
