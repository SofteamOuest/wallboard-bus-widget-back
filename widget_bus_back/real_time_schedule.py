import itertools
from json import JSONDecodeError
from multiprocessing.pool import ThreadPool

from flask_restful import Resource
from requests import RequestException

from widget_bus_back.bus_line import BusLineSchedule, BusLine, BusLineScheduleAggregator
from widget_bus_back.remote_api import RemoteApi
from widget_bus_back.request_params import parse_stop_request_params
from widget_bus_back.response_format import to_json_compatible_object
from widget_bus_back.time_string import extract_delay

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
            return [BusLineSchedule(bus_line=BusLine(stop), error_message=e.__class__.__name__ + ':' + str(e))]


def build_real_time_schedules(stop, remote_schedules):
    schedules = [build_real_time_schedule(stop, x) for x in remote_schedules]
    aggregator = BusLineScheduleAggregator()
    for sch in schedules:
        aggregator.add(sch)
    return list(aggregator.values())


def build_real_time_schedule(stop, remote_schedule):
    line = remote_schedule['ligne']['numLigne']
    direction = remote_schedule['sens']
    terminus = remote_schedule['terminus']
    next_arrival = extract_delay(remote_schedule['temps'])
    bus_line = BusLine(stop, line, direction)
    return BusLineSchedule(bus_line, terminus, [next_arrival])
