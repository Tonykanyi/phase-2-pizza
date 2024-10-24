#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api=Api(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class Restaurants(Resource):
    def get(self):
        restaurants=[]
        for restaurant in Restaurant.query.all():
            restaurant_dict={
                "address":restaurant.address,
                "id":restaurant.id,   
                "name":restaurant.name,
                
            }
            restaurants.append(restaurant_dict)
        return make_response(restaurants,200)

api.add_resource(Restaurants,'/restaurants')

class Restaurants_by_id(Resource):
    def get(self,id):
        restaurant=Restaurant.query.filter_by(id=id).first()
        
        if not restaurant:
            response_body={
                "error": "Restaurant not found"
            }
            return make_response(response_body,404)
        
        return make_response(restaurant.to_dict(),200)
    
    def delete(self,id):
        restaurant=Restaurant.query.filter_by(id=id).first()
        
        if not restaurant:
            response_body={
                "error": "Restaurant not found"
            }
            return make_response(response_body,400)
        
        db.session.delete(restaurant)
        db.session.commit()
        
        return make_response("",204)
        
api.add_resource(Restaurants_by_id,'/restaurants/<int:id>')

class Pizzas(Resource):
    def get (self):
        pizzas=[]
        for pizza in Pizza.query.all():
            pizza_dict={
                "id":pizza.id,
                "ingredients":pizza.ingredients,
                "name":pizza.name
            }
            pizzas.append(pizza_dict)
        
        return make_response(pizzas,200)
        
api.add_resource(Pizzas,'/pizzas')

class Restaurant_pizza(Resource):
    def post(self):
        data=request.get_json()
        price=data['price']
        pizza_id=data['pizza_id']
        restaurant_id=data['restaurant_id']
        
        if 1<= price <=30:
            restaurant_pizza=RestaurantPizza(price =price,pizza_id=pizza_id,restaurant_id=restaurant_id)
        
            if restaurant_pizza:
                db.session.add(restaurant_pizza)
                db.session.commit()
                restaurant_pizza_dict=restaurant_pizza.to_dict()
                return make_response(restaurant_pizza_dict,201)
        else:
            response_body={
                "errors": ["validation errors"]
            }
            return make_response(response_body,400)
    
api.add_resource(Restaurant_pizza,'/restaurant_pizzas')
        
        
        
        




if __name__ == '__main__':
    app.run(port=5555, debug=True)
