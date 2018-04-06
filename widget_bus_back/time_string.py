def extract_delay(next_arrival_minute_string):
    """Returns the value of delay string as an float
    >>> extract_delay('1 mn')
    1.0
    >>> extract_delay('5 mn')
    5.0
    >>> extract_delay('22 mn')
    22.0
    >>> extract_delay('1 mn 30')
    1.5
    >>> extract_delay('Proche')
    0.0
    >>> extract_delay('horaire.proche')
    0.0
    """
    if "proche" in next_arrival_minute_string.lower():
        return 0.0

    parts = split_next_arrival_minute_string(next_arrival_minute_string)
    return sum([value / (60 ** index) for index, value in enumerate(parts)])


def split_next_arrival_minute_string(next_arrival_minute_string):
    parts = next_arrival_minute_string.split('mn')
    for p in parts:
        part = p.strip()
        if len(part):
            yield int(part)


def extract_hour(hour_string):
    """Returns the value of hour string as an integer
    >>> extract_hour('14h')
    14
    >>> extract_hour('3h')
    3
    >>> extract_hour('10')
    10
    """
    return int(hour_string.rstrip('h'))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
