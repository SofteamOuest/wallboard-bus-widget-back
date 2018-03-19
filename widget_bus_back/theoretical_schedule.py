from flask_restful import Resource
from flask_restful import reqparse


class TheoreticalSchedule(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('stop', required=True)
        parser.add_argument('line', action='append', required=True)
        parser.add_argument('direction', action='append', type=int, default=[1, 2], choices=(1, 2))
        args = parser.parse_args()

        return {'line': args}
