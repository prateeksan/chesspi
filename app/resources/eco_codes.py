from flask_restful import Resource
import pgn

# Import games list
from app import db

# Eco
# Shows a single eco code
class EcoCode(Resource):
    def get(self):
        # TODO: implement this if we have more detailed info on
        #       the individual chess openings
        return {'eco': 'B22'}

# EcoCodeList
# Shows a list of the eco codes we have in the database
class EcoCodeList(Resource):
    def get(self):

        result = db.engine.execute("SELECT DISTINCT eco from games")
        eco_code_set = [item[0] for item in result]

        return sorted(eco_code_set)