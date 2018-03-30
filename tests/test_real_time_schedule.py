import unittest

import sys
from unittest.mock import patch, call

import requests

import run
from widget_bus_back.real_time_schedule import RealTimeScheduleResource
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

    @patch.object(RemoteApi, 'fetch_real_time_schedule', lambda _, __: {})
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


if __name__ == '__main__':
    unittest.main()
