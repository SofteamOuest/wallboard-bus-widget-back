import unittest

from widget_bus_back.bus_line import BusLinePermutation


class TestBusLinePermutation(unittest.TestCase):
    def test_simple_permutation_should_return_one_bus_line(self):
        p = BusLinePermutation(['A'], ['1'], [10])
        lines = list(p.lines)
        self.assertEquals(len(lines), 1)
        self.assertEquals(lines[0].stop, 'A')
        self.assertEquals(lines[0].line, '1')
        self.assertEquals(lines[0].direction, 10)

    def test_multiple_permutation_should_return_four_bus_lines(self):
        p = BusLinePermutation(['A'], ['C4', 'C5'], [1, 2])
        lines = list(p.lines)
        self.assertEquals(len(lines), 4)