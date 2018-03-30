from flask_restful import reqparse


def parse_bus_line_request_params():
    parser = reqparse.RequestParser()
    parser.add_argument('stop', action='append', required=True)
    parser.add_argument('line', action='append', required=True)
    parser.add_argument('direction', action='append', type=int, default=[1, 2], choices=(1, 2))
    return parser.parse_args()


def parse_stop_request_params():
    parser = reqparse.RequestParser()
    parser.add_argument('stop', action='append', required=True)
    return parser.parse_args()

