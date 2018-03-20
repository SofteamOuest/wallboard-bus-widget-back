import itertools


class BusLine:
    def __init__(self, stop, line, direction):
        self.stop = stop
        self.line = line
        self.direction = direction


class BusLinePermutation:
    def __init__(self, stops = (), lines = (), directions = ()):
        self.__permutations = itertools.product(stops, lines, directions)

    @property
    def lines(self):
        for p in self.__permutations:
            yield BusLine(*p)