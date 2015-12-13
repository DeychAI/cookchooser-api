from flask.ext.restful import Resource, abort, fields, marshal, marshal_with
from flask import g

from auth import auth
from models import User

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'username': fields.String,
    'group': fields.String
}


class UserAPI(Resource):
    decorators = [auth.login_required]

    @marshal_with(user_fields)
    def get(self, user_id):
        if user_id != g.user.id:
            abort(403)
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            abort(404, message="User not found!")
        return user
