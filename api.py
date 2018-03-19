from flask import Flask
from flask_restful import Api
from flask_restful.utils import cors
from widget_bus_back.theoretical_schedule import TheoreticalSchedule
from widget_bus_back.real_time_schedule import RealTimeSchedule

app = Flask(__name__)
api = Api(app)
api.decorators = [cors.crossdomain(origin='*')]

api.add_resource(TheoreticalSchedule, '/theoretical')
api.add_resource(RealTimeSchedule, '/real-time')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
