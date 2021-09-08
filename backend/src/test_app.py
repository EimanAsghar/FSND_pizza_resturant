import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import (
    setup_db,
    user,
    order,
    pizza
)


class PizzaResturantTestCase(unittest.TestCase):
    """This class represents the pizza resturant test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "resturant_test"
        self.database_path = "postgresql://postgres:1998@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

# Tests will include at least:
# 1- One test for success behavior of each endpoint
# 2- One test for error behavior of each endpoint
# 3- At least two tests of RBAC for each role

    # Success for all pizza
    def test_get_all_pizza(self):
        res = self.client().get('/pizza')
        data = json.loads(res.data)
        # check the status code
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Error for all pizza




    # Success for all order
    def test_get_all_orders(self):
        res = self.client().get('/orders')
        data = json.loads(res.data)
        # check the status code
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Error for all order





    # Success for order of spacific customer
    def test_user_exist(self):
        res = self.client().get('/orders/1')

        data = json.loads(res.data)
        # check if the return values equal to these.
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    # error for order of spacific customer
    def test_user_does_not_exist(self):
        res = self.client().get('/orders/1000')

        data = json.loads(res.data)
        # check if the return values equal to these.
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    # Success for create account
    def test_create_new_account(self):
        res = self.client().post('/users', json={
            'name': 'Sara',
            'email':  'sara@gmail.com',
            'address': 'albsaten',
            'phone': '0548673985'
        })

        data = json.loads(res.data)
        # check the status code
        self.assertEqual(res.status_code, 200)

    # error for create account
    def test_create_account_not_allowed(self):

        # send bad request
        res = self.client().post('/users', json={})

        data = json.loads(res.data)
        # check the status code
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # Success for add new pizza 
    def test_add_new_pizza(self):
        res = self.client().post('/pizza', json={
            'name': 'Pepperoni',
            'price':  '45',
            'ingredients': 'Beef Pepperoni, Mozzarella & Signature Tomato Sauce',
        })

        data = json.loads(res.data)
        # check the status code
        self.assertEqual(res.status_code, 200)

    # error for add new pizza 
    def test_add_new_pizza_not_allowed(self):

        # send bad request
        res = self.client().post('/pizza', json={})

        data = json.loads(res.data)
        # check the status code
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')



 # Success for make new order
    def test_make_new_order(self):
        res = self.client().post('/orders/1/create', json={
            'pizza_id': '1',
            'quantity':  '4'
        })

        data = json.loads(res.data)
        # check the status code
        self.assertEqual(res.status_code, 200)

    # error for add new pizza 
    def test_make_new_order_not_allowed(self):

        # send bad request
        res = self.client().post('/orders/1/create', json={})

        data = json.loads(res.data)
        # check the status code
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    #Success for edit exist pizza
    def test_edit_exist_pizza(self):
        res = self.client().patch('/pizza/1')

        data = json.loads(res.data)
        # check if the return values equal to these.
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #error for edit exist pizza
    def test_edit_pizza_not_exist(self):
        res = self.client().patch('/pizza/1000')

        data = json.loads(res.data)
        # check if the return values equal to these.
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')


    # Success for delete pizza
    def test_delete_pizza(self):
        res = self.client().delete('/pizza/1')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # check if the return id equla to 1
        self.assertEqual(data['deleted'], 1)
        # find the pizza by id to check if it's deleted or not
        self.assertEqual(pizza.query.filter(
            pizza.id == 1).one_or_none(), None)

    # error for delete pizza
    def test_pizza_does_not_exist(self):
        res = self.client().delete('/pizza/1000')

        data = json.loads(res.data)
        # check if the return values equal to these.
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')



        