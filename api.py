# Python v3.5.1
from flask import Flask
from flask_restful import Resource, Api, abort
import pgn

app = Flask(__name__)
api = Api(app)

# games = ["Game 0", "Game 1", "Game 2"]

games_input = open('sample_data/kasparov.pgn').read()
games = pgn.loads(games_input)
# games = [pgn.dumps(g) for g in games_models]

# Abort the request if a game cannot be found
def abort_if_game_doesnt_exist(game_id):
    #Can be changed based on how games are retrieved
    if game_id > len(games) -1:
        abort(404, message="Game {} doesn't exist".format(game_id))

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world', 'chesspi': 'Chess API'}

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
        return [{'pgn': pgn.dumps(g)} for g in games]

# API Routing
api.add_resource(HelloWorld, '/')
api.add_resource(Game, '/games/<game_id>')
api.add_resource(GameList, '/games')

if __name__ == '__main__':
    app.run(debug=True)
