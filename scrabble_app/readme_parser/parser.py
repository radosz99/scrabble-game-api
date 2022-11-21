def save_readme_for_game(game):
    with open(f"resources/readme_{game.token}.txt", "w") as f:
        f.write(get_readme_for_game(game))


def get_readme_for_game(game):
    readme = """
# Last moves

| Id | Move | Created words | Date | Points | Player | 
| - | - | - | - | - | - |"""
    table_view = get_moves_table_view(game)
    for row in table_view:
        readme += row
    return readme


def get_moves_table_view(game):
    table_view = [create_move_row(index, move, game) for index, move in enumerate(game.moves)]
    table_view.reverse()
    return table_view


def create_move_row(index, move, game):
    return f"\n|{index}| {move.move_string} | {move.list_of_words} | {move.creation_date} | {move.points} | {get_player_name_via_id(game, move.player_id)} |"


def get_player_name_via_id(game, id):
    return game.players[id].name
