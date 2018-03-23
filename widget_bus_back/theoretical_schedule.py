from flask_restful import Resource, reqparse
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime
from .remote_api import RemoteApi
from .bus_line import build_bus_line_combinations, BusLineSchedule

FETCH_PROCESSES = 4


class TheoreticalScheduleResource(Resource):
    def __init__(self):
        self.remote_api = RemoteApi()
        self.current_time = datetime.now()

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
        return build_theoretical_schedule(bus_line, self.current_time, remote_schedules)


def parse_request_params():
    parser = reqparse.RequestParser()
    parser.add_argument('stop', action='append', required=True)
    parser.add_argument('line', action='append', required=True)
    parser.add_argument('direction', action='append', type=int, default=[1, 2], choices=(1, 2))
    return parser.parse_args()


def to_json(obj_list):
    return list(map(lambda obj: vars(obj), obj_list))


def build_theoretical_schedule(bus_line, current_time, remote_schedules):
    try:
        terminus = remote_schedules['ligne']['directionSens' + str(bus_line.direction)]
        next_arrival = remote_schedules['prochainsHoraires'][0]
        delay_to_next_arrival = compute_delay(current_time, next_arrival['heure'], next_arrival['passages'][0])
        return BusLineSchedule(bus_line, terminus, delay_to_next_arrival)
    except KeyError as e:
        return BusLineSchedule(bus_line=bus_line, error_message=e.__class__.__name__ + ':' + str(e))


def compute_delay(current_time, next_arrival_hour_string, next_arrival_minute_string):
    next_arrival_hour = extract_hour(next_arrival_hour_string)
    next_arrival_minute = int(next_arrival_minute_string)
    next_arrival = current_time.replace(hour = next_arrival_hour, minute=next_arrival_minute)

    delay = next_arrival - current_time
    delay_in_seconds = delay.days * 86400 + delay.seconds
    if delay_in_seconds < 0:
        delay_in_seconds += 86400

    return delay_in_seconds / 60


def extract_hour(hour_string):
    """Returns the value of hour string as an integer
    >>>hour_string('14h')
    14
    >>>hour_string('3h')
    3
    >>>hour_string('10')
    10
    """
    return int(hour_string.rstrip('h'))

