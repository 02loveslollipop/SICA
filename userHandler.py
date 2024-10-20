from flask import jsonify
from pymongo import MongoClient
import pymongo
from user import User
from pymongo.results import InsertOneResult, UpdateResult
from pymongo.server_api import ServerApi
from bson import ObjectId

class UserHandler:

    def __init__(self,db_name: str,  uri: str = None, connection: MongoClient = None) -> None:
        if connection is not None:
            self.connection = connection
        else:
            self.connection = MongoClient(uri, server_api=ServerApi('1'))
        self.db_name = db_name

    def userRegister(self,user: User) -> InsertOneResult:
        db = self.connection[self.db_name]
        return db.users.insert_one(user.to_dict())


    def getUsers(self) -> list[User]:
        db = self.connection[self.db_name]

        result = db.users.find({'_isActive': True})	
    
        resultDict = list(result)
    
        return User.bulk_from_dict(resultDict)
    
    def getUserByID(self, user_id) -> User:
        db = self.connection[self.db_name]
        user_id_object = ObjectId(user_id)
        response = db.users.find_one({'_id': user_id_object})
        return response
        
    def updateUser(self, user_id, user: User) -> UpdateResult:
        db = self.connection[self.db_name]
        return db.user.update_one({'_id': user_id}, {'$set': user.to_dict()})
    
    def deleteUser(self, user_id) -> UpdateResult:
        db = self.connection[self.db_name]
        return db.user.update_one({'_id': user_id}, {'$set': {'_isActive': False}})
    
    def __del__(self) -> None:

        self.connection.close() 