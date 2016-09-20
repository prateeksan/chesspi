# Python v3.5.1
from flask import Flask
from flask_restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')
db = SQLAlchemy(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/test')

if __name__ == '__main__':
    app.run(debug=True)

# TODO(https://github.com/mmautner/simple_api use this)