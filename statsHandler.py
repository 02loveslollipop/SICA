from pymongo import MongoClient

class StatsHandler:
    def __init__(self,db_name: str,  uri: str = None, connection: MongoClient = None) -> None:
        if connection is not None:
            self.connection = connection
        else:
            self.connection = MongoClient(uri)
        self.db_name = db_name
        self.statsConn = self.connection[self.db_name].stats
    
    def getStats(self) -> dict:
        stats = self.statsConn.find_one()
        return stats
    
    def genStats(self) -> None:
        pass # Generate or update stats here (Sells, providers, products, etc)