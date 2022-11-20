from PIL import Image, ImageFont, ImageDraw

from scrabble_app.game_logic import utils

FONT_PATH = "resources/fonts/SpaceMono-Regular.ttf"
BACKGROUND_TILE_PATH = "resources/tiles/background.png"
TILES_PATH = "resources/tiles"
fnt_letter = ImageFont.truetype(FONT_PATH, 40)
fnt_points = ImageFont.truetype(FONT_PATH, 10)

LETTER_VALUES = utils.letter_values


def generate_letter_tile_image(letter, points):
    img = Image.open(BACKGROUND_TILE_PATH).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.text((6, -10), letter, font=fnt_letter, fill=(0, 0, 0))
    d.text((31, 30), points, font=fnt_points, fill=(0, 0, 0))
    return img


def create_file_with_letter_tile_image(letter, points):
    image = generate_letter_tile_image(letter, points)
    image.save(f"{TILES_PATH}/{letter}.png")


if __name__ == "__main__":
    for key, value in LETTER_VALUES.items():
        value = str(value)
        create_file_with_letter_tile_image(key, value)
