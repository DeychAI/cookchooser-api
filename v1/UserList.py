from flask.ext.restful import Resource, reqparse, abort

from models import User, db

class UserListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', required = 'True')
        self.parser.add_argument('password', required = 'True')
        super(UserListAPI, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        if User.query.filter_by(username=args['username']).first() is not None:
            abort(400, message="User already exists")

        user = User(args['username'])
        user.hash_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return { 'username': args['username'], 'id': user.id }, 201