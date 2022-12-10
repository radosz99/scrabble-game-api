from datetime import datetime, timedelta
import os
import pytz

from scrabble_app.game_logic.move_parser import Move, Replace
from scrabble_app.logger import logger
from scrabble_app.game_logic import exceptions as exc
from scrabble_app.game_logic.models import Country, Game, GameStatus


def save_readme_for_game(game: Game, repository_path):
    readme = get_readme_for_game(game, repository_path)
    logger.debug(f"Readme for game with token {game.token}: \n {readme}")
    try:
        os.mkdir("resources/readme")
    except FileExistsError:
        pass
    with open(f"resources/readme/readme_{game.token}.txt", "w") as f:
        f.write(readme)
    return readme


def get_readme_for_game(game: Game, repository_path):
    readme = """
# Scrabble Tournament
Play in Github Scrabble Tournament! Make moves by creating issues according to the rules!
 """
    if game.status in [GameStatus.FINISHED, GameStatus.IN_PROGRESS]:
        readme += "\nStart new game:\n"
        countries_table_view = get_countries_table_view()
        for row in countries_table_view:
            readme += row
    readme += """

## Current status
"""
    readme += f" - Language - ![](https://raw.githubusercontent.com/radosz99/radosz99/main/flags/{game.country.name}.png)," \
              f"\n - Game is {game.status.name.replace('_', ' ')}," \
              f"\n - Has begun - {convert_date_to_date_string(game.initialize_timestamp)}," \
              f"\n - Total moves: {len(game.moves)},"
    if game.moves:
        f"\n - Last move has been made - {convert_date_to_date_string(game.last_move_timestamp)}."
    readme += """
### Game score
| Player name | Points |
 | - | - |  """
    score_view = get_game_score_table_view(game)
    for row in score_view:
        readme += row
    readme += "\n\nNow it is "
    readme += f"{game.players[game.whose_turn].name}'s"
    readme += """ turn, letters in rack:
<p align="center">
    """
    readme += f"<img src=\"https://raw.githubusercontent.com/{repository_path}/main/rack.png\" width=30% alt=\"Img\"/>"
    readme += """
</p>
"""
    player_letters = ''.join(game.get_letters_from_player_with_turn())
    replace_string = f"scrabble|replace|{player_letters}"
    readme += "\n## Moving rules"
    readme += f"\n - inserting letters - raise an issue with title `scrabble|move|X:Y:WORD`, where `X` and `Y` are " \
              f"coordinates, and `WORD` is string containing player's letter and letters from board, " \
              f"for example [scrabble&#124;move&#124;7:A:BRIDE]({get_issue_url('scrabble|move|7:A:BRIDE')}) if you " \
              f"want to create word `BRIDE` in 7th row starting from column A (RIDE is already on the board) and B " \
              f"is in player's letters. Number should go first if word is in a row (7:A) or second if word is in a " \
              f"column (A:7). For more details see [notation system](https://en.wikipedia.org/wiki/Scrabble" \
              f"#Notation_system) and examples in [cheater section](#cheater),"
    readme += f"\n - replacing letters - raise an issue with title `scrabble|replace|LETTERS`, where `LETTERS` is " \
              f"string of letters you want to replace, for example [scrabble&#124;replace&#124;" \
              f"{player_letters}]({get_issue_url(replace_string)}.)"
    readme += """
<p align="center">"""
    readme += f"\n<img src=\"https://raw.githubusercontent.com/{repository_path}/main/board.png\" width=60% alt=\"Img\"/>"
    readme += """
</p>
    
## Leaderboard
| Moves | Who | Points |
| - | - | - |"""
    leaderboard_table_view = get_leaderboard_table_view(game)
    for row in leaderboard_table_view:
        readme += row
    readme += """

<a name="cheater"></a>
## Cheater section  
Are you sure? :smiling_imp: :smiling_imp: :smiling_imp:
<details>
  <summary>Spoiler warning!</summary>
  
  | Id | Move | Issue link | Points |
  | - | - | - | - |  """
    best_moves_table_view = get_best_moves_table_view(game)
    for row in best_moves_table_view:
        readme += row
    readme += """
</details>
    """
    readme += """
## Latest moves
<details>
  <summary>Show latest 10 moves</summary>
  
  | Id | Type | Move / Letters to replace | Created words / New letters | Date | Points | Player | Who |
  | - | - | - | - | - | - | - | - |"""
    table_view = get_moves_table_view(game)
    for row in table_view[:10]:
        readme += row
    readme += """
</details>
    """
    return readme


def get_moves_table_view(game):
    logger.info(f"Moves = {game.moves}")
    table_view = [create_move_row(index, move, game) for index, move in enumerate(game.moves)]
    table_view.reverse()  # sorting from latest
    return table_view


def get_leaderboard_table_view(game):
    moves_dict = {}
    for move in game.moves:
        moves_number, points = moves_dict.get(move.github_user, (0, 0))
        moves_dict[move.github_user] = (moves_number + 1, points + move.points)
    leader_list = [(key, value[0], value[1]) for key, value in moves_dict.items()]
    leader_list.sort(key=lambda x: x[1], reverse=True)
    return [create_leader_row(detail[0], detail[1], detail[2]) for detail in leader_list]


def create_leader_row(github_user, moves_number, points):
    return f"\n| {moves_number} | [@{github_user}](github.com/{github_user})| {points}"


def get_countries_table_view():
    return [create_country_row(country.name) for country in Country]


def create_country_row(country_name):
    return f"\n - ![](https://raw.githubusercontent.com/radosz99/radosz99/main/flags/{country_name}.png)  [scrabble&#124;init&#124;{country_name}]({get_issue_url_for_init(country_name)})"


def create_move_row(index, move, game):
    if isinstance(move, Move):
        return f"\n|{index}| INSERT | {move.move_string} | {move.list_of_words} | {convert_date_to_date_string(move.creation_date)} | {move.points} | {get_player_name_via_id(game, move.player_id)} | [@{move.github_user}](github.com/{move.github_user}) |"
    elif isinstance(move, Replace):
        return f"\n|{index}| REPLACE | {move.letters_to_replace} | {move.new_letters} | {convert_date_to_date_string(move.creation_date)} | 0 | {get_player_name_via_id(game, move.player_id)} | [@{move.github_user}](github.com/{move.github_user}) |"


def convert_date_to_date_string(date):
    date = date.astimezone(pytz.UTC)
    date_string = date.strftime("%m/%d/%Y, %H:%M:%S")
    return f"{date_string} UTC"


def get_elapsed_time_from_datetime(old_date):
    now = datetime.now()
    now += timedelta(hours=1, minutes=20, seconds=35)
    delta = now - old_date
    seconds = int(delta.total_seconds())
    days = seconds // (60 * 60 * 24)
    seconds -= days * (60 * 60 * 24)
    hours = seconds // (60 * 60)
    seconds -= hours * (60 * 60)
    minutes = seconds // 60
    seconds -= minutes * 60
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"


def get_player_name_via_id(game, id):
    return game.players[id].name


def get_game_score_table_view(game):
    return [get_player_score_row(player.name, player.points) for _, player in game.players.items()]


def get_player_score_row(player_name, points):
    return f"\n| {player_name} | {points}"


def get_best_moves_table_view(game):
    try:
        best_moves = game.get_best_moves()
        table_view = [create_best_move_row(index + 1, move) for index, move in enumerate(best_moves)]
        return table_view
    except exc.InternalConnectionError as e:
        logger.debug(f"Best moves cannot be fetched - {str(e)}")
        return []


def create_best_move_row(index, move):
    move_string = move['move']
    return f"\n|{index}| {move_string} | [scrabble&#124;move&#124;{move_string}]({get_issue_url_for_move(move['move'])}) | {move['points']} "


def get_issue_url_for_init(country_name):
    move_title = f"scrabble|init|{country_name.upper()}"
    return get_issue_url(move_title)


def get_issue_url_for_move(move):
    move_title = f"scrabble|move|{move}"
    return get_issue_url(move_title)


def get_issue_url(title):
    return f"https://github.com/radosz99/radosz99/issues/new?title={replace_colons_and_vertical_lines(title)}" \
           f"&body=Just+push+%27Submit+new+issue%27+or+update+with+your+move."


def replace_colons_and_vertical_lines(string):
    string = string.replace(':', "%3A")
    return string.replace('|', "%7C")