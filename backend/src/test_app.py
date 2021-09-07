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

