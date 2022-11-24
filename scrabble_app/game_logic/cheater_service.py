import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from scrabble_app.logger import logger

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
    return [detail['word'] for detail in response['details'] if not detail['exist']]


def get_best_moves_from_response(response):
    return [parse_move_from_response(move) for move in response['moves'][:10]]


def get_best_moves(letters, board, country):
    logger.info("Getting best moves")
    response = send_post_request(url=f"{CHEATER_URL}/{country}", json_body={"letters": letters, "board": board})
    return get_best_moves_from_response(response)


def validate_words(words, country):
    words = [word.lower() for word in words]
    logger.info(f"Validating list of words via cheater service = {words}")
    response = send_post_request(url=f"{VALIDATION_URL}/{country}", json_body={"words": words})
    return response['status'], get_incorrect_words_from_response(response)


def send_post_request(json_body, url):
    logger.info(f"Sending post request to {url} with body = {json_body}")
    response = requests.post(url, json=json_body).json()
    logger.info(f"Response {response}")
    return response