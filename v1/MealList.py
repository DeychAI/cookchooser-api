from flask.ext.restful import Resource, fields, marshal, marshal_with, reqparse

from auth import auth
from models import Meal, Category, db

cat_fields = {
    'id': fields.Integer
}

meal_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'category_id': fields.Integer
}

class MealListAPI(Resource):
    #decorators = [auth.login_required]
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('name', required='True')
        self.post_parser.add_argument('group', required='True')
        self.post_parser.add_argument('category_id', required='True')
        self.post_parser.add_argument('client_id', required='True')

        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('cat')
        super(MealListAPI, self).__init__()

    #def post(self):

    @marshal_with(meal_fields)
    def get(self):
        args = self.get_parser.parse_args()
        if args['cat'] is None:
            meals = Meal.query.all()
        else:
            meals = Meal.query.filter_by(category_id=args['cat']).all()
        return meals
