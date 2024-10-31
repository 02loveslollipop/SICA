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
from dashboard import Dashboard
from login import Login
from user import User
from product import Product
from sale import Sale
from secret import Secret

app = Flask(__name__)
cors = CORS(app)
config = Secret()
redis = Redis(host=config.redis_host, port=config.redis_port)
mongo = MongoClient(config.mongo_uri)
saleHandler = SaleHandler(config.mongo_db, connection=mongo)
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

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login = Login(data['email'], data['password'])
    if loginHandler.login(login):
        response = tokenHandler.generate(data['email'])
        return jsonify(response), 200
    return jsonify({'error': 'Invalid credentials'}), 401




