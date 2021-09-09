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
from auth import AuthError, requires_auth

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

    # -------------------------------GET----------------------------------------------
    # get all pizza for (customers + manager)

    @app.route('/pizza')
    def get_pizza():
        pizza_result = pizza.query.all()
        pizza_info = [p.information() for p in pizza_result]

        return jsonify({
            "success": True,
            "pizza": pizza_info
        }), 200

    # view all order for manager
    @app.route('/orders')
    #@requires_auth('get:orders')
    def get_orders(payload):
        order_result = order.query.order_by(order.order_time.desc()).all()
        order_info = [o.information() for o in order_result]

        return jsonify({
            "success": True,
            "order": order_info
        }), 200

    # view order for spacific customer
    @app.route('/orders/<int:userid>')
    #@requires_auth('get:specific_orders')
    def get_spacific_orders(payload, userid):

        find_user = user.query.filter(user.id == userid).one_or_none()

        if find_user is None:
            abort(404)

        order_result = order.query.filter(
            order.user_id == userid).order_by(order.order_time.desc()).all()

        if order_result is None:
            abort(404)

        order_info = [o.information() for o in order_result]

        return jsonify({
            "success": True,
            "order": order_info
        }), 200

    # -------------------------------POST----------------------------------------------
    # create new account
    @app.route('/users', methods=['POST'])
    def create_account():

        body = request.get_json()

        if ('name' not in body) or ('email' not in body) or ('address' not in body) or ('phone' not in body):
            abort(422)

        # create user object
        new_user = user(
            name=request.get_json().get('name'),
            email=request.get_json().get('email'),
            address=request.get_json().get('address'),
            phone=request.get_json().get('phone')
        )

        new_user.insert()

        return jsonify({'success': True, 'user': [new_user.information()]}), 200

    # add new pizza by (Manager)
    @app.route('/pizza', methods=['POST'])
    #@requires_auth('post:pizza')
    def add_new_pizza(payload):

        body = request.get_json()
        if ('name' not in body) or ('price' not in body) or ('ingredients' not in body):
            abort(422)

        # create user object
        new_pizza = pizza(
            name=request.get_json().get('name'),
            price=request.get_json().get('price'),
            ingredients=request.get_json().get('ingredients')
        )

        new_pizza.insert()

        return jsonify({'success': True, 'pizza': [new_pizza.information()]}), 200

    # make order for (customers)
    @app.route('/orders/<int:user_id>/create', methods=['POST'])
    #@requires_auth('post:orders')
    def create_orders(payload, user_id):

        find_user = user.query.filter(user.id == user_id).one_or_none()

        if find_user is None:
            abort(404)

        body = request.get_json()
        if ('pizza_id' not in body) or ('quantity' not in body):
            abort(422)

        ordertime = datetime.now()
        pickuptime = ordertime + timedelta(minutes=45)
        formatted_ordertime = ordertime.isoformat()
        formatted_pickuptime = pickuptime.isoformat()

    # create order object
        new_order = order(
            user_id=json.dumps(user_id),
            pizza_id=request.get_json().get('pizza_id'),
            quantity=request.get_json().get('quantity'),
            order_time=json.dumps(formatted_ordertime),
            pickup_time=json.dumps(formatted_pickuptime)
        )

        new_order.insert()

        return jsonify({'success': True, 'order': [new_order.information()]}), 200

    # -------------------------------PATCH----------------------------------------------
    # Edit pizza details by (Manager)

    @app.route('/pizza/<int:pizza_id>', methods=['PATCH'])
    #@requires_auth('patch:pizza')
    def edit_pizza(payload, pizza_id):

        # get spacific pizza by id
        pizza_result = pizza.query.filter(pizza.id == pizza_id).one_or_none()

        # send error if it not found
        if pizza_result is None:
            abort(404)

        body = request.get_json()

        if 'name' in body:
            pizza_result.name = body.get('name')

        elif 'price' in body:
            pizza_result.price = body.get('price')

        elif 'ingredients' in body:
            pizza_result.ingredients = body.get('ingredients')

        pizza_result.update()

        return jsonify({
            'success': True,
            'pizza': pizza_result.information()
        }), 200

    # -------------------------------DELETE----------------------------------------------
    # Delete spacifi pizza by (Manager)

    @app.route('/pizza/<int:pizza_id>', methods=['DELETE'])
    #@requires_auth('delete:pizza')
    def delete_pizza(payload, pizza_id):
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

    @app.errorhandler(AuthError)
    def authentication_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error.get('description')
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
