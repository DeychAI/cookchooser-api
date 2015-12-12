from flask.ext.restful import Resource, reqparse, abort

from auth import auth
from models import Category, db

class CategoryListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', required = 'True')
        super(CategoryListAPI, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        if Category.query.filter_by(name=args['name']).first() is not None:
            abort(400, message="Category already exists")
        cat = Category(name=args['name'])
        db.session.add(cat)
        db.session.commit()
        return { 'Category': cat.name, 'id': cat.id }, 201
