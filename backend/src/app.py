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
#General Specifications:

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
  app = Flask(__name__, template_folder='templates')
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

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)