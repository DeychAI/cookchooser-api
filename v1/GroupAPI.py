from flask.ext.restful import Resource, abort, fields, marshal_with, reqparse
from flask import g
from v1.UserAPI import user_fields
from auth import auth
from models import User


class GroupAPI(Resource):
    decorators = [auth.login_required]

    # get list of users in your group
    @marshal_with(user_fields)
    def get(self):
        return User.query.filter_by(group=g.user.group).all()
