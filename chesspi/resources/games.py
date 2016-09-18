from flask_restful import Resource, abort, reqparse, fields, marshal
import pgn

# Import games list
from chesspi import games

# Set up request fields
game_fields = {
    'event': fields.String,
    'site': fields.String,
    'date': fields.String,
    'round': fields.String,
    'white': fields.String,
    'black': fields.String,
    'result': fields.String,
    'whiteelo': fields.String,
    'blackelo': fields.String,
    'eco': fields.String,
    'moves': fields.List(fields.String),
}

# Set up parser
parser = reqparse.RequestParser(trim=True)
parser.add_argument('format', type=str,
    default="json",
    choices=("json", "pgn"),
    case_sensitive=False,
    help='Valid formats: json (default) or pgn')
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
        args = parser.parse_args()
        game_id = int(game_id)
        abort_if_game_doesnt_exist(game_id)
        return format_pgn(games[game_id], args['format'])

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

        return [format_pgn(game, args['format']) for game in filtered_games]

# Format pgn object to dictionary
def format_pgn(game, output_format):

    if output_format.lower() == 'pgn':
        return pgn.dumps(game)

    return marshal(game, game_fields)

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