import itertools


class BusLine:
    def __init__(self, stop, line, direction):
        self.stop = stop
        self.line = line
        self.direction = direction


def build_bus_line_combinations(stops=(), lines=(), directions=()):
    cross_product_combinations = itertools.product(stops, lines, directions)
    for cpc in cross_product_combinations:
        yield BusLine(*cpc)
