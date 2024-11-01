from pymongo import MongoClient
from product import Product
from pymongo.results import InsertOneResult, UpdateResult
from pymongo.server_api import ServerApi
from bson import ObjectId
from exceptions import ProductNotFoundException

class ProductHandler:

    def __init__(self,db_name: str,  uri: str = None, connection: MongoClient = None) -> None:
        if connection is not None:
            self.connection = connection
        else:
            self.connection = MongoClient(uri, server_api=ServerApi('1'))
        self.db_name = db_name

    def productRegister(self,product: Product) -> InsertOneResult:
        db = self.connection[self.db_name]
        validate = db.products.find_one({'name': product.name})
        if validate is not None:
            return False
        return db.products.insert_one(product.to_dict()).acknowledged


    def getProducts(self) -> list[Product]:
        db = self.connection[self.db_name]
        result = db.products.find({'_isActive': True})	
        resultDict = list(result)
        return Product.bulk_from_dict(resultDict)
    
    def getProductByID(self, product_id) -> Product:
        db = self.connection[self.db_name]
        product_id_object = ObjectId(product_id)
        result = db.products.find_one({'_id': product_id_object})
        if result is None:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        return result
        
    def updateProduct(self, product_id, product: Product) -> UpdateResult:
        db = self.connection[self.db_name]
        product_id_object = ObjectId(product_id)
        productJson = product.to_dict()
        productJson['_id'] = product_id_object
        #print(productJson)
        result = db.products.update_one({'_id': product_id_object}, {'$set': productJson})
        if result.modified_count > 0:
            return {'message': 'Products updated successfully', 'updated_count': result.modified_count}
        else:
            return {'message': 'No product was updated', 'updated_count': result.modified_count}


    def deleteProduct(self, product_id) -> UpdateResult:
        db = self.connection[self.db_name]
        product_id_object = ObjectId(product_id)
        return db.products.update_one({'_id': product_id_object}, {'$set': {'_isActive': False}})
    