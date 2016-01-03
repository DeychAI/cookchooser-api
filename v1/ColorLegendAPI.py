from flask.ext.restful import Resource, reqparse, abort, fields, marshal_with
from auth import auth
from models import ColorLegend, db

colors = ['none', 'red', 'green', 'blue', 'orange']


class ColorLegendAPI(Resource):
    decorators = [auth.login_required]
