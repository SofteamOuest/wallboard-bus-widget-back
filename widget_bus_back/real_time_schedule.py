import itertools
from json import JSONDecodeError
from multiprocessing.pool import ThreadPool

from flask_restful import Resource
from requests import RequestException

from widget_bus_back.bus_line import BusLineSchedule, BusLine
from widget_bus_back.remote_api import RemoteApi
from widget_bus_back.request_params import parse_stop_request_params
from widget_bus_back.response_format import to_json_compatible_object

FETCH_PROCESSES = 4


class RealTimeScheduleResource(Resource):
    def __init__(self):
        self.remote_api = RemoteApi()

    def get(self):
        request_params = parse_stop_request_params()
        stops = request_params['stop']
        schedules = self.fetch_schedules(stops)
        return to_json_compatible_object(schedules)

    def fetch_schedules(self, stops):
        unique_stops = set(stops)

        if len(stops) == 1:
            return self.fetch_schedule(stops.pop())

        pool = ThreadPool(FETCH_PROCESSES)
        schedules = pool.map(lambda l: self.fetch_schedule(l), unique_stops)
        pool.close()
        pool.join()
        return list(itertools.chain.from_iterable(schedules))

    def fetch_schedule(self, stop):
        try:
            remote_schedules = self.remote_api.fetch_real_time_schedule(stop)
            return build_real_time_schedules(stop, remote_schedules)
        except (KeyError, JSONDecodeError, RequestException) as e:
            return BusLineSchedule(bus_line=BusLine(stop), error_message=e.__class__.__name__ + ':' + str(e))


def build_real_time_schedules(stop, remote_schedules):
    schedules = map(lambda x: build_real_time_schedule(stop, x), remote_schedules)
    return list(schedules)


def build_real_time_schedule(stop, remote_schedule):
    line = remote_schedule['ligne']['numLigne']
    direction = remote_schedule['sens']
    terminus = remote_schedule['terminus']
    next = compute_delay(remote_schedule['temps'])
    bus_line = BusLine(stop, line, direction)
    return BusLineSchedule(bus_line, terminus, [next])


def compute_delay(next_arrival_minute_string):
    """Returns the value of delay string as an float
    >>> compute_delay('1 mn')
    1
    >>> compute_delay('5 mn')
    5
    >>> compute_delay('22 mn')
    22
    >>> compute_delay('1 mn 30')
    1.5
    >>> compute_delay('Proche')
    0
    >>> compute_delay('horaire.proche')
    0
    """
    if "proche" in next_arrival_minute_string.lower():
        return 0

    parts = next_arrival_minute_string.split('mn')
    parts = list(map(int, filter(None, map(str.strip, parts))))

    if len(parts) < 2:
        return parts[0]

    return parts[0] + parts[1] / 60
