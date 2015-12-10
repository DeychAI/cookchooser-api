from flask.ext.restful import Resource

from auth import auth

class MealListAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        return { 'data': 'Got it!' }