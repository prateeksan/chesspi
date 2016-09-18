from flask_restful import Resource

class Index(Resource):
    def get(self):
        return {
            'chesspi': 'Chess API',
            'sample_calls': [
                '/games',
                '/games/16',
                '/games?name=chandler',
                '/games?eco=b22']
        }