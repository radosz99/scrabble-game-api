import os
from pathlib import Path
from json.decoder import JSONDecodeError

import requests
from dotenv import load_dotenv

from scrabble_app.game_logic import exceptions as exc
from scrabble_app.logger import logger
from scrabble_app.constants import CHEATER_BEST_MOVES_TIMEOUT

load_dotenv(dotenv_path=Path('local.env'))

api_url = os.getenv('CHEATER_API_URL')

VALIDATION_URL = f"{api_url}/check-words"
CHEATER_URL = f"{api_url}/best-move"


def parse_move_from_response(move):
    first_coord, second_coord = move['coordinates'].split('_')
    word = move['word']
    points = move['points']
    move_string = f"{first_coord}:{second_coord}:{word}"
    return {"move": move_string, "points": points}


def get_incorrect_words_from_response(response):
    return ["".join(detail['word']) for detail in response['details'] if not detail['exist']]


def get_best_moves_from_response(response):
    return [parse_move_from_response(move) for move in response['moves'][:10]]


def get_best_moves(letters, board, country):
    logger.info("Getting best moves")
    response = send_post_request(url=f"{CHEATER_URL}/{country}",
                                 json_body={"letters": letters, "board": board},
                                 timeout=CHEATER_BEST_MOVES_TIMEOUT)
    logger.debug(f"Response: {response}")
    if "moves" not in response:
        raise exc.NotParsableResponseError(str(response))
    else:
        return get_best_moves_from_response(response)


def validate_words(words, country):
    words = [word.lower() for word in words]
    logger.info(f"Validating list of words via cheater service = {words}")
    response = send_post_request(url=f"{VALIDATION_URL}/{country}",
                                 json_body={"words": words})
    logger.debug(f"Response: {response}")
    if not response['status']:
        raise exc.IncorrectWordError(f"Some words have not passed validation = {get_incorrect_words_from_response(response)}")
    else:
        logger.info("Validation successful")


def send_post_request(json_body, url, timeout=15):
    logger.info(f"Sending post request to {url} with body = {json_body}")
    try:
        response = requests.post(url,
                                 json=json_body,
                                 timeout=timeout)
        logger.debug(f"Response {response.text}, parsing to JSON...")
        return get_parsed_json_response(response)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
            exc.NotParsableResponseError) as e:
        raise exc.InternalConnectionError(f"Something wrong with cheater server - {str(e)}")


def get_parsed_json_response(response):
    try:
        return response.json()
    except JSONDecodeError as e:
        raise exc.NotParsableResponseError(f"Cannot parse response, detail: {str(e)}, response: {response.text}")
