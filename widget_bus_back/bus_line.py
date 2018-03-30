import itertools


class BusLine(object):
    def __init__(self, stop, line=None, direction=None):
        self.stop = stop
        self.line = line
        self.direction = direction


class BusLineSchedule(BusLine):
    def __init__(self, bus_line, terminus='', next_time=-1, error_message=''):
        copy_attributes = vars(bus_line)
        super().__init__(**copy_attributes)
        self.terminus = terminus
        self.next = next_time
        if error_message:
            self.error_message = error_message
            self.unavailable = True


def build_bus_line_combinations(stop=(), line=(), direction=()):
    cross_product_combinations = itertools.product(stop, line, direction)
    for cpc in cross_product_combinations:
        yield BusLine(*cpc)
