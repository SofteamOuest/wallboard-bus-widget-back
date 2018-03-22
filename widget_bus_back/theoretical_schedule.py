from flask_restful import Resource, reqparse
from multiprocessing.dummy import Pool as ThreadPool
from json import dumps as json_dumps
from .remote_api import RemoteApi
from .bus_line import build_bus_line_combinations

FETCH_PROCESSES = 4


class TheoreticalScheduleResource(Resource):
    def __init__(self):
        self.remote_api = RemoteApi()

    def get(self):
        request_params = parse_request_params()
        bus_lines = build_bus_line_combinations(**request_params)
        schedules = self.fetch_schedules(bus_lines)
        return to_json(schedules)

    def fetch_schedules(self, bus_lines):
        pool = ThreadPool(FETCH_PROCESSES)
        schedules = pool.map(lambda l: self.fetch_schedule(l), list(bus_lines))
        pool.close()
        pool.join()
        return schedules

    def fetch_schedule(self, bus_line):
        remote_schedules = self.remote_api.fetch_theoretical_schedule(bus_line)
        return build_schedule(bus_line, remote_schedules)


def parse_request_params():
    parser = reqparse.RequestParser()
    parser.add_argument('stop', action='append', required=True)
    parser.add_argument('line', action='append', required=True)
    parser.add_argument('direction', action='append', type=int, default=[1, 2], choices=(1, 2))
    return parser.parse_args()


def to_json(obj_list):
    return list(map(json_dumps, obj_list))


def build_schedule(bus_line, remote_schedules):
    return bus_line
