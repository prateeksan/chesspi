from flask_restful import Resource, fields, marshal, reqparse
import pgn

# Import games list
from app import models

# Set up request fields
player_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
}

# Set up parser
parser = reqparse.RequestParser(trim=True)
parser.add_argument('name', type=str,
    case_sensitive=False,
    store_missing=False,
    help='Name of player')

# Player
# Shows a single eco code
class Player(Resource):
    def get(self, player_id):

        player = models.Player.query.get(int(player_id))

        if player is None:
            abort(404, message="Player {} does not exist".format(player_id))

        return marshal(player, player_fields)

# PlayerList
# Shows a list of players and number of games in the database
class PlayerList(Resource):
    def get(self):

        args = parser.parse_args()
        players = models.Player.query.all()
        
        if any(args):
            players = list(filter(lambda p: player_match(p, args), players))

        return marshal(players, player_fields)

def player_match(player, args):
    if 'name' in args and args['name'] not in player.full_name().lower():
        return False

    return True