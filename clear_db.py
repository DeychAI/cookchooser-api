# -*- coding: utf-8 -*-

from app import app
from models import db, Category, Meal


with app.app_context():
   	db.drop_all()
   	db.create_all()

   	#Categories
   	meal_cat = Category(name=u'Блюдо')
	salad_cat = Category(name=u'Салат или гарнир')
	db.session.add_all([meal_cat, salad_cat])
	db.session.commit()