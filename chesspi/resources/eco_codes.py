from flask_restful import Resource
import pgn

# Import games list
from chesspi import games

# Eco
# Shows a single eco code
class EcoCode(Resource):
    def get(self):
        # TODO: implement this if we have more detailed info on
        #       the individual chess openings
        return {'eco': games[0].eco}

# EcoCodeList
# Shows a list of the eco codes we have in the database
class EcoCodeList(Resource):
    def get(self):
        eco_code_set = {game.eco for game in games}
        return sorted(list(eco_code_set))