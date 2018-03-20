import unittest
import sys
import bus_api


class TestTheoreticalScheduleResource(unittest.TestCase):
    def setUp(self):
        self.app = bus_api.app.test_client()

    def test_get_with_no_parameter_should_return_error(self):
        response = self.app.get('/theoretical')
        self.assertTrue('Missing required parameter' in response.get_data().decode(sys.getdefaultencoding()))

    def test_get_with_parameters_should_not_return_error(self):
        response = self.app.get('/theoretical?stop=Aline=1&line&2')
        self.assertFalse('Missing required parameter' in response.get_data().decode(sys.getdefaultencoding()))


if __name__ == '__main__':
    unittest.main()
