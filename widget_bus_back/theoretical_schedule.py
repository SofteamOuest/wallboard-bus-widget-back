from flask_restful import Resource
from flask_restful import reqparse

from .bus_line import BusLinePermutation


class TheoreticalScheduleResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('stop', action='append', required=True)
        parser.add_argument('line', action='append', required=True)
        parser.add_argument('direction', action='append', type=int, default=[1, 2], choices=(1, 2))
        args = parser.parse_args()

        p = BusLinePermutation(map(lambda x: args[x], ['stop', 'line', 'direction']))

        return {'line': args}
