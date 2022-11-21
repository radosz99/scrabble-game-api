from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from scrabble_app.game_logic.models import Game
from scrabble_app.game_logic.exceptions import IncorrectMoveError, IncorrectWordError, GameIsOverError
from scrabble_app.logger import logger
from scrabble_app.readme_parser import parser as readme_parser
import token_generator

app = FastAPI()

games = []


init_game = Game(token='DEBUG_TOKEN', debug=True, skip_word_validation=True)
init_game.make_move("7:G:ab")
init_game.make_move("7:G:abp")
games.append(init_game)


def get_game_via_token(game_token):
    for game in games:
        if game.token == game_token:
            return game
    raise HTTPException(status_code=404, detail="Game with token has not been found")


@app.get("/initialize")
async def initialize_game():
    # TODO: add request body with players
    game_token = token_generator.generate(length=12)
    game = Game(token=game_token)
    games.append(game)
    return {"game_token": game_token}


@app.get("/status/{game_token}")
async def get_game_status(game_token):
    game = get_game_via_token(game_token)
    return game.get_status_in_json()


@app.get("/board-image/{game_token}")
async def get_board_image(game_token):
    game = get_game_via_token(game_token)
    return FileResponse(f"resources/boards/board_{game.token}.png")


@app.get("/rack-image/{game_token}")
async def get_rack_image(game_token):
    game = get_game_via_token(game_token)
    return FileResponse(f"resources/racks/rack_{game.token}.png")


@app.get("/readme/{game_token}")
async def get_readme(game_token, repository_path: str = "radosz99/radosz99"):
    game = get_game_via_token(game_token)
    readme_parser.save_readme_for_game(game, repository_path)
    return FileResponse(f"resources/readme_{game.token}.txt")


@app.get("/status")
async def get_game_statuses():
    return {'games': [game.get_short_status_in_json() for game in games]}


@app.get("/replace/{game_token}/{letters}")
async def replace_player_letters(game_token, letters):
    game = get_game_via_token(game_token)
    try:
        response = game.letters_replacement(letters.upper())
        return {"valid": True, "message": response}
    except IncorrectMoveError as e:
        return {"valid": False, "message": str(e)}


@app.get("/best-moves/{game_token}")
async def get_possible_moves(game_token):
    game = get_game_via_token(game_token)
    return {"moves": game.get_best_moves()}


@app.post("/move/{game_token}/{move_string}")
async def make_move(game_token, move_string):
    # TODO: handle github username
    game = get_game_via_token(game_token)
    try:
        status = game.make_move(move_string)
        return {"valid": True, "message": status}
    except IncorrectMoveError as e:
        msg = f"Incorrect move = {str(e)}"
        logger.info(msg)
        return {"valid": False, "message": msg}
    except IncorrectWordError as e:
        msg = f"Incorrect words created with move = {str(e)}"
        logger.info(msg)
        return {"valid": False, "message": msg}
    except GameIsOverError as e:
        logger.info(str(e))
        return {"valid": False, "message": str(e)}

