from flask import Flask
from flask_restful import Resource, Api
from flask_restful.utils import cors

app = Flask(__name__)
api = Api(app)
api.decorators = [cors.crossdomain(origin='*')]


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
