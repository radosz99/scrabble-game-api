import os

from PIL import Image, ImageFont, ImageDraw

from scrabble_app.game_logic import utils
from scrabble_app.game_logic.models import Country

FONT_PATH = "resources/fonts/SpaceMono-Regular.ttf"
NARROW_FONT_PATH = "resources/fonts/mplus-1m-regular.ttf"
BACKGROUND_TILE_PATH = "resources/tiles/background.png"
TILES_PATH = "resources/tiles"
fnt_letter = ImageFont.truetype(FONT_PATH, 38)
fnt_points = ImageFont.truetype(FONT_PATH, 10)
narrow_fnt_letter = ImageFont.truetype(NARROW_FONT_PATH, 36)

LETTER_VALUES = utils.letters_values

letter_coordinates_dict = {
    "GB": (6, -7),
    "FR": (6, -7),
    "PL": (6, -7),
    "ES": (6, -5),
    "DE": (6, -5)
}

def generate_letter_tile_image(letter, points, country):
    font = fnt_letter if len(letter) == 1 else narrow_fnt_letter
    letter_coordinates = letter_coordinates_dict[country] if len(letter) == 1 else (1, 7)
    points_coordinates = (31, 30) if len(letter) == 1 else (37, 30)
    img = Image.open(BACKGROUND_TILE_PATH).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.text(letter_coordinates, letter, font=font, fill=(0, 0, 0))
    d.text(points_coordinates, points, font=fnt_points, fill=(0, 0, 0))
    return img


def create_file_with_letter_tile_image(letter, points, country):
    image = generate_letter_tile_image(letter, points, country)
    image.save(f"{TILES_PATH}/{country}/{letter}.png")


if __name__ == "__main__":
    for country, letters_values in LETTER_VALUES.items():
        for letter, value in letters_values.items():
            path = f"{TILES_PATH}/{country}"
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
            value = str(value)
            create_file_with_letter_tile_image(letter, value, country)
