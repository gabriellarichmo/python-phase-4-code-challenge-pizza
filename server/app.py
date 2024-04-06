#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


# @app.route("/")
# def index():
#     return "<h1>Code challenge</h1>"

class Restaurants(Resource):
    def get(self):
        try:
            restaurants = [restaurant.to_dict(only=("address", "id", "name")) for restaurant in Restaurant.query]
            return restaurants, 200
        except Exception:
            return {"error": "Restaurant not found"}, 404

class RestaurantById(Resource):
    def get(self, id):
        try:
            restaurant = db.session.get(Restaurant, id).to_dict()
            return restaurant, 200
        except Exception:
            return {"error": "Restaurant not found"}, 404

    def delete(self, id):
        try:
            restaurant = db.session.get(Restaurant, id)
            db.session.delete(restaurant)
            db.session.commit()
            return {}, 204
        except Exception:
            return {"error": "Restaurant not found"}, 404

class Pizzas(Resource):
    def get(self):
        try:
            pizzas = [pizza.to_dict(only=("id", "ingredients", "name")) for pizza in Pizza.query]
            return pizzas, 200
        except Exception:
            return {"error": "Pizza not found"}, 404

class RestaurantPizzas(Resource):
    def post(self):
        try:
            data = request.get_json()
            new_rp = RestaurantPizza(**data)
            db.session.add(new_rp)
            db.session.commit()
            return new_rp.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            # return {"error": str(e)}
            return {"errors": ["validation errors"]}, 400


api.add_resource(Restaurants, "/restaurants")
api.add_resource(RestaurantById, "/restaurants/<int:id>")
api.add_resource(Pizzas, "/pizzas")
api.add_resource(RestaurantPizzas, "/restaurant_pizzas")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
