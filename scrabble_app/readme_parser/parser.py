import os

from scrabble_app.game_logic.move_parser import Move, Replace
from scrabble_app.logger import logger


def save_readme_for_game(game, repository_path):
    readme = get_readme_for_game(game, repository_path)
    logger.info(f"Readme for game with token {game.token}: \n {readme}")
    try:
        os.mkdir("resources/readme")
    except FileExistsError:
        pass
    with open(f"resources/readme/readme_{game.token}.txt", "w") as f:
        f.write(readme)
    return readme


def get_readme_for_game(game, repository_path):
    get_best_moves_table_view(game)
    readme = """
Play scrabble!
## Current status
### Board
<p align="center">
"""
    readme += f"<img src=\"https://raw.githubusercontent.com/{repository_path}/main/board.png\" width=70% alt=\"Img\"/>"
    readme += """
    </p>
    
### Turn
Now it is """
    readme += f"{game.players[game.whose_turn].name}"
    readme += """ turn, letters in rack:
<p align="center">
"""
    readme += f"<img src=\"https://raw.githubusercontent.com/{repository_path}/main/rack.png\" width=30% alt=\"Img\"/>"
    readme += """
</p>

### Game score
| Id | Player name | Points |
  | - | - | - |  """
    score_view = get_game_score_table_view(game)
    for row in score_view:
        readme += row
    readme += "\n## Make the move\n"
    readme += f"Make the move and insert the letters by creating an [issue]({get_issue_url('7:A:RIDE')}) according to the rules or...\n"
    readme += """
## Possibly best moves  
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

| Id | Type | Move / Letters to replace | Created words / New letters | Date | Points | Player | Who |
| - | - | - | - | - | - | - | - |"""
    table_view = get_moves_table_view(game)
    for row in table_view:
        readme += row
    return readme


def get_moves_table_view(game):
    table_view = [create_move_row(index, move, game) for index, move in enumerate(game.moves)]
    table_view.reverse()
    return table_view


def create_move_row(index, move, game):
    if isinstance(move, Move):
        return f"\n|{index}| INSERT | {move.move_string} | {move.list_of_words} | {convert_date_to_date_string(move.creation_date)} | {move.points} | {get_player_name_via_id(game, move.player_id)} | [{move.github_user}](github.com/radosz99) |"
    elif isinstance(move, Replace):
        return f"\n|{index}| REPLACE | {move.letters_to_replace} | {move.new_letters} | {convert_date_to_date_string(move.creation_date)} | 0 | {get_player_name_via_id(game, move.player_id)} | [{move.github_user}](github.com/radosz99) |"

def convert_date_to_date_string(date):
    return date.strftime("%m/%d/%Y, %H:%M:%S")

def get_player_name_via_id(game, id):
    return game.players[id].name


def get_game_score_table_view(game):
    return [get_player_score_row(index, player.name, player.points) for index, player in game.players.items()]


def get_player_score_row(index, player_name, points):
    return f"\n|{index} | {player_name} | {points}"


def get_best_moves_table_view(game):
    best_moves = game.get_best_moves()
    table_view = [create_best_move_row(index + 1, move) for index, move in enumerate(best_moves)]
    return table_view


def create_best_move_row(index, move):
    move_string = move['move']
    return f"\n|{index}| {move_string} | [scrabble&#124;move&#124;{move_string}]({get_issue_url(move['move'])}) | {move['points']} "


def get_issue_url(move):
    return f"https://github.com/radosz99/radosz99/issues/new?title=scrabble%7Cmove%7C{get_move_with_replaced_colon(move)}&body=Just+push+%27Submit+new+issue%27+or+update+with+your+move."

def get_move_with_replaced_colon(move_string):
    return move_string.replace(':', "%3A")