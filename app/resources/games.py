from flask_restful import Resource, abort, reqparse, fields, marshal
import pgn

# Import app modules:
from app.common.game_parser import GameParser

# Import games list
from app import games
from app import limiter

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
    decorators = [limiter.limit("1/second")]
    def get(self):
        args = parser.parse_args()

        games_parser = GameParser()
        games = games_parser.get_games(args)

        return games_parser.format_games(games, return_type=args['format'])

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