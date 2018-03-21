import unittest

from widget_bus_back.bus_line import build_bus_line_combinations


class TestBusLinePermutation(unittest.TestCase):
    def test_simple_permutation_should_return_one_bus_line(self):
        result = build_bus_line_combinations(['A'], ['1'], [10])
        lines = list(result)
        self.assertEquals(len(lines), 1)
        self.assertEquals(lines[0].stop, 'A')
        self.assertEquals(lines[0].line, '1')
        self.assertEquals(lines[0].direction, 10)

    def test_multiple_permutation_should_return_four_bus_lines(self):
        result = build_bus_line_combinations(['A'], ['C4', 'C5'], [1, 2])
        lines = list(result)
        self.assertEquals(len(lines), 4)


if __name__ == '__main__':
    unittest.main()
