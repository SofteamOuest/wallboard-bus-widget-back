import logging

import os


def configure_logging():
    numeric_level = get_log_level()
    logging.basicConfig(level=numeric_level)


def get_log_level():
    log_level = os.getenv('WIDGET_BUS_LOG_LEVEL', 'INFO')
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    return numeric_level
