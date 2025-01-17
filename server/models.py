from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    
    restaurantpizzas=db.relationship('RestaurantPizza',back_populates='restaurant',cascade='all,delete-orphan')
    pizzas=association_proxy('restaurantpizzas','Pizza',creator=lambda pizza_obj:RestaurantPizza(pizza=pizza_obj))
    
    serialize_rules=('-restaurantpizzas.restaurant',)
    
    

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    restaurantpizzas=db.relationship('RestaurantPizza',back_populates='pizza',cascade='all,delete-orphan')
    restaurants=association_proxy('restaurantpizzas','Restaurant',creator=lambda restaurant_obj:RestaurantPizza(restaurant=restaurant_obj))
    
    serialize_rules=('-restaurantpizzas.pizza',)
    

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    pizza_id=db.Column(db.Integer,db.ForeignKey('pizzas.id'))
    restaurant_id=db.Column(db.Integer,db.ForeignKey('restaurants.id'))
    
    pizza=db.relationship('Pizza',back_populates='restaurantpizzas')
    restaurant=db.relationship('Restaurant',back_populates='restaurantpizzas')
    
    serialize_rules=('-pizza.restaurantpizzas','-restaurant.restaurantpizzas')

    @validates('price')
    def validates_price(self,key,price):
        if price < 1 or price >30:
            raise ValueError('price entered must be between 1 - 30')
        return price

    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'
