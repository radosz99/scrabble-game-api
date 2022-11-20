from fastapi import FastAPI

from scrabble_app.game_logic.models import Game
from scrabble_app.game_logic.exceptions import IncorrectMoveError, IncorrectWordError, GameIsOverError
from scrabble_app.logger import logger
import token_generator

app = FastAPI()

games = []


def get_game_via_token(game_token):
    for game in games:
        if game.token == game_token:
            return game
    return None


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


@app.get("/status")
async def get_game_statuses():
    return {'games': [game.get_short_status_in_json() for game in games]}


@app.get("/replace/{game_token}/{letters}")
async def replace_player_letters(game_token, letters):
    game = get_game_via_token(game_token)
    if not game:
        return {"valid": False, "message": "Wrong game token"}
    else:
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
    if not game:
        return {"valid": False, "message": "Wrong game token"}
    else:
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

