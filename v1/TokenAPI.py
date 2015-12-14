from flask import g
from flask.ext.restful import Resource, marshal
from v1.UserAPI import user_fields

from auth import auth


class TokenAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        token = g.user.generate_auth_token()
        return { 'token': token.decode('ascii'), 'user': marshal(g.user, user_fields)}