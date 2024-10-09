class Provider:
    
    @staticmethod
    def bulk_from_dict(data: dict) -> list['Provider']:
        return [Provider(**item) for item in data]
    
    def __init__(self,name: str, address: str, _id: int = None) -> None:
        self.name = name
        self.address = address
        self._id = _id
        self._isActive = True
        #TODO: Add more fields as needed

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'address': self.address
            #...
        } #TODO: Add more fields as needed
    
    def __str__(self) -> str:
        return self.name