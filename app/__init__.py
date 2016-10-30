# Python v3.5.1

from flask import Flask
from flask_restful import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')
db = SQLAlchemy(app)
limiter = Limiter(app, key_func=get_remote_address)

# import models
from app.common import models

# import resources
from app.resources.games import Game, GameList
from app.resources.index import Index
from app.resources.eco_codes import EcoCodeList
from app.resources.players import Player, PlayerList

# API Routing
api.add_resource(Index, '/')
api.add_resource(Game, '/games/<game_id>')
api.add_resource(GameList, '/games')
api.add_resource(EcoCodeList, '/eco_codes')
api.add_resource(PlayerList, '/players')
api.add_resource(Player, '/players/<player_id>')