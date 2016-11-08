from flask_restful import Resource, abort, reqparse
import pgn

# Import app modules:
from app.common.game_parser import GameParser

# Import games list
from app import limiter

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

        game_parser = GameParser()
        game = game_parser.get_game(game_id)

        if game is None:
            abort(404, message="Game {} doesn't exist".format(game_id))

        return game_parser.format_game(game, return_type=args['format'])

    def post(self):
        """Creates a new game via an API request"""
        # TODO(Test this)
        # TODO(200 should only be returned on success)
        # TODO(Add Authentication)
        args = parser.parse_args()
        if pgn in args:
            game_parser = GameParser(pgn_string=args['pgn'])
            game_parser.add_games()
        return 200

# GameList
# Shows a list of all games
class GameList(Resource):
    decorators = [limiter.limit("1/second")]
    def get(self):
        args = parser.parse_args()

        game_parser = GameParser()
        games = game_parser.get_games(args)

        return game_parser.format_games(games, return_type=args['format'])