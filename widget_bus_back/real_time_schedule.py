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

        pool = ThreadPool(FETCH_PROCESSES)
        schedules = pool.map(lambda l: self.fetch_schedule(l), unique_stops)
        pool.close()
        pool.join()
        return schedules

    def fetch_schedule(self, stop):
        try:
            remote_schedules = self.remote_api.fetch_real_time_schedule(stop)
            return self.build_theoretical_schedule(remote_schedules)
        except RequestException as e:
            return BusLineSchedule(bus_line=BusLine(stop), error_message=e.__class__.__name__ + ':' + str(e))

    def build_theoretical_schedule(self, remote_schedules):
        return BusLineSchedule(BusLine('test'))
