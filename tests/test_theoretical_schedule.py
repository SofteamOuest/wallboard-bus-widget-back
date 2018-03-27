import unittest
from datetime import datetime

import sys
from unittest.mock import call, patch

import run
from widget_bus_back.bus_line import BusLine
from widget_bus_back.remote_api import RemoteApi
from widget_bus_back.theoretical_schedule import TheoreticalScheduleResource, build_theoretical_schedule, compute_delay


class TestTheoreticalScheduleResource(unittest.TestCase):
    def setUp(self):
        self.app = run.app.test_client()

    def test_get_with_no_parameter_should_return_error(self):
        # act
        response = self.app.get('/theoretical')

        # assert
        response_string = response.get_data().decode(sys.getdefaultencoding())
        self.assertTrue('missing required parameter' in response_string.lower())

    @patch.object(RemoteApi, 'fetch_theoretical_schedule', lambda _, __: {})
    def test_get_with_parameters_should_not_return_error(self):
        # act
        response = self.app.get('/theoretical?stop=A&line=1&line=2')

        # assert
        response_string = response.get_data().decode(sys.getdefaultencoding())
        self.assertFalse('server error' in response_string.lower())
        self.assertFalse('missing required parameter' in response_string.lower())

    @patch('widget_bus_back.theoretical_schedule.RemoteApi')
    def test_get_with_three_lines_should_call_remote_api_thrice_times(self, mock_api):
        # arrange
        lines = [BusLine('foo', 'bar', i) for i in range(3)]

        # act
        TheoreticalScheduleResource().fetch_schedules(lines)

        # assert
        expected_calls = map(lambda x: call().fetch_theoretical_schedule(x), lines)
        mock_api.assert_has_calls(list(expected_calls), any_order=True)

    def test_build_theoretical_schedule_should_compute_next_time(self):
        # arrange
        bus_line = BusLine('foo', 'bar', 1)
        now = datetime(2018, 1, 1, 14, 0, 0)
        remote_schedule = {
            "ligne": {
                "directionSens1": "Foch - Cathédrale",
                "directionSens2": "Porte de Vertou",
            },
            "prochainsHoraires": [
                {
                    "heure": "14h",
                    "passages": ["18"]
                },
                {
                    "heure": "14h",
                    "passages": ["33"]
                }]
        }

        # act
        sch = build_theoretical_schedule(bus_line, now, remote_schedule)

        # assert
        self.assertEquals(sch.line, bus_line.line)
        self.assertEquals(sch.stop, bus_line.stop)
        self.assertEquals(sch.direction, bus_line.direction)
        self.assertEquals(sch.terminus, "Foch - Cathédrale")
        self.assertEquals(sch.next, 18)

    @patch.object(RemoteApi, 'fetch_theoretical_schedule', lambda _, __: {})
    def test_fetch_schedule_when_unavailable_should_return_error(self):
        # arrange
        bus_line = BusLine('foo', 'bar', 1)

        # act
        sch = TheoreticalScheduleResource().fetch_schedule(bus_line)

        # assert
        self.assertTrue(sch.unavailable)
        self.assertTrue(sch.error_message)

    def test_compute_delay_in_the_incoming_hour(self):
        now = datetime(2018, 1, 1, 14, 0, 0)
        delay = compute_delay(now, '14h', '18')
        self.assertEquals(delay, 18)

    def test_compute_delay_in_the_next_hour(self):
        now = datetime(2018, 1, 1, 14, 0, 0)
        delay = compute_delay(now, '15h', '02')
        self.assertEquals(delay, 62)

    def test_compute_delay_in_the_next_day(self):
        now = datetime(2018, 1, 1, 23, 59, 0)
        delay = compute_delay(now, '0h', '05')
        self.assertEquals(delay, 6)


if __name__ == '__main__':
    unittest.main()
