# Pizza Resturant

# Geting Started: 

# Backend
### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash

export FLASK_APP=app.py
export FLASK_ENV=development 
python -m flask run

```

# API Referance 
## Error Handling
- Error are returnes as JSON objects in the following format:
```bash
{
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }
```
- The API will return these error types when request fail: 
   - 400: Bad Request
   - 404: Not found
   - 422: unprocessable

## Endpoints 
#### GET /pizza

```bash
{
{
    "pizza": [
        {
            "id": 2,
            "ingredients": "Grilled Chicken breast, Onions, BBQ Sauce & Mozzarella",
            "name": "BBQ Chicken",
            "price": 50
        },
        {
            "id": 1,
            "ingredients": "San Marzano tomatoes, mozzarella cheese, fresh basil, salt",
            "name": "margherita",
            "price": 45
        }
    ],
    "success": true
}

```
#### GET /orders
```bash
{
    "order": [
        {
            "id": 2,
            "order_time": "09/06/2021, 15:00:00",
            "pickup_time": "09/06/2021, 15:30:00",
            "pizza_id": 1,
            "quantity": 3,
            "user_id": 1
        },
        {
            "id": 1,
            "order_time": "09/05/2021, 15:37:04",
            "pickup_time": "09/05/2021, 16:00:00",
            "pizza_id": 1,
            "quantity": 2,
            "user_id": 1
        }
    ],
    "success": true
}

```
#### GET /orders/<int:userid>
```bash
{
    "order": [
        {
            "id": 4,
            "order_time": "09/07/2021, 22:52:48",
            "pickup_time": "09/07/2021, 23:37:48",
            "pizza_id": 1,
            "quantity": 5,
            "user_id": 4
        }
    ],
    "success": true
}
```
#### POST /users
```bash
{
    "success": true,
    "user": [
        {
            "address": "albsaten",
            "email": "bayan@gmail.com",
            "id": 9,
            "name": "bayan",
            "phone": "0548673985"
        }
    ]
}
```

#### POST /pizza
```bash
{
    "pizza": [
        {
            "id": 5,
            "ingredients": "A Combination of Cheeses: 2 Layers of Mozzarella, Feta, American cheese, Oregano & Signature Tomato Sauce",
            "name": "Four Cheeses",
            "price": 30
        }
    ],
    "success": true
}
```

#### POST /orders/<int:user_id>/create
```bash
{
    "order": [
        {
            "id": 5,
            "order_time": "09/08/2021, 03:36:22",
            "pickup_time": "09/08/2021, 04:21:22",
            "pizza_id": 2,
            "quantity": 5,
            "user_id": 1
        }
    ],
    "success": true
}
```
#### PATCH /pizza/<int:pizza_id>
```bash
{
    "pizza": {
        "id": 5,
        "ingredients": "A Combination of Cheeses: 2 Layers of Mozzarella, Feta, American cheese, Oregano & Signature Tomato Sauce",
        "name": "Four Cheeses",
        "price": 40
    },
    "success": true
}
```
#### DELETE /pizza/<int:pizza_id>
```bash
{
    "deleted": 5,
    "success": true
}
```
## Testing
To run the tests, run
```
dropdb resturant_test
createdb resturant_test
psql resturant_test < resturant.psql
python test_app.py
```

