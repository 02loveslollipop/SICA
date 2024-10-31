class Product:

    @staticmethod
    def bulk_from_dict(data: dict) -> list['Product']:
        return [Product(**item) for item in data]

    def __init__(self, name: str,description: str,category: str,price: float,status: str,quantity: int,_id: int = None,_isActive: bool = True) -> None:  
        self._id = _id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.status = status
        self.quantity = quantity
        self._isActive = _isActive



    def to_dict(self) -> dict:
        return {
        'name': self.name,
        'description': self.description,
        'category': self.category,
        'price': self.price,
        'status': self.status,
        'quantity' : self.quantity,
        '_isActive': self._isActive	
        } 
    