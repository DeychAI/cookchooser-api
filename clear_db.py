# -*- coding: utf-8 -*-
import os
from app import app
from models import db, Category, Meal, User
import ast
import uuid
from v1.ColorLegendAPI import generate_default_legend

with app.app_context():
    db.drop_all()
    db.create_all()

    # Categories
    soup_cat = Category(name='Суп')
    meal_cat = Category(name='Горячее')
    salad_cat = Category(name='Салат')
    gar_cat = Category(name='Гарнир')
    db.session.add_all([soup_cat, meal_cat, salad_cat, gar_cat])
    db.session.commit()

    # User
    user = User('deigov@gmail.com')
    user.hash_password(os.environ.get('INIT_PASS') or '123')
    user.name = 'Сашко'
    db.session.add(user)
    db.session.commit()
    generate_default_legend(user.group)

    # Meals
    line = '["Блины","Буррито","Говядина жареная","Говядина с огурчиками","Говяжья отбивная с помидором","Гречка","Грибной суп","Гуляш","Индейка на пару","Индейка тушеная с помидорами","Картошка жареная с грибами","Колбаса кровяная","Колдуны","Котлеты","Куриная отбивная с ананасом","Куриная отбивные с помидором","Куриное филе в кисло-сладком соусе","Куриный суп","Курица жареная","Курица запеченая с яблоками","Курица на пару","Курица с помидорами тушеная","Макароны с фаршем и сливками","Манты","Мясной рулет с грибами и сыром","Мясо в горшочках","Окрошка","Омлет","Пельмени","Пирожки с сыром","Пирожки с фаршем","Пицца","Рассольник","Роллы","Рулетики лаваш с колбасой","Рулетики лаваш с рыбой","Рыба на пару","Рыбный суп с сайрой","Свекольник","Сердечки куриные жареные","Солянка","Сосиски","Суп гороховый с копченостями","Суп с фрикадельками","Сырный суп","Тефтели","Фаршированые перцы","Харчо"]'
    x = ast.literal_eval(line)
    for y in x:
        meal = Meal(name=y, category=meal_cat, group=user.group, uuid=str(uuid.uuid4()), revision=1, color='none')
        db.session.add(meal)
        db.session.commit()

    line = '["Греческий","Гречка","Зимний","Крабовый","Макароны с сыром","Морковь острая","Мясной с фасолью","Огурцы и помидоры","Огурцы, помидоры, горошек","Пюре","Свекольный с сыром","Селедка под шубой","Фасоль стручковая"]'
    x = ast.literal_eval(line)
    for y in x:
        meal = Meal(name=y, category=gar_cat, group=user.group, uuid=str(uuid.uuid4()), revision=1, color='none')
        db.session.add(meal)
        db.session.commit()
