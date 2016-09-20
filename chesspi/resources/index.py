from flask_restful import Resource

class Index(Resource):
    def get(self):
        return {
            'chesspi': 'Chess API',
            'sample_calls': [
                {
                    'url': '/games',
                    'description': 'List of all games in the DB'
                },
                {
                    'url': '/games/16',
                    'description': 'Show game with id 16'
                },
                {
                    'url': '/games/16?format=pgn',
                    'description': 'Show game with id 16 in pgn format'
                },
                {
                    'url': '/games?name=anand',
                    'description': 'Show games played by Anand'
                },
                {
                    'url': '/games?eco=b22',
                    'description': 'Show games opening with ECO B22'
                },
                {
                    'url': '/games?format=pgn',
                    'description': 'Show games in pgn format'
                },
                {
                    'url': '/players',
                    'description': 'List of all players in DB'
                },
                {
                    'url': '/eco_codes',
                    'description': 'List of all eco codes in DB'
                }
            ]
        }