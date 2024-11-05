from pymongo import MongoClient
from user import User
from pymongo.results import InsertOneResult, UpdateResult
from pymongo.server_api import ServerApi
from bson import ObjectId
from exceptions import UserNotFoundException

class UserHandler:

    def __init__(self,db_name: str,  uri: str = None, connection: MongoClient = None) -> None:
        if connection is not None:
            self.connection = connection
        else:
            self.connection = MongoClient(uri, server_api=ServerApi('1'))
        self.db_name = db_name

    def userRegister(self,user: User) -> InsertOneResult:
        db = self.connection[self.db_name]
        return db.users.insert_one(user.to_dict()).acknowledged


    def getUsers(self) -> list[User]:
        db = self.connection[self.db_name]
        result = db.users.find({'_isActive': True})	
        result = list(result)
        return result
    
    def getUserByID(self, user_id) -> User:
        db = self.connection[self.db_name]
        user_id_object = ObjectId(user_id)
        result = db.users.find_one({'_id': user_id_object})
        if result is None:
            raise UserNotFoundException(f"User with id {user_id} not found")
        return result
        
    def updateUser(self, user_id, user: User) -> UpdateResult:
        db = self.connection[self.db_name]
        user_id_object = ObjectId(user_id)
        userJson = user.to_dict()
        userJson['_id'] = user_id_object
        print(userJson)
        result = db.users.update_one({'_id': user_id_object}, {'$set': userJson})
        if result.modified_count > 0:
            return {'message': 'User updated successfully', 'updated_count': result.modified_count}
        else:
            return {'message': 'No user was updated', 'updated_count': result.modified_count}


    def deleteUser(self, user_id) -> UpdateResult:
        db = self.connection[self.db_name]
        user_id_object = ObjectId(user_id)
        return db.users.update_one({'_id': user_id_object}, {'$set': {'_isActive': False}})
    
    def getUserRole(self, email) -> str:
        db = self.connection[self.db_name]
        user = db.users.find_one({'email': email})
        if user is None:
            raise UserNotFoundException(f"User with email {email} not found")
        else:
            return user['role']