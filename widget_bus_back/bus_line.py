import itertools


class BusLine:
    def __init__(self, stop, line, direction):
        self.stop = stop
        self.line = line
        self.direction = direction


def build_bus_line_combinations(stop=(), line=(), direction=()):
    cross_product_combinations = itertools.product(stop, line, direction)
    for cpc in cross_product_combinations:
        yield BusLine(*cpc)
