from flask import g
from flask.ext.restful import Resource

from auth import auth

class TokenAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        token = g.user.generate_auth_token()
        return { 'token': token.decode('ascii'), 'id': g.user.id }