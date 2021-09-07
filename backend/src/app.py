import os
from flask import (
    Flask, request, abort, jsonify, render_template
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import (
    setup_db,
    user,
    order,
    pizza
)
from datetime import datetime, timedelta
import json

# General Specifications:

# Endpoints will include at least:
# 1- Two GET requests
# 2- One POST request
# 3- One PATCH request
# 4- One DELETE request

# Roles will include at least:
# 1- Two roles with different permissions
# 2- Permissions specified for all endpoints

# Tests will include at least:
# 1- One test for success behavior of each endpoint
# 2- One test for error behavior of each endpoint
# 3- At least two tests of RBAC for each role


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return render_template('index.html')

    # 1- Two GET requests
    @app.route('/pizza')
    def get_pizza():
        pizza_result = pizza.query.all()
        pizza_info = [p.information() for p in pizza_result]

        return jsonify({
            "success": True,
            "pizza": pizza_info
        }), 200

    @app.route('/orders')
    def get_orders():
        order_result = order.query.order_by(order.order_time.desc()).all()
        order_info = [o.information() for o in order_result]

        return jsonify({
            "success": True,
            "order": order_info
        }), 200

    # 2- One POST request

    @app.route('/users', methods=['POST'])
    def create_account():

        # create user object
        new_user = user(
            name=request.get_json().get('name'),
            address=request.get_json().get('address'),
            phone=request.get_json().get('phone')
        )

        try:
            new_user.insert()

        except:
            # send error
            abort(422)

        return jsonify({'success': True, 'user': [new_user.information()]}), 200

    @app.route('/pizza', methods=['POST'])
    def add_new_pizza():

        # create user object
        new_pizza = pizza(
            name=request.get_json().get('name'),
            price=request.get_json().get('price'),
            ingredients=request.get_json().get('ingredients')
        )

        try:
            new_pizza.insert()

        except:
            # send error
            abort(422)

        return jsonify({'success': True, 'pizza': [new_pizza.information()]}), 200

    @app.route('/orders', methods=['POST'])
    def create_orders():

        ordertime = datetime.datetime.now()
        pickuptime = ordertime + timedelta(minutes=45)
        formatted_ordertime = ordertime.isoformat()
        formatted_pickuptime = pickuptime.isoformat()

    # create order object
        new_order = order(
            pizza_id=request.get_json().get('pizza_id'),
            quantity=request.get_json().get('quantity'),
            order_time=json.dumps(formatted_ordertime),
            pickup_time=json.dumps(formatted_pickuptime)
        )

        try:
            new_order.insert()

        except:
            # send error
            abort(422)

        return jsonify({'success': True, 'order': [new_order.information()]}), 200

    # 3- One PATCH request
    @app.route('/pizza/<int:pizza_id>', methods=['PATCH'])
    def edit_pizza(pizza_id):

        # get spacific pizza by id
        pizza_result = pizza.query.filter(pizza.id == pizza_id).one_or_none()
        body = request.get_json()

        # send error if it not found
        if pizza_result is None:
            abort(404)

        if 'name' in body:
            pizza_result.name = request.get_json().get('name')

        elif 'price' in body:
            pizza_result.price = request.get_json().get('price')

        elif 'ingredients' in body:
            pizza_result.ingredients = request.get_json().get('ingredients')

        pizza_result.update()

        return jsonify({
            'success': True,
            'pizza': [p.information() for p in pizza_result]
        }), 200

    # 4- One DELETE request

    @app.route('/pizza/<int:pizza_id>', methods=['DELETE'])
    def delete_pizza(pizza_id):
        try:
            # delete pizza based on spacific id
            find_pizza = pizza.query.filter(
                pizza.id == pizza_id).one_or_none()

            find_pizza.delete()

            return jsonify({
                'success': True,
                'deleted': pizza_id
            }), 200

        except:
            abort(404)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
