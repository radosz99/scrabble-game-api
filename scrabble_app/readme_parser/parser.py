from scrabble_app.game_logic.move_parser import Move, Replace
from scrabble_app.logger import logger

def save_readme_for_game(game, repository_path):
    readme = get_readme_for_game(game, repository_path)
    logger.info(f"Readme for game with token {game.token}: \n {readme}")
    with open(f"resources/readme_{game.token}.txt", "w") as f:
        f.write(readme)


def get_readme_for_game(game, repository_path):
    get_best_moves_table_view(game)
    readme = """
# Board

<p align="center">
"""
    readme += f"<img src=\"https://raw.githubusercontent.com/{repository_path}/main/board.png\" width=70% alt=\"Img\"/>"
    readme += """
    </p>
    
# Last moves

| Id | Type | Move / Letters to replace | Created words / New letters | Date | Points | Player | 
| - | - | - | - | - | - | - |"""
    table_view = get_moves_table_view(game)
    for row in table_view:
        readme += row
    readme += """
# Possibly best moves:

<details>
  <summary>Spoiler warning</summary>
  
  | Id | Move | Issue title | Points | Link |
  | - | - | - | - | - | """
    best_moves_table_view = get_best_moves_table_view(game)
    for row in best_moves_table_view:
        readme += row
    readme += """
</details>
    """
    return readme


def get_moves_table_view(game):
    table_view = [create_move_row(index, move, game) for index, move in enumerate(game.moves)]
    table_view.reverse()
    return table_view


def create_move_row(index, move, game):
    if isinstance(move, Move):
        return f"\n|{index}| INSERT | {move.move_string} | {move.list_of_words} | {move.creation_date} | {move.points} | {get_player_name_via_id(game, move.player_id)} |"
    elif isinstance(move, Replace):
        return f"\n|{index}| REPLACE | {move.letters_to_replace} | {move.new_letters} | {move.creation_date} | 0 | {get_player_name_via_id(game, move.player_id)} |"


def get_player_name_via_id(game, id):
    return game.players[id].name


def get_best_moves_table_view(game):
    best_moves = game.get_best_moves()
    table_view = [create_best_move_row(index + 1, move) for index, move in enumerate(best_moves)]
    return table_view


def create_best_move_row(index, move):
    return f"\n|{index}| {move['move']} | scrabble&#124;move&#124;{move['move']} | {move['points']} | {get_issue_url(move['move'])}"


def get_issue_url(move):
    return f"https://github.com/radosz99/radosz99/issues/new?title=scrabble|move|{move}&body=Just+push+%27Submit+new+issue%27+or+update+with+your+move."
