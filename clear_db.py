# -*- coding: utf-8 -*-
import os
from app import app
from models import db, Category, Meal, User
import ast
import uuid

with app.app_context():
    db.drop_all()
    db.create_all()

    # Categories
    meal_cat = Category(name='Блюдо')
    salad_cat = Category(name='Салат или гарнир')
    db.session.add_all([meal_cat, salad_cat])
    db.session.commit()

    # User
    user = User('deigov@gmail.com')
    user.hash_password(os.environ.get('INIT_PASS') or '123')
    user.name = 'Сашко'
    db.session.add(user)
    db.session.commit()

    # Meals
    line = '["Блины","Буррито","Говядина жареная","Говядина с огурчиками","Говяжья отбивная с помидором","Гречка","Грибной суп","Гуляш","Индейка на пару","Индейка тушеная с помидорами","Картошка жареная с грибами","Колбаса кровяная","Колдуны","Котлеты","Куриная отбивная с ананасом","Куриная отбивные с помидором","Куриный суп","Курица жареная","Курица запеченая с яблоками","Курица на пару","Курица с помидорами тушеная","Макароны с фаршем и сливками","Манты","Мясной рулет с грибами и сыром","Мясо в горшочках","Окрошка","Омлет","Пельмени","Пирожки с сыром","Пирожки с фаршем","Пицца","Рассольник","Роллы","Рулетики лаваш с колбасой","Рулетики лаваш с рыбой","Рыба на пару","Рыбный суп с сайрой","Свекольник","Сердечки куриные жареные","Солянка","Сосиски","Суп гороховый с копченостями","Суп с фрикадельками","Сырный суп","Тефтели","Фаршированые перцы","Харчо"]'
    x = ast.literal_eval(line)
    for y in x:
        meal = Meal(name=y, category=meal_cat, group=user.group, client_id=str(uuid.uuid4()), revision=1, color='none')
        db.session.add(meal)
        db.session.commit()

    line = '["Греческий","Гречка","Зимний","Крабовый","Макароны с сыром","Морковь острая","Мясной с фасолью","Огурцы и помидоры","Огурцы, помидоры, горошек","Пюре","Свекольный с сыром","Селедка под шубой","Фасоль стручковая"]'
    x = ast.literal_eval(line)
    for y in x:
        meal = Meal(name=y, category=salad_cat, group=user.group, client_id=str(uuid.uuid4()), revision=1, color='none')
        db.session.add(meal)
        db.session.commit()
