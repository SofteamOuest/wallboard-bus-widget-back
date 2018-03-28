import logging
import os
import requests


class RemoteApi:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api = os.getenv('WIDGET_BUS_API_URL', 'http://open_preprod.tan.fr/ewp')
        self.logger.info('WIDGET_BUS_API_URL %s', self.api)

    def fetch_theoretical_schedule(self, bus_line):
        url = self.build_theoretical_schedule_url(bus_line)
        r = requests.get(url)
        return r.json()

    def build_theoretical_schedule_url(self, bus_line):
        """For instance, http://open.tan.fr/ewp/horairesarret.json/IDNA/4/1"""
        return '{0}/horairesarret.json/{1}/{2}/{3}'.format(self.api, bus_line.stop, bus_line.line, bus_line.direction)
