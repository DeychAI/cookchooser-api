from flask.ext.restful import Resource, fields, marshal, marshal_with, reqparse, abort
from flask import g
from auth import auth
from models import Meal, Category, db

cat_fields = {
    'id': fields.Integer
}

meal_fields = {
    'uuid': fields.String,
    'name': fields.String,
    'category_id': fields.Integer,
    'group': fields.String,
    'revision': fields.Integer,
    'color': fields.String,
    'image': fields.String,
    'description': fields.String
}

post_parser = reqparse.RequestParser()
post_parser.add_argument('uuid', required='True')
post_parser.add_argument('name', required='True')
post_parser.add_argument('category_id', required='True')
post_parser.add_argument('revision', required='True')
post_parser.add_argument('color', required='True')
post_parser.add_argument('image')
post_parser.add_argument('description')

get_parser = reqparse.RequestParser()
get_parser.add_argument('cat')

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('revision', required='True')


class MealsListAPI(Resource):
    decorators = [auth.login_required]

    @marshal_with(meal_fields)
    def post(self):
        args = post_parser.parse_args()
        meal = Meal.query.filter_by(uuid=args['uuid']).first()
        if meal is not None:
            abort(409, message='Meal already exists')

        meal = Meal(name=args['name'],
                    group=g.user.group,
                    category_id=args['category_id'],
                    uuid=args['uuid'],
                    revision=1,
                    color=args['color'],
                    image=args['image'],
                    description=args['description'])
        db.session.add(meal)
        db.session.commit()
        return meal, 201

    @marshal_with(meal_fields)
    def get(self):
        args = get_parser.parse_args()
        if args['cat'] is None:
            meals = Meal.query.filter_by(group=g.user.group).all()
        else:
            meals = Meal.query.filter_by(category_id=args['cat'], group=g.user.group).all()
        return meals


class MealAPI(Resource):
    decorators = [auth.login_required]

    @marshal_with(meal_fields)
    def get(self, uuid):
        meal = Meal.query.get_or_404(uuid)
        return meal

    @marshal_with(meal_fields)
    def put(self, uuid):
        args = post_parser.parse_args()
        meal = Meal.query.get_or_404(uuid)

        if meal.group != g.user.group:
            abort(403, message='Access denied')

        if meal.revision != int(args['revision']):
            abort(409, message='Wrong revision')

        meal.name = args['name']
        meal.category_id = args['category_id']
        meal.color = args['color']
        meal.image = args['image']
        meal.description = args['description']

        meal.revision += 1

        db.session.add(meal)
        db.session.commit()
        return meal

    def delete(self, uuid):
        args = delete_parser.parse_args()
        meal = Meal.query.get_or_404(uuid)

        if meal.group != g.user.group:
            abort(403, message='Access denied')

        if meal.revision != int(args['revision']):
            abort(409, message='Wrong revision')

        db.session.delete(meal)
        db.session.commit()
        return {'result': 'Meal deleted'}
