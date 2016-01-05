from flask.ext.restful import Resource, reqparse, abort, fields, marshal_with
from auth import auth
from models import ColorLegend, db
from flask import g

colors = ['none', 'red', 'green', 'blue', 'orange']
default_legend = ['Все блюда', 'Красная метка', 'Зеленая метка', 'Синяя метка', 'Оранжевая метка']

post_parser = reqparse.RequestParser()
for color in colors:
    post_parser.add_argument(color, required='True')


def generate_default_legend(group):
    for color, desc in zip(colors, default_legend):
        item = ColorLegend(group=group, color=color, legend=desc)
        db.session.add(item)
        db.session.commit()


class ColorLegendAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        legends = ColorLegend.query.filter_by(group=g.user.group).all()
        result = {}
        for legend in legends:
            result[legend.color] = legend.legend

        return result

    def post(self):
        args = post_parser.parse_args()
        result = {}
        for col in colors:
            item = ColorLegend.query.filter_by(group=g.user.group, color=col).first()

            if item is None:
                abort(404, message="This color not exists")

            item.legend = args[col]
            db.session.add(item)
            db.session.commit()
            result[col] = item.legend

        return result
