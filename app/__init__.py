# Python v3.5.1

from flask import Flask
from flask_restful import Api

# initialize games from sample data
from app.common.models import games

# import resources
from app.resources.games import Game, GameList
from app.resources.index import Index
from app.resources.eco_codes import EcoCodeList
from app.resources.players import PlayerList

app = Flask(__name__)
api = Api(app)

# API Routing
api.add_resource(Index, '/')
api.add_resource(Game, '/games/<game_id>')
api.add_resource(GameList, '/games')
api.add_resource(EcoCodeList, '/eco_codes')
api.add_resource(PlayerList, '/players')