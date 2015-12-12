from flask.ext.restful import Resource, abort

from auth import auth
from models import Category

class CategoryAPI(Resource):
	def get(self, cat_id):
		cat = Category.query.filter_by(id=cat_id).first()
		if cat is None:
			abort(404, message="Category not found!")
		return {'id': cat.id, 'name': cat.name}
