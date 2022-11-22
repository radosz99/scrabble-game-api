from scrabble_app.game_logic.move_parser import Move, Replace


def save_readme_for_game(game, repository_path):
    with open(f"resources/readme_{game.token}.txt", "w") as f:
        f.write(get_readme_for_game(game, repository_path))


def get_readme_for_game(game, repository_path):
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
