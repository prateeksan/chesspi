from flask_restful import Resource

# Game
# Shows a single game in the game list
class Game(Resource):
    def get(self, game_id):
        game_id = int(game_id)
        abort_if_game_doesnt_exist(game_id)
        return {'pgn': pgn.dumps(games[game_id])}

# GameList
# Shows a list of all games
class GameList(Resource):
    def get(self):
        args = parser.parse_args()

        # Check for filters, if none return whole list
        if any(args):
            filtered_games = filter(lambda g: game_match(g, args), games)
        else:
            filtered_games = games

        return [{
                'date': g.date,
                'black': g.black,
                'white': g.white,
                'eco': g.eco,
                'pgn': pgn.dumps(g),
                } for g in filtered_games]