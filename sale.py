class Sale:
    def __init__(self, id_seller: int, id_client: int, products: list[dict], date: str, idSale: str = None, total: float = None) -> None:
        self.id_seller = id_seller
        self.id_client = id_client
        self.products = products
        self.date = date
        self.idSale = idSale
        self.total = total
    
    @staticmethod
    def from_dict(data: dict) -> 'Sale':
        return Sale(**data)
    
    def to_dict(self) -> dict:
        return {
            'id_seller': self.id_seller,
            'id_client': self.id_client,
            'products': self.products,
            'date': self.date,
            'idSale': self.idSale,
            'total': self.total
        }