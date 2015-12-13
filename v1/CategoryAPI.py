from flask.ext.restful import Resource, abort, fields, marshal_with, reqparse
from auth import auth
from models import Category, db
from v1.CategoryListAPI import cat_fields


class CategoryAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('name', required ='True')

        super(CategoryAPI, self).__init__()

    @marshal_with(cat_fields)
    def get(self, cat_id):
        cat = Category.query.filter_by(id=cat_id).first()
        if cat is None:
            abort(404, message="Category not found!")
        return cat

    @marshal_with(cat_fields)
    def put(self, cat_id):
        cat = Category.query.filter_by(id=cat_id).first()
        if cat is None:
            abort(404, message="Category not found!")
        args = self.put_parser.parse_args()
        cat.name = args['name']
        db.session.add(cat)
        db.session.commit()
        return cat

    def delete(self, cat_id):
        cat = Category.query.filter_by(id=cat_id).first()
        if cat is None:
            abort(404, message="Category not found!")
        db.session.delete(cat)
        db.session.commit()
        return {'result': 'Category deleted'}

