from flask.ext.restful import Resource, reqparse, abort, marshal_with
from v1.UserAPI import user_fields
from models import User, db


class UserListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', required = 'True')
        self.parser.add_argument('password', required = 'True')
        self.parser.add_argument('name', required = 'True')
        super(UserListAPI, self).__init__()

    @marshal_with(user_fields)
    def post(self):
        args = self.parser.parse_args()
        if User.query.filter_by(username=args['username']).first() is not None:
            abort(400, message="User already exists")

        user = User(args['username'])
        user.hash_password(args['password'])
        user.name = args['name']
        db.session.add(user)
        db.session.commit()
        return user, 201
