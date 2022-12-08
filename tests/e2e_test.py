import os
import shutil
from datetime import datetime
import json

from fastapi.testclient import TestClient

from scrabble_app.logger import logger
from scrabble_app.game_logic.models import Country
from main import app

client = TestClient(app)

tests_results = 'tests/results'
# FOR RUN - pytest --log-cli-level INFO tests/e2e_test.py


def save_test_data_to_directory(game_status, readme, token, country):
    if not os.path.exists(tests_results):
        os.mkdir(tests_results)
    now = datetime.now()
    parsed_date = now.strftime('%Y-%m-%d_%H:%M:%S')
    dir_name = f"{parsed_date}-test-results-{country.name}-{token}"
    full_path = f"{tests_results}/{dir_name}"
    os.mkdir(full_path)
    shutil.copy('info.log', full_path)
    shutil.copy('debug.log', full_path)
    with open(f"{full_path}/game_status.json", "w+") as f:
        f.writelines(game_status)
    with open(f"{full_path}/readme.md", "w+") as f:
        f.writelines(readme)
    shutil.copyfile(f"resources/boards/board_{token}.png", f"{full_path}/board.png")


def test_e2e():
    country = Country.PL
    response = client.get(f"/initialize/{country.name}")
    response_json = response.json()
    logger.info(response_json)
    assert 'game_token' in response_json
    assert response.status_code == 200

    token = response_json['game_token']

    while True:
        response = client.get(f"/best-moves/{token}")
        response_json = response.json()

        assert 'moves' in response_json
        assert response.status_code == 200

        moves = response_json['moves']
        if not moves:
            logger.info("No moves")
            break
        first_move = moves[0]
        move_string = first_move['move']
        assert ':' in move_string
        response = client.post(f"/move/{token}",
                               json={
                                    "move": move_string,
                                    "github_user": "radosz99",
                                    "issue_title": "debug_title",
                                    "issue_number": "debug_number"})
        response_json = response.json()
        logger.info(response_json)

        assert 'detail' in response_json
        assert response.status_code == 200
        if 'over' in response_json['detail']:
            logger.info("Game is over")
            break
    logger.info(f"Token: {token}")
    response = client.get(f"/status/{token}")
    game_status = json.dumps(response.json(), indent=4)

    response = client.get(f"/readme/{token}")
    readme = response.text
    save_test_data_to_directory(game_status, readme, token, country)

