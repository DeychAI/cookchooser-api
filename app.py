from flask import Flask
from flask_restful import Api

from models import db
from v1.MealList import MealListAPI
from v1.Token import TokenAPI
from v1.User import UserAPI
from v1.UserList import UserListAPI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.cookchooser'
app.config['SECRET_KEY'] = 'cookchooser secret key'

db.init_app(app)

api = Api(app)

api.add_resource(UserListAPI, '/api/v1/users')
api.add_resource(TokenAPI, '/api/v1/token')
api.add_resource(MealListAPI, '/api/v1/meals')
api.add_resource(UserAPI, '/api/v1/users/<int:user_id>')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
