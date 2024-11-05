from provider import Provider
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.results import InsertOneResult, UpdateResult
from exceptions import ProviderNotFoundException
from bson import ObjectId

class ProviderHandler:
    """
    ProviderHandler is a class that manages CRUD operations for providers in a MongoDB database.
    Attributes:
        db_name (str): The name of the database.
        connection (MongoClient): The MongoDB client connection.
    Methods:
        __init__(db_name: str, uri: str = None, connection: MongoClient = None) -> None:
            Initializes the ProviderHandler with a database name, and optionally a URI or an existing MongoClient connection.
        getProviders() -> list[Provider]:
            Retrieves all providers from the database and returns them as a list of Provider objects.
        getProviderByID(provider_id) -> Provider:
            Retrieves a provider by its ID from the database and returns it as a Provider object.
        addProvider(provider: Provider) -> InsertOneResult:
            Adds a new provider to the database and returns the result of the insertion.
        updateProvider(provider_id, provider: Provider) -> UpdateResult:
            Updates an existing provider in the database by its ID and returns the result of the update.
        deleteProvider(provider_id) -> UpdateResult:
            Soft deletes a provider by setting its '_isActive' field to False and returns the result of the update.
        __del__() -> None:
            Closes the MongoDB client connection when the ProviderHandler object is deleted.
    """
    def __init__(self,db_name: str,  uri: str = None, connection: MongoClient = None) -> None:
        """
        Initializes the provider handler with a database name and optional URI or connection.

        Args:
            db_name (str): The name of the database.
            uri (str, optional): The URI for the MongoDB connection. Defaults to None.
            connection (MongoClient, optional): An existing MongoClient connection. Defaults to None.

        If a connection is provided, it will be used. Otherwise, a new MongoClient will be created using the provided URI.
        """
        if connection is not None:
            self.connection = connection
        else:
            self.connection = MongoClient(uri, server_api=ServerApi('1'))
        self.db_name = db_name
        
    
    def getProviders(self) -> list[Provider]:
        """
        Retrieves a list of providers from the database.

        Returns:
            list[Provider]: A list of Provider objects retrieved from the database.
        """
        db = self.connection[self.db_name]
        result = db.providers.find()
        resultDict = list(result)
        return resultDict
    
    def getProviderByID(self, provider_id) -> Provider:
        """
        Retrieve a provider by its unique identifier.

        Args:
            provider_id (str): The unique identifier of the provider.

        Returns:
            Provider: The provider object corresponding to the given ID.
        """
        db = self.connection[self.db_name]
        
        result = db.providers.find_one({'_id': ObjectId(provider_id)})
        if result is None:
            raise ProviderNotFoundException(f"Provider with id {provider_id} not found")
        
    
    def addProvider(self, provider: Provider) -> InsertOneResult:
        """
        Adds a new provider to the database.

        Args:
            provider (Provider): The provider object to be added to the database.

        Returns:
            InsertOneResult: The result of the insert operation.
        """
        db = self.connection[self.db_name]
        return db.providers.insert_one(provider.to_dict())
    
    def updateProvider(self, provider_id, provider: Provider) -> UpdateResult:
        """
        Updates a provider's information in the database.

        Args:
            provider_id (str): The unique identifier of the provider to be updated.
            provider (Provider): An instance of the Provider class containing the updated information.

        Returns:
            UpdateResult: The result of the update operation, including details such as the number of documents matched and modified.
        """
        db = self.connection[self.db_name]
        return db.providers.update_one({'_id': provider_id}, {'$set': provider.to_dict()})
    
    def deleteProvider(self, provider_id) -> UpdateResult:
        """
        Marks a provider as inactive in the database.

        Args:
            provider_id (str): The unique identifier of the provider to be marked as inactive.

        Returns:
            UpdateResult: The result of the update operation, indicating the success or failure of the operation.
        """
        db = self.connection[self.db_name]
        return db.providers.update_one({'_id': provider_id}, {'$set': {'_isActive': False}})
    
    def __del__(self) -> None:
        """
        Destructor method that ensures the database connection is properly closed
        when the instance is deleted.

        This method is automatically called when the instance is about to be destroyed.
        It closes the database connection to free up resources.
        """
        self.connection.close()    

    

        