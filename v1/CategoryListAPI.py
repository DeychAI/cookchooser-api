from flask.ext.restful import Resource, reqparse, abort, fields, marshal_with

from auth import auth
from models import Category, db

cat_fields = {
    'id': fields.Integer,
    'name': fields.String
}


class CategoryListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', required = 'True')
        super(CategoryListAPI, self).__init__()

    @marshal_with(cat_fields)
    def get(self):
        return Category.query.all()

    @marshal_with(cat_fields)
    def post(self):
        args = self.parser.parse_args()
        if Category.query.filter_by(name=args['name']).first() is not None:
            abort(400, message="Category already exists")
        cat = Category(name=args['name'])
        db.session.add(cat)
        db.session.commit()
        return cat, 201
