import hashlib
import datetime
from flask import jsonify
from pymongo import MongoClient
from exceptions import ExpiredTokenException, TokenNotInSessionException

class TokenHandler:
    
    def __init__(self, ttl: int, secret: str, connection: MongoClient, db: str) -> None:
        self.secret = secret
        self.ttl = ttl
        self.mongoConnect = connection
        self.db = db
    
    def generate(self, user: str) -> dict:
        token = hashlib.sha256(f'{user}{str(datetime.datetime.now())}'.encode("utf-8")).hexdigest()
        ttl = datetime.datetime.now() + datetime.timedelta(hours=self.ttl)
        result = {
            'token': token,
            'ttl': ttl,
            'user': user
        }
        db = self.mongoConnect[self.db]
        db.tokens.insert_one({"_id": token, "ttl": ttl, "user": user})
        return result
    
    def auth(self, token: str) -> bool:
        db = self.mongoConnect[self.db]
        token = db.tokens.find_one({"_id": token})
        if token is None:
            raise TokenNotInSessionException("Token not found in session")
        if token['ttl'] < datetime.datetime.now():
            db.tokens.delete_one({"_id": token})
            raise ExpiredTokenException("Token expired")
        return True

    def delete(self, token: str) -> None:
        db = self.mongoConnect[self.db]
        result = db.tokens.delete_one({"_id": token})
        if result.deleted_count == 0:
            raise TokenNotInSessionException("Token not found in session")