from datetime import datetime

import pytz


class LocalTime:
    def __init__(self):
        self.timezone = pytz.timezone('Europe/Paris')

    def localize(self, when):
        return self.timezone.normalize(when)

    def now(self):
        return pytz.utc.localize(datetime.utcnow()).astimezone(self.timezone)
