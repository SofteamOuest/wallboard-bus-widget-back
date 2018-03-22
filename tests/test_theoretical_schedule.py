from unittest import TestCase, main
from unittest.mock import patch, call
import sys
import bus_api
from widget_bus_back.bus_line import BusLine
from widget_bus_back.theoretical_schedule import TheoreticalScheduleResource


class TestTheoreticalScheduleResource(TestCase):
    def setUp(self):
        self.app = bus_api.app.test_client()

    def test_get_with_no_parameter_should_return_error(self):
        response = self.app.get('/theoretical')
        self.assertTrue('Missing required parameter' in response.get_data().decode(sys.getdefaultencoding()))

    def test_get_with_parameters_should_not_return_error(self):
        response = self.app.get('/theoretical?stop=A&line=1&line=2')
        self.assertFalse('Missing required parameter' in response.get_data().decode(sys.getdefaultencoding()))

    @patch('widget_bus_back.theoretical_schedule.RemoteApi')
    def test_get_with_three_lines_should_call_remote_api_thrice_times(self, mock_api):
        # arrange
        lines = [BusLine('foo', 'bar', i) for i in range(3)]

        # act
        TheoreticalScheduleResource().fetch_schedules(lines)

        # assert
        expected_calls = map(lambda x: call().fetch_theoretical_schedule(x), lines)
        mock_api.assert_has_calls(list(expected_calls))


if __name__ == '__main__':
    main()
