from flask import Flask
from flask_restful import Api
from flask_restful.utils import cors

from widget_bus_back.logging import configure_logging
from widget_bus_back.real_time_schedule import RealTimeScheduleResource
from widget_bus_back.theoretical_schedule import TheoreticalScheduleResource

app = Flask(__name__)
api = Api(app)
api.decorators = [cors.crossdomain(origin='*')]

api.add_resource(TheoreticalScheduleResource, '/theoretical')
api.add_resource(RealTimeScheduleResource, '/real-time')


def main():
    configure_logging()
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
