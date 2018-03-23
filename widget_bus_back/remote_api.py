from datetime import datetime, timedelta
from random import randint, seed


class RemoteApi:
    def __init__(self):
        seed()

    def fetch_theoretical_schedule(self, bus_line):
        now = datetime.now() + timedelta(minutes=randint(0, 10))

        return {
            "ligne": {
                "directionSens1": "Foch - Cathédrale",
                "directionSens2": "Porte de Vertou",
            },
            "prochainsHoraires": [
                {
                    "heure": str(now.hour) + 'h',
                    "passages": [str(now.minute)]
                }]
        }

