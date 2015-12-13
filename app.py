import os
from flask import Flask
from flask_restful import Api

from models import db
from v1.MealsAPI import MealsListAPI, MealAPI
from v1.TokenAPI import TokenAPI
from v1.UserAPI import UserAPI
from v1.UserListAPI import UserListAPI
from v1.CategoryListAPI import CategoryListAPI
from v1.CategoryAPI import CategoryAPI
from v1.InvitesAPI import InvitesListAPI, InviteAPI
from v1.GroupAPI import GroupAPI


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.cookchooser'
app.config['SECRET_KEY'] = os.environ.get('COOKCHOOSER_KEY') or 'cookchooser secret key'
app.config['ERROR_404_HELP'] = False

db.init_app(app)

api = Api(app)

api.add_resource(UserListAPI, '/api/v1/users')
api.add_resource(TokenAPI, '/api/v1/token')
api.add_resource(MealsListAPI, '/api/v1/meals')
api.add_resource(MealAPI, '/api/v1/meals/<int:meal_id>')
api.add_resource(UserAPI, '/api/v1/users/<int:user_id>')
api.add_resource(CategoryListAPI, '/api/v1/categories')
api.add_resource(CategoryAPI, '/api/v1/categories/<int:cat_id>')
api.add_resource(InvitesListAPI, '/api/v1/invites')
api.add_resource(InviteAPI, '/api/v1/invites/<int:inv_id>')
api.add_resource(GroupAPI, '/api/v1/group')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
