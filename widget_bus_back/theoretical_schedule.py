from json import JSONDecodeError

from flask_restful import Resource
from multiprocessing.dummy import Pool as ThreadPool

from requests import RequestException

from widget_bus_back.response_format import to_json_compatible_object
from widget_bus_back.request_params import parse_bus_line_request_params
from widget_bus_back.local_time import LocalTime
from widget_bus_back.remote_api import RemoteApi
from widget_bus_back.bus_line import build_bus_line_combinations, BusLineSchedule

FETCH_PROCESSES = 4


class TheoreticalScheduleResource(Resource):
    def __init__(self):
        self.remote_api = RemoteApi()
        self.local_time = LocalTime()
        self.current_time = self.local_time.now()

    def get(self):
        request_params = parse_bus_line_request_params()
        bus_lines = build_bus_line_combinations(**request_params)
        schedules = self.fetch_schedules(bus_lines)
        return to_json_compatible_object(schedules)

    def fetch_schedules(self, bus_lines):
        pool = ThreadPool(FETCH_PROCESSES)
        schedules = pool.map(lambda l: self.fetch_schedule(l), list(bus_lines))
        pool.close()
        pool.join()
        return schedules

    def fetch_schedule(self, bus_line):
        try:
            remote_schedules = self.remote_api.fetch_theoretical_schedule(bus_line)
            return self.build_theoretical_schedule(bus_line, remote_schedules)
        except (KeyError, JSONDecodeError, RequestException) as e:
            return BusLineSchedule(bus_line=bus_line, error_message=e.__class__.__name__ + ':' + str(e))

    def build_theoretical_schedule(self, bus_line, remote_schedules):
        terminus = remote_schedules['ligne']['directionSens' + str(bus_line.direction)]
        next_arrival = remote_schedules['prochainsHoraires'][0]
        delay_to_next_arrival = self.compute_delay(next_arrival['heure'], next_arrival['passages'][0])
        return BusLineSchedule(bus_line, terminus, delay_to_next_arrival)

    def compute_delay(self, next_arrival_hour_string, next_arrival_minute_string):
        next_arrival_hour = extract_hour(next_arrival_hour_string)
        next_arrival_minute = int(next_arrival_minute_string)
        next_arrival = self.current_time.replace(hour=next_arrival_hour, minute=next_arrival_minute, second=0)
        self.local_time.localize(next_arrival)

        delay = next_arrival - self.current_time
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

