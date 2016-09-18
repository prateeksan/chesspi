from flask_restful import Resource, abort, reqparse
import pgn

# Load games
# TODO: Move the loading of game data to common area
games_input = open('sample_data/kasparov.pgn').read()
games = pgn.loads(games_input)

# Set up parser
parser = reqparse.RequestParser(trim=True)
parser.add_argument('name', type=str, 
    case_sensitive=False,
    store_missing=False,
    help='Name of player')
parser.add_argument('eco', type=str, 
    case_sensitive=False,
    store_missing=False,
    help='Encyclopedia of Chess Opening (ECO) Codes')

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

# Abort the request if a game cannot be found
def abort_if_game_doesnt_exist(game_id):
    #Can be changed based on how games are retrieved
    if game_id > len(games) -1:
        abort(404, message="Game {} doesn't exist".format(game_id))

def game_match(game, args):
    if 'name' in args:
        if args['name'] not in game.black.lower() and \
           args['name'] not in game.white.lower():
            return False
    if 'eco' in args:
        if args['eco'] != game.eco.lower():
            return False
    return True