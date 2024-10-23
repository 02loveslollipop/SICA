from sale import Sale
from pymongo import MongoClient

class SaleHandler:

    def __init__(self, db_name: str, uri: str = None, connection: MongoClient = None) -> None:
        if connection is not None:
            self.connection = connection
        else:
            self.connection = MongoClient(uri)
        self.db_name = db_name
        self.conn = self.connection[self.db_name]

    def getSales(self) -> list[dict]:
        saleConn = self.conn.sales
        sales = saleConn.find()
        return [Sale.from_dict(sale) for sale in sales]
    
    def getSalesByDate(self, date: str) -> list[dict]:
        saleConn = self.conn.sales
        sales = saleConn.find({'date': date})
        return [Sale.from_dict(sale) for sale in sales]
    
    def getSalesByUser(self, user_id: int) -> list[dict]:
        saleConn = self.conn.sales
        sales = saleConn.find({'user_id': user_id})
        return [Sale.from_dict(sale) for sale in sales]
    
    def makeSale(self, id_seller: str, id_client: str, products: list[dict], date: str) -> dict:
        total = 0
        productReceiptDetails = []
        for product in products:
            productResult = self.conn.products.find_one({'_id': product['idProducto']})
            if (productPrice := productResult.get('price')) is None:
                return {'error': f'Product {product["idProducto"]} not found'}
            total += productPrice * product['quantity']
            productReceiptDetails.append({
                'quantity': product['quantity'],
                'product': productResult['name'],
                'price': productPrice,
                'subtotal': productPrice * product['quantity']
            })
        saleConn = self.conn.sales
        saleConn.insert_one({
            'id_seller': id_seller,
            'id_client': id_client,
            'products': products,
            'date': date,
            'total': total
        })
        return {
            'seller': id_seller,
            'client': id_client,
            'date': date,
            'total': total,
            'products': productReceiptDetails
        }

            
    