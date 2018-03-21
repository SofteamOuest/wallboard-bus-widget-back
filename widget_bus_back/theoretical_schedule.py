from flask_restful import Resource, reqparse
from multiprocessing.dummy import Pool as ThreadPool
from json import dumps as json_dumps
from .bus_line import build_bus_line_combinations

FETCH_PROCESSES = 4


class TheoreticalScheduleResource(Resource):
    def get(self):
        request_params = parse_request_params()
        bus_lines = build_bus_line_combinations(request_params)
        schedules = self.fetch_schedules(bus_lines)
        return to_json(schedules)

    def fetch_schedules(self, bus_lines):
        pool = ThreadPool(FETCH_PROCESSES)
        schedules = pool.map(lambda l: self.fetch_schedule(l), list(bus_lines))
        pool.close()
        pool.join()
        return schedules

    def fetch_schedule(self, bus_line):
        return bus_line


def parse_request_params():
    param_dict = parse_request_params_to_dict()
    return to_params_map(param_dict)


def parse_request_params_to_dict():
    parser = reqparse.RequestParser()
    parser.add_argument('stop', action='append', required=True)
    parser.add_argument('line', action='append', required=True)
    parser.add_argument('direction', action='append', type=int, default=[1, 2], choices=(1, 2))
    return parser.parse_args()


def to_params_map(params_dict):
    return map(lambda x: params_dict[x], ['stop', 'line', 'direction'])


def to_json(obj_list):
    return list(map(json_dumps, obj_list))
