import sys
import unittest
from unittest.mock import patch, call

import requests

import run
from widget_bus_back.real_time_schedule import RealTimeScheduleResource, build_real_time_schedule, \
    build_real_time_schedules
from widget_bus_back.remote_api import RemoteApi


class TestRealTimeScheduleResource(unittest.TestCase):
    def setUp(self):
        self.app = run.app.test_client()

    def test_get_with_no_parameter_should_return_error(self):
        # act
        response = self.app.get('/real_time')

        # assert
        response_string = response.get_data().decode(sys.getdefaultencoding())
        self.assertTrue('missing required parameter' in response_string.lower())

    @patch.object(RemoteApi, 'fetch_real_time_schedule', lambda _, __: [])
    def test_get_with_parameters_should_not_return_error(self):
        # act
        response = self.app.get('/real_time?stop=A')

        # assert
        response_string = response.get_data().decode(sys.getdefaultencoding())
        self.assertFalse('server error' in response_string.lower())
        self.assertFalse('missing required parameter' in response_string.lower())

    @patch('widget_bus_back.real_time_schedule.RemoteApi')
    def test_get_with_three_stops_should_call_remote_api_thrice(self, mock_api):
        # arrange
        stops = ['foo', 'bar', 'baz']

        # act
        RealTimeScheduleResource().fetch_schedules(stops)

        # assert
        expected_calls = map(lambda x: call().fetch_real_time_schedule(x), stops)
        mock_api.assert_has_calls(list(expected_calls), any_order=True)

    def test_get_with_three_lines_same_stop_should_call_remote_api_once(self):
        with patch.object(RemoteApi, 'fetch_real_time_schedule', return_value={}) as mock_method:
            # arrange
            stops = ['foo', 'foo', 'foo']

            # act
            RealTimeScheduleResource().fetch_schedules(stops)

            # assert
            mock_method.assert_called_once_with('foo')

    @patch.object(RemoteApi, 'fetch_real_time_schedule', side_effect=requests.RequestException)
    def test_fetch_schedule_when_unavailable_should_return_error(self, __):
        # arrange
        stops = ['foo']

        # act
        sch = RealTimeScheduleResource().fetch_schedule(stops)

        # assert
        self.assertTrue(sch.unavailable)
        self.assertTrue(sch.error_message)

    def test_build_real_time_schedule_with_one_line_should_compute_next_time(self):
        # arrange
        stop = 'IDNA'
        remote_schedule = {
            "sens": 2,
            "terminus": "Porte de Vertou",
            "temps": "5 mn",
            "ligne": {
                "numLigne": "4",
            }
        }

        # act
        sch = build_real_time_schedule(stop, remote_schedule)

        # assert
        self.assertEqual(sch.stop, stop)
        self.assertEqual(sch.line, "4")
        self.assertEqual(sch.direction, 2)
        self.assertEqual(sch.terminus, "Porte de Vertou")
        self.assertEqual(sch.next_arrivals, [5])

    def test_build_real_time_schedules_with_two_lines_should_concat_results(self):
        # arrange
        stop = 'IDNA'
        remote_schedules = [{
                "sens": 2,
                "terminus": "Porte de Vertou",
                "temps": "1 mn",
                "ligne": {
                    "numLigne": "4",
                }
            },
            {
                "sens": 1,
                "terminus": "Quai des Antilles",
                "temps": "1 mn 30",
                "ligne": {
                    "numLigne": "C5",
                }
            }]

        # act
        sch = build_real_time_schedules(stop, remote_schedules)

        # assert
        self.assertEqual(len(sch), 2)

        self.assertEqual(sch[0].stop, stop)
        self.assertEqual(sch[0].line, "4")
        self.assertEqual(sch[0].direction, 2)
        self.assertEqual(sch[0].terminus, "Porte de Vertou")
        self.assertEqual(sch[0].next_arrivals, [1])

        self.assertEqual(sch[1].stop, stop)
        self.assertEqual(sch[1].line, "C5")
        self.assertEqual(sch[1].direction, 1)
        self.assertEqual(sch[1].terminus, "Quai des Antilles")
        self.assertEqual(sch[1].next_arrivals, [1.5])

    def test_build_real_time_schedules_with_one_line_two_schedules_should_aggregate_results(self):
        # arrange
        stop = 'IDNA'
        remote_schedules = [{
                "sens": 2,
                "terminus": "Porte de Vertou",
                "temps": "1 mn",
                "ligne": {
                    "numLigne": "4",
                }
            },
            {
                "sens": 2,
                "terminus": "Porte de Vertou",
                "temps": "2 mn 30",
                "ligne": {
                    "numLigne": "4",
                }
            }]

        # act
        sch = build_real_time_schedules(stop, remote_schedules)

        # assert
        self.assertEqual(len(sch), 1)

        self.assertEqual(sch[0].stop, stop)
        self.assertEqual(sch[0].line, "4")
        self.assertEqual(sch[0].direction, 2)
        self.assertEqual(sch[0].terminus, "Porte de Vertou")
        self.assertEqual(sch[0].next_arrivals, [1, 2.5])


if __name__ == '__main__':
    unittest.main()
