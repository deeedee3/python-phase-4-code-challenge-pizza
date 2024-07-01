#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    try:
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    try:
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return jsonify(restaurant.to_dict()), 200
        else:
            return jsonify({"error": "Restaurant not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    try:
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        else:
            return jsonify({"error": "Restaurant not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    try:
        pizzas = Pizza.query.all()
        return jsonify([pizza.to_dict() for pizza in pizzas]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    try:
        if 'restaurant_id' not in data or 'pizza_id' not in data or 'price' not in data:
            raise ValueError("Missing restaurant_id, pizza_id or price")

        new_restaurant_pizza = RestaurantPizza(
            restaurant_id=data['restaurant_id'],
            pizza_id=data['pizza_id'],
            price=data['price']
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return jsonify(new_restaurant_pizza.to_dict()), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5555, debug=True)
