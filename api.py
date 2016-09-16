# Python v3.5.1
from flask import Flask
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

games = ["Game 0", "Game 1", "Game 2"]

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
        return games[game_id]

api.add_resource(HelloWorld, '/')
api.add_resource(Game, '/games/<game_id>')


if __name__ == '__main__':
    app.run(debug=True)
