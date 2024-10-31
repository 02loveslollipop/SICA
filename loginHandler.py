from pymongo import MongoClient
from login import Login
from pymongo.results import InsertOneResult, UpdateResult
from pymongo.server_api import ServerApi
from bson import ObjectId
import bcrypt

class LoginHandler:

    def __init__(self,db_name: str,  uri: str = None, connection: MongoClient = None) -> None:
        if connection is not None:
            self.connection = connection
        else:
            self.connection = MongoClient(uri, server_api=ServerApi('1'))
        self.db_name = db_name

    def login(self,login: Login) -> bool:
        db = self.connection[self.db_name]
        user = db.users.find_one({'email': login.email})
        if user is None:
            return False
        password = login.password.encode('utf-8')
        if bcrypt.checkpw(password, user['password']):
            return True
        else:
            return False