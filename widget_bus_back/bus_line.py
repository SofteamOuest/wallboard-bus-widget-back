import itertools


class BusLine(object):
    def __init__(self, stop, line=None, direction=None):
        self.stop = stop
        self.line = line
        self.direction = direction

    @property
    def key(self):
        return '{0}-{1}-{2}'.format(self.stop, self.line, self.direction)


class BusLineSchedule(BusLine):
    def __init__(self, bus_line, terminus='', next_arrivals=(), error_message=''):
        copy_attributes = vars(bus_line)
        super().__init__(**copy_attributes)
        self.terminus = terminus
        self.next_arrivals = next_arrivals
        if error_message:
            self.error_message = error_message
            self.unavailable = True


def build_bus_line_combinations(stop=(), line=(), direction=()):
    cross_product_combinations = itertools.product(stop, line, direction)
    for cpc in cross_product_combinations:
        yield BusLine(*cpc)


class BusLineScheduleAggregator:
    def __init__(self):
        self.items = {}

    def add(self, new_schedule):
        if not(new_schedule.key in self.items):
            self.items[new_schedule.key] = new_schedule
        else:
            self.items[new_schedule.key].next_arrivals.extend(new_schedule.next_arrivals)

    def values(self):
        return self.items.values()
