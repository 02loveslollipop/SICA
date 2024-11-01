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
from dashboard import Dashboard
from login import Login
from user import User
from product import Product
from secret import Secret
from provider import Provider

app = Flask(__name__)
cors = CORS(app)
config = Secret()
redis = Redis(host=config.redis_host, port=config.redis_port)
mongo = MongoClient(config.mongo_uri)
saleHandler = SaleHandler(config.mongo_db, connection=mongo)
providerHandler = ProviderHandler(config.mongo_db, connection=mongo)
userHandler = UserHandler(config.mongo_db, connection=mongo)
productHandler = ProductHandler(config.mongo_db, connection=mongo)
loginHandler = LoginHandler(config.mongo_db, connection=mongo)
tokenHandler = TokenHandler(config.token_ttl, config.secret, mongo, config.mongo_db)
dashboard = Dashboard(app, mongo, config.mongo_db)

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
    try:
        products = productHandler.getProducts()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/product', methods=['POST'])
@login_required
def addProduct():
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
    try:
        product = productHandler.getProductByID(id)
        return jsonify(product), 200
    except ProductNotFoundException:
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/product/<id>', methods=['PUT'])
@login_required
def updateProduct(id): #TODO: Add validation for the request to only update only the fields that are present in the request
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description')
        category = data.get('category')
        price = data.get('price')
        status = data.get('status')
        quantity = data.get('quantity')
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
    try:
        sales = saleHandler.getSales()
        return jsonify(sales), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/sale', methods=['POST'])
@login_required
def generateSale():
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
@login_required #TODO: Implement this
def getSalesByProduct(id):
    try:
        return jsonify({'message': 'Not implemented'}), 501
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/sale/user/<id>', methods=['GET'])
@login_required
def getSalesByUser(id):
    try:
        sales = saleHandler.getSalesByUser(id)
        return jsonify(sales), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Provider endpoints

@app.route('/provider', methods=['GET'])
@login_required
def getProviders():
    try:
        providers = providerHandler.getProviders()
        return jsonify(providers), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/provider', methods=['POST'])
@login_required
def addProvider():
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
    try:
        users = userHandler.getUsers()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user', methods=['POST'])
@login_required
def addUser():
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
    try:
        user = userHandler.getUserByID(id)
        return jsonify(user), 200
    except UserNotFoundException:
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/user/<id>', methods=['PUT'])
@login_required #TODO: Implement this
def updateUser(id):
    try:
        return jsonify({'message': 'Not implemented'}), 501
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<id>', methods=['DELETE'])
@login_required
def deleteUser(id):
    try:
        userHandler.deleteUser(id)
        return jsonify({'message': 'User deleted'}), 200
    except UserNotFoundException:
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
