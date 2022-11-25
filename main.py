from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from scrabble_app.game_logic.models import Game, MoveRequestBody, ReplaceRequestBody, Country
from scrabble_app.game_logic import exceptions as exc
from scrabble_app.logger import logger
from scrabble_app.readme_parser import parser as readme_parser
import token_generator


app = FastAPI()

games = []


init_game = Game(token='DEBUG_TOKEN', debug=True, skip_word_validation=True)
init_game.make_move(MoveRequestBody(move="7:G:ab", github_user="radosz99", issue_title="scrabble|move|7:G:ab",issue_number="1"))
init_game.make_move(MoveRequestBody(move="7:G:abp", github_user="radosz99", issue_title="scrabble|move|7:G:abp",issue_number="1"))

games.append(init_game)


def get_game_via_token(game_token):
    for game in games:
        if game.token == game_token:
            return game
    raise HTTPException(status_code=404, detail="Game with token has not been found")


def get_country_via_abbreviation(abbreviation):
    for country in Country:
        if abbreviation.upper() == country.name:
            return country
    raise HTTPException(status_code=400, detail=f"Wrong country, currently supported = {[country.name for country in Country]})")


@app.get("/initialize/{country}")
async def initialize_game(country):
    # TODO: add request body with players
    game_token = token_generator.generate(length=12)
    game = Game(token=game_token, country=get_country_via_abbreviation(country))
    games.append(game)
    return {"game_token": game_token, "detail": "New game has been initialized"}


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
    return FileResponse(f"resources/readme/readme_{game.token}.txt")


@app.get("/status")
async def get_game_statuses():
    return {'games': [game.get_short_status_in_json() for game in games]}


@app.post("/replace/{game_token}")
async def replace_player_letters(game_token, details: ReplaceRequestBody):
    game = get_game_via_token(game_token)
    try:
        response = game.letters_replacement(details)
        return {"detail": response}
    except exc.IncorrectMoveError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/best-moves/{game_token}")
async def get_possible_moves(game_token):
    game = get_game_via_token(game_token)
    return {"moves": game.get_best_moves()}


@app.post("/move/{game_token}")
async def make_move(game_token, details: MoveRequestBody):
    game = get_game_via_token(game_token)
    try:
        status = game.make_move(details)
        return {"detail": status}
    except exc.IncorrectMoveError as e:
        msg = f"Incorrect move, {str(e)}"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)
    except exc.IncorrectWordError as e:
        msg = f"Incorrect words created with move, {str(e)}"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)
    except exc.GameIsOverError as e:
        logger.info(str(e))
        raise HTTPException(status_code=400, detail=str(e))

