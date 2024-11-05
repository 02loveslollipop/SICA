"""
This module implements a Flask application with various endpoints for managing users, products, sales, and providers.
It includes authentication and authorization mechanisms using tokens.
Endpoints:
-----------
- /login [POST]
    - Description: Authenticates a user and generates an access token.
    - Request Body: { "email": "user@example.com", "password": "password" }
    - Responses:
        - 200: { "token": "access_token" }
        - 400: { "error": "Invalid request" }
        - 401: { "error": "Invalid credentials" }
        - 500: { "error": "Internal server error" }
- /logout [POST]
    - Description: Logs out a user by invalidating the access token.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: { "message": "Logged out" }
        - 400: { "error": "Token not found" }
        - 401: { "error": "Token not in session" }
        - 500: { "error": "Internal server error" }
- /product [GET]
    - Description: Retrieves a list of products.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: List of products
        - 500: { "error": "Internal server error" }
- /product [POST]
    - Description: Adds a new product.
    - Headers: { "X-Access-Token": "access_token" }
    - Request Body: { "name": "Product Name", "description": "Product Description", "category": "Category", "price": 100.0, "status": "Available", "quantity": 10 }
    - Responses:
        - 201: { "message": "Product added" }
        - 400: { "error": "Invalid request" }
        - 500: { "error": "Internal server error" }
- /product/<id> [GET]
    - Description: Retrieves a product by its ID.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: Product details
        - 404: { "error": "Product not found" }
        - 500: { "error": "Internal server error" }
- /product/<id> [PUT]
    - Description: Updates a product by its ID.
    - Headers: { "X-Access-Token": "access_token" }
    - Request Body: { "name": "Product Name", "description": "Product Description", "category": "Category", "price": 100.0, "status": "Available", "quantity": 10 }
    - Responses:
        - 200: { "message": "Product updated" }
        - 400: { "error": "Invalid request" }
        - 404: { "error": "Product not found" }
        - 500: { "error": "Internal server error" }
- /product/<id> [DELETE]
    - Description: Deletes a product by its ID.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: { "message": "Product deleted" }
        - 404: { "error": "Product not found" }
        - 500: { "error": "Internal server error" }
- /sale [GET]
    - Description: Retrieves a list of sales.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: List of sales
        - 500: { "error": "Internal server error" }
- /sale [POST]
    - Description: Generates a new sale.
    - Headers: { "X-Access-Token": "access_token" }
    - Request Body: { "id_seller": "seller_id", "id_client": "client_id", "products": ["product_id1", "product_id2"], "date": "YYYY-MM-DD HH:MM:SS" }
    - Responses:
        - 201: { "message": "Sale generated" }
        - 400: { "error": "Invalid request" }
        - 500: { "error": "Internal server error" }
- /sale/date [GET]
    - Description: Retrieves sales within a date range.
    - Headers: { "X-Access-Token": "access_token" }
    - Query Parameters: dateLo, dateHi
    - Responses:
        - 200: List of sales within the date range
        - 400: { "error": "Could not parse dates from request" }
        - 500: { "error": "Internal server error" }
- /sale/product/<id> [GET]
    - Description: Retrieves sales for a specific product.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: List of sales for the product
        - 500: { "error": "Internal server error" }
- /sale/user/<id> [GET]
    - Description: Retrieves sales for a specific user.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: List of sales for the user
        - 500: { "error": "Internal server error" }
- /provider [GET]
    - Description: Retrieves a list of providers.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: List of providers
        - 500: { "error": "Internal server error" }
- /provider [POST]
    - Description: Adds a new provider.
    - Headers: { "X-Access-Token": "access_token" }
    - Request Body: { "name": "Provider Name", "address": "Provider Address" }
    - Responses:
        - 201: { "message": "Provider added" }
        - 400: { "error": "Invalid request" }
        - 500: { "error": "Internal server error" }
- /provider/<id> [GET]
    - Description: Retrieves a provider by its ID.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: Provider details
        - 404: { "error": "Provider not found" }
        - 500: { "error": "Internal server error" }
- /provider/<id> [PUT]
    - Description: Updates a provider by its ID.
    - Headers: { "X-Access-Token": "access_token" }
    - Request Body: { "name": "Provider Name", "address": "Provider Address" }
    - Responses:
        - 200: { "message": "Provider updated" }
        - 400: { "error": "Invalid request" }
        - 404: { "error": "Provider not found" }
        - 500: { "error": "Internal server error" }
- /provider/<id> [DELETE]
    - Description: Deletes a provider by its ID.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: { "message": "Provider deleted" }
        - 404: { "error": "Provider not found" }
        - 500: { "error": "Internal server error" }
- /user [GET]
    - Description: Retrieves a list of users.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: List of users
        - 500: { "error": "Internal server error" }
- /user [POST]
    - Description: Adds a new user.
    - Headers: { "X-Access-Token": "access_token" }
    - Request Body: { "name": "User Name", "lastname": "User Lastname", "email": "user@example.com", "cellphone": "1234567890", "password": "password", "role": "role" }
    - Responses:
        - 201: { "message": "User added" }
        - 400: { "error": "Invalid request" }
        - 500: { "error": "Internal server error" }
- /user/<id> [GET]
    - Description: Retrieves a user by its ID.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: User details
        - 404: { "error": "User not found" }
        - 500: { "error": "Internal server error" }
- /user/<id> [PUT]
    - Description: Updates a user by its ID.
    - Headers: { "X-Access-Token": "access_token" }
    - Request Body: { "name": "User Name", "lastname": "User Lastname", "email": "user@example.com", "cellphone": "1234567890", "password": "password", "role": "role" }
    - Responses:
        - 200: { "message": "User updated" }
        - 400: { "error": "Invalid request" }
        - 404: { "error": "User not found" }
        - 500: { "error": "Internal server error" }
- /user/<id> [DELETE]
    - Description: Deletes a user by its ID.
    - Headers: { "X-Access-Token": "access_token" }
    - Responses:
        - 200: { "message": "User deleted" }
        - 404: { "error": "User not found" }
        - 500: { "error": "Internal server error" }
"""
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
from redis import Redis
from datetime import datetime
import hashlib
from functools import wraps
from exceptions import *
from saleHandler import SaleHandler
from userHandler import UserHandler
from productHandler import ProductHandler
from loginHandler import LoginHandler
from tokenHandler import TokenHandler
from providerHandler import ProviderHandler
from login import Login
from user import User
from product import Product
from secret import Secret
from provider import Provider
from flasgger import Swagger

template = {
  "info": {
    "title": "SICA-API",
    "description": "Backend of SICA",
    "version": "1.0.0",
    "contact": {
        "email": "support@02loveslollipop.uk",
        "url": "https://github.com/02loveslollipop"
    },
    "host": "sica.02loveslollipop.uk"    
  }
}

app = Flask(__name__)
cors = CORS(app)
config = Secret()
mongo = MongoClient(config.uri)
saleHandler = SaleHandler(config.dbName, connection=mongo)
providerHandler = ProviderHandler(config.dbName, connection=mongo)
userHandler = UserHandler(config.dbName, connection=mongo)
productHandler = ProductHandler(config.dbName, connection=mongo)
loginHandler = LoginHandler(config.dbName, connection=mongo)
tokenHandler = TokenHandler(config.token_ttl, config.secret, mongo, config.dbName)
swagger = Swagger(app, template=template)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers['X-Access-Token']
            if token is None:
                return jsonify({'error': 'Token not found'}), 400
            
            if not loginHandler.authToken(token):
                return jsonify({'error': 'Invalid token'}), 401
        except KeyError:
            return jsonify({'error': 'Token not found'}), 400
        except ExpiredTokenException:
            return jsonify({'error': 'Token expired'}), 418
        except TokenNotInSessionException:
            return jsonify({'error': 'Token not in session'}), 401
        return f(*args, **kwargs)
    return wrapper

# Login endpoints

@app.route('/login', methods=['POST'])
def login():
    """Login endpoint.
    ---
    parameters:
        -   in: body
            name: body
            required: true
            type: JSON
            schema:
                $ref: '#/definitions/Login'
            example:
                email: admin@test.com
                password: admin     
    definitions:
        Login:
            type: object
            properties:
                email:
                    type: string
                    description: User email
                    example: admin@test.com
                password:
                    type: string
                    description: User password
                    example: admin
    responses:
        200:
            description: User logged in
            schema:
            type: object
            properties:
                token:
                type: string
                description: Access token
            example:
                token: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        400:
            description: Invalid request
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Invalid request
        401:
            description: Invalid credentials
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Invalid credentials
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error   
    """
    try:
        data = request.json
        login = Login(data['email'], data['password'])
        if loginHandler.login(login):
            response = tokenHandler.generate(data['email'])
            return jsonify(response), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    except KeyError:
        return jsonify({'error': 'Invalid request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout endpoint.
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
    responses:
        200:
            description: User logged out
            schema:
            type: object
            properties:
                message:
                type: string
                description: Message
            example:
                message: Logged out
        400:
            description: Token not found
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Token not found
        401:
            description: Token not in session
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Token not in session
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        token = request.headers['X-Access-Token']
        tokenHandler.delete(token)
        return jsonify({'message': 'Logged out'}), 200
    except KeyError:
        return jsonify({'error': 'Token not found'}), 400
    except TokenNotInSessionException:
        return jsonify({'error': 'Token not in session'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Product endpoints

@app.route('/product', methods=['GET'])
@login_required
def getProducts():
    """Get all products
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
    definitions:
        Product:
            type: object
            properties:
                name:
                    type: string
                    description: Product name
                    example: Product Name
                description:
                    type: string
                    description: Product description
                    example: Product Description
                category:
                    type: string
                    description: Product category
                    example: Category
                price:
                    type: number
                    description: Product price
                    example: 100.0
                status:
                    type: string
                    description: Product status
                    example: Available
                quantity:
                    type: integer
                    description: Product quantity
                    example: 10
    responses:
        200:
            description: List of products
            schema:
            type: array
            items:
                $ref: '#/definitions/Product'
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        products = productHandler.getProducts()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/product', methods=['POST'])
@login_required
def addProduct():
    """Add a new product
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: body
            name: body
            required: true
            type: JSON
            schema:
                $ref: '#/definitions/Product'
            example:
                name: Product Name
                description: Product Description
                category: Category
                price: 100.0
                status: Available
                quantity: 10
    responses:
        201:
            description: Product added
            schema:
            type: object
            properties:
                message:
                type: string
                description: Message
            example:
                message: Product added
        400:
            description: Invalid request
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Invalid request
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        category = data.get('category')
        price = data.get('price')
        status = data.get('status')
        quantity = data.get('quantity')
        product = Product(name, description, category, price, status, quantity)
        productHandler.addProduct(product)
        return jsonify({'message': 'Product added'}), 201
    except ValueError:
        return jsonify({'error': 'Invalid request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/product/<id>', methods=['GET'])
@login_required
def getProduct(id):
    """Get a product by ID
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: path
            name: id
            required: true
            type: string
            description: Product ID
            example: 60b2b3b9d9c1b6f5f7e8f7b4
    responses:
        200:
            description: Product details
            schema:
            $ref: '#/definitions/Product'
        404:
            description: Product not found
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Product not found
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        product = productHandler.getProductByID(id)
        return jsonify(product), 200
    except ProductNotFoundException:
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/product/<id>', methods=['PUT'])
@login_required
def updateProduct(id):
    """
    Update a product by ID
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: path
            name: id
            required: true
            type: string
            description: Product ID
            example: 60b2b3b9d9c1b6f5f7e8f7b4
        -   in: body
            name: body
            required: true
            type: JSON
            schema:
                $ref: '#/definitions/Product'
            example:
                name: Product Name
                description: Product Description
                category: Category
                price: 100.0
                status: Available
                quantity: 10
    """
    try:
        data = request.json
        currentData = mongo[config.mongo_db].products.find_one({'_id': ObjectId(id)})
        if currentData is None:
            return jsonify({'error': 'Product not found'}), 404
        if name := data.get('name') is None:
            name = currentData['name']
        if description := data.get('description') is None:
            description = currentData['description']
        if category := data.get('category') is None:
            category = currentData['category']
        if price := data.get('price') is None:
            price = currentData['price']
        if status := data.get('status') is None:
            status = currentData['status']
        if quantity := data.get('quantity') is None:
            quantity = currentData['quantity']
        product = Product(name, description, category, price, status, quantity)
        productHandler.updateProduct(id, product)
        return jsonify({'message': 'Product updated'}), 200
    except ValueError:
        return jsonify({'error': 'Invalid request'}), 400
    except ProductNotFoundException:
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/product/<id>', methods=['DELETE'])
@login_required
def deleteProduct(id):
    """Delete a product by ID
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: path
            name: id
            required: true
            type: string
            description: Product ID
            example: 60b2b3b9d9c1b6f5f7
    responses:
        200:
            description: Product deleted
            schema:
            type: object
            properties:
                message:
                type: string
                description: Message
            example:
                message: Product deleted
        404:
            description: Product not found
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Product not found
    """
    try:
        productHandler.deleteProduct(id)
        return jsonify({'message': 'Product deleted'}), 200
    except ProductNotFoundException:
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Inventory endpoints TODO: check if this will be implemented

# Sales endpoints

@app.route('/sale', methods=['GET'])
@login_required
def getSales():
    """Get all sales
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
    definitions:
        Sale:
            type: object
            properties:
                id_seller:
                    type: string
                    description: Seller ID
                    example: 60b2b3b9d9c1b6f5f7e8f7b4
                id_client:
                    type: string
                    description: Client ID
                    example: 60b2b3b9d9c1b6f5f7e8f7b4
                products:
                    type: array
                    description: List of products
                    items:
                        type: object
                        properties:
                            idProducto:
                                type: string
                                description: Product ID
                                example: 60b2b3b9d9c1b6f5f7e8f7b4
                            quantity:
                                type: integer
                                description: Product quantity
                                example: 10
                date:
                    type: string
                    description: Sale date
                    example: 2021-05-29 12:00:00
                total:
                    type: number
                    description: Sale total
                    example: 100.0
    responses:
        200:
            description: List of sales
            schema:
            type: array
            items:
                $ref: '#/definitions/Sale'
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        sales = saleHandler.getSales()
        return jsonify(sales), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/sale', methods=['POST'])
@login_required
def generateSale():
    """Create a new sale
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: body
            name: body
            required: true
            type: JSON
            schema:
                $ref: '#/definitions/Sale'
            example:
                id_seller: 60b2b3b9d9c1b6f5f7e8f7b4
                id_client: 60b2b3b9d9c1b6f5f7e8f7b4
                products: [{"idProducto": "60b2b3b9d9c1b6f5f7e8f7b4", "quantity": 10}]
                date: 2024-11-04 12:00:00
    responses:
        201:
            description: Sale generated
            schema:
            type: object
            properties:
                message:
                type: string
                description: Message
            example:
                message: Sale generated
        400:
            description: Invalid request
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Invalid request
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        data = request.get_json()
        id_seller = data.get('id_seller')
        id_client = data.get('id_client')
        products = data.get('products')
        if date := data.get('date') is None:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        saleHandler.makeSale(id_seller, id_client, products, date)
        return jsonify({'message': 'Sale generated'}), 201
    except ValueError:
        return jsonify({'error': 'Invalid request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/sale/date', methods=['GET'])
@login_required
def getSalesByDate():
    """Get sales within a date range
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: query
            name: dateLo
            required: true
            type: string
            description: Lower date limit
            example: 2021-05-29
        -   in: query
            name: dateHi
            required: true
            type: string
            description: Upper date limit
            example: 2021-05-30
    responses:
        200:
            description: List of sales within the date range
            schema:
            type: array
            items:
                $ref: '#/definitions/Sale'
        400:
            description: Could not parse dates from request
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Could not parse dates from request
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        dateLo = request.args.get('dateLo')
        dateHi = request.args.get('dateHi')
        sales = saleHandler.getSalesByDate(dateLo, dateHi)
        return jsonify(sales), 200
    except ValueError:
        return jsonify({'error': 'Could not parse dates from request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sale/product/<id>', methods=['GET'])
@login_required
def getSalesByProduct(id):
    """Get sales for a specific product
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: path
            name: id
            required: true
            type: string
            description: Product ID
            example: 60b2b3b9d9c1b6f5f7e8f7b4
    responses:
        200:
            description: List of sales for the product
            schema:
            type: array
            items:
                $ref: '#/definitions/Sale'
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        result = saleHandler.getSaleByProduct(id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/sale/user/<id>', methods=['GET'])
@login_required
def getSalesByUser(id):
    """Get sales for a specific user
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: path
            name: id
            required: true
            type: string
            description: User ID
            example: 60b2b3b9d9c1b6f5f7e8f7b4
    responses:
        200:
            description: List of sales for the user
            schema:
            type: array
            items:
                $ref: '#/definitions/Sale'
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        sales = saleHandler.getSalesByUser(id)
        return jsonify(sales), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Provider endpoints

@app.route('/provider', methods=['GET'])
@login_required
def getProviders():
    """
    Get all providers
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
    definitions:
        Provider:
            type: object
            properties:
                name:
                    type: string
                    description: Provider name
                    example: Provider Name
                address:
                    type: string
                    description: Provider address
                    example: Provider Address
    responses:
        200:
            description: List of providers
            schema:
            type: array
            items:
                $ref: '#/definitions/Provider'
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        providers = providerHandler.getProviders()
        return jsonify(providers), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/provider', methods=['POST'])
@login_required
def addProvider():
    """Create a new provider
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: body
            name: body
            required: true
            type: JSON
            schema:
                $ref: '#/definitions/Provider'
            example:
                name: Provider Name
                address: Provider Address
    responses:
        201:
            description: Provider added
            schema:
            type: object
            properties:
                message:
                type: string
                description: Message
            example:
                message: Provider added
        400:
            description: Invalid request
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Invalid request
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        data = request.get_json()
        name = data.get('name')
        address = data.get('address')
        provider = Provider(name, address)
        providerHandler.addProvider(provider)
        return jsonify({'message': 'Provider added'}), 201
    except ValueError:
        return jsonify({'error': 'Invalid request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/provider/<id>', methods=['GET'])
@login_required
def getProvider(id):
    """Get a provider by ID
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: path
            name: id
            required: true
            type: string
            description: Provider ID
            example: 60b2b3b9d9c1b6f5f7e8f7b4
    responses:
        200:
            description: Provider details
            schema:
            $ref: '#/definitions/Provider'
        404:
            description: Provider not found
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Provider not found
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        provider = providerHandler.getProviderByID(id)
        return jsonify(provider), 200
    except ProviderNotFoundException:
        return jsonify({'error': 'Provider not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/provider/<id>', methods=['PUT'])
@login_required
def updateProvider(id):
    """Update a provider by ID
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: path
            name: id
            required: true
            type: string
            description: Provider ID
            example: 60b2b3b9d9c1b6f5f7e8f7b4
        -   in: body
            name: body
            required: true
            type: JSON
            schema:
                $ref: '#/definitions/Provider'
            example:
                name: Provider Name
                address: Provider Address
    responses:
        200:
            description: Provider updated
            schema:
            type: object
            properties:
                message:
                type: string
                description: Message
            example:
                message: Provider updated
        400:
            description: Invalid request
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Invalid request
        404:
            description: Provider not found
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Provider not found
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        data = request.get_json()
        request = mongo[config.mongo_db].providers.find_one({'_id': ObjectId(id)})
        if request is None:
            return jsonify({'error': 'Provider not found'}), 404
        if name := data.get('name') is None:
            name = request['name']
        if address := data.get('address') is None:
            address = request['address']
        provider = Provider(name, address)
        providerHandler.updateProvider(id, provider)
        return jsonify({'message': 'Provider updated'}), 200
    except ValueError:
        return jsonify({'error': 'Invalid request'}), 400
    except ProviderNotFoundException:
        return jsonify({'error': 'Provider not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/provider/<id>', methods=['DELETE'])
@login_required
def deleteProvider(id):
    """"Delete a provider by ID
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: path
            name: id
            required: true
            type: string
            description: Provider ID
            example: 60b2b3b9d9c1b6f5f7e8f7b4
    responses:
        200:
            description: Provider deleted
            schema:
            type: object
            properties:
                message:
                type: string
                description: Message
            example:
                message: Provider deleted
        404:
            description: Provider not found
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Provider not found
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        providerHandler.deleteProvider(id)
        return jsonify({'message': 'Provider deleted'}), 200
    except ProviderNotFoundException:
        return jsonify({'error': 'Provider not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# User endpoints

@app.route('/user', methods=['GET'])
@login_required
def getUsers():
    """Get all users
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
    definitions:
        User:
            type: object
            properties:
                name:
                    type: string
                    description: User name
                    example: John
                lastname:
                    type: string
                    description: User lastname
                    example: Smith Paisa
                email:
                    type: string
                    description: User email
                    example: john.smith.paisa@test.com
                cellphone:
                    type: string
                    description: User cellphone
                    example: 1234567890
                role:
                    type: string
                    description: User role
                    enum: [admin, user]
                    example: admin
    responses:
        200:
            description: List of users
            schema:
            type: array
            items:
                $ref: '#/definitions/User'
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        users = userHandler.getUsers()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user', methods=['POST'])
@login_required
def addUser():
    """Create a new user
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: body
            name: body
            required: true
            type: JSON
            schema:
                $ref: '#/definitions/User'
            example:
                name: John
                lastname: Smith Paisa
                email: john.smith.paisa@test.com
                cellphone: 1234567890
                password: admin
                role: admin
    responses:
        201:
            description: User added
            schema:
            type: object
            properties:
                message:
                type: string
                description: Message
            example:
                message: User added
        400:
            description: Invalid request
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Invalid request
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        data = request.get_json()
        name = data.get('name')
        lastname = data.get('lastname')
        email = data.get('email')
        cellphone = data.get('cellphone')
        password = data.get('password')
        role = data.get('role')
        user = User(name, lastname, email, cellphone, password, role)
        userHandler.addUser(user)
        return jsonify({'message': 'User added'}), 201
    except ValueError:
        return jsonify({'error': 'Invalid request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@app.route('/user/<id>', methods=['GET'])
@login_required
def getUser(id):
    """Get a user by ID
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: path
            name: id
            required: true
            type: string
            description: User ID
            example: 60b2b3b9d9c1b6f5f7e8f7b4
    responses:
        200:
            description: User details
            schema:
            $ref: '#/definitions/User'
        404:
            description: User not found
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: User not found
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        user = userHandler.getUserByID(id)
        return jsonify(user), 200
    except UserNotFoundException:
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/user/<id>', methods=['PUT'])
@login_required 
def updateUser(id):
    """Update a user by ID
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: path
            name: id
            required: true
            type: string
            description: User ID
            example: 60b2b3b9d9c1b6f5f7e8f7b4
        -   in: body
            name: body
            required: true
            type: JSON
            schema:
                $ref: '#/definitions/User'
            example:
                name: John
                lastname: Smith Paisa
                email: john.smith.paisa@test.com
    responses:
        200:
            description: User updated
            schema:
            type: object
            properties:
                message:
                type: string
                description: Message
            example:
                message: User updated
        404:
            description: User not found
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: User not found
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        currentData = mongo[config.mongo_db].users.find_one({'_id': ObjectId(id)})
        data = request.get_json()
        if currentData is None:
            return jsonify({'error': 'User not found'}), 404
        if name := data.get('name') is None:
            name = currentData['name']
        if lastname := data.get('lastname') is None:
            lastname = currentData['lastname']
        if email := data.get('email') is None:
            email = currentData['email']
        if cellphone := data.get('cellphone') is None:
            cellphone = currentData['cellphone']
        if password := data.get('password') is None:
            password = currentData['password']
        if role := data.get('role') is None:
            role = currentData['role']
        user = User(name, lastname, email, cellphone, password, role)
        userHandler.updateUser(id, user)
        return jsonify({'message': 'User updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<id>', methods=['DELETE'])
@login_required
def deleteUser(id):
    """
    Delete a user by ID
    ---
    parameters:
        -   in: header
            name: X-Access-Token
            required: true
            type: string
            description: Access token
            example: d2bd959809159bc15e26de7a01e7e58750bf8537b9381b32069d6e2017310d57
        -   in: path
            name: id
            required: true
            type: string
            description: User ID
            example: 60b2b3b9d9c1b6f5f7e8f7b4
    responses:
        200:
            description: User deleted
            schema:
            type: object
            properties:
                message:
                type: string
                description: Message
            example:
                message: User deleted
        404:
            description: User not found
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: User not found
        500:
            description: Internal server error
            schema:
            type: object
            properties:
                error:
                type: string
                description: Error message
            example:
                error: Internal server error
    """
    try:
        userHandler.deleteUser(id)
        return jsonify({'message': 'User deleted'}), 200
    except UserNotFoundException:
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#add root endpoint so Cloudflare is happy
@app.route('/')
def root():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SICA API</title>
    </head>
    <body>

        <h1>SICA API</h1>
        <p>the EC2 is working and the api is available. Hopefully...</p>

        <iframe style="position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;" src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1&controls=0&mute=0" title="YouTube video player" frameborder="0" allow="autoplay" allowfullscreen></iframe>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Running in dev mode')
        app.run(host='0.0.0.0', port=5000, debug=True)
    elif sys.argv[1] == 'https':
        print('Running dev with https')
        app.run(host='0.0.0.0' , port=443, ssl_context='adhoc', debug=True)
    elif sys.argv[1] == 'prod':
        print('Running in production mode')
        app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))
    elif len(sys.argv) == 3 and sys.argv[1] == 'test':
        port = int(sys.argv[2])
        print(f'Running in production test at port {port}')
        app.run(host='0.0.0.0', port=port, ssl_context=('cert.pem', 'key.pem'))
    else:
        print('Running in dev mode')
        app.run(host='0.0.0.0', port=5000)
