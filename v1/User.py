from flask.ext.restful import Resource, abort

from auth import auth
from models import User

class UserAPI(Resource):
    decorators = [auth.login_required]
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            abort(404, message="User not found!")
        return {'username': user.username}