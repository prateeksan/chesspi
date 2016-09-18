# Python v3.5.1

from flask import Flask
from flask_restful import Api

# initialize games from sample data
from chesspi.common.models import games

# import resources
from chesspi.resources.games import Game, GameList
from chesspi.resources.index import Index

app = Flask(__name__)
api = Api(app)

# API Routing
api.add_resource(Index, '/')
api.add_resource(Game, '/games/<game_id>')
api.add_resource(GameList, '/games')