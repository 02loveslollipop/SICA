from pymongo import MongoClient
from userHandler import UserHandler
from productHandler import ProductHandler
from providerHandler import ProviderHandler
from saleHandler import SaleHandler
from user import User
from product import Product
from provider import Provider
from sale import Sale
from secret import Secret
import datetime

def create_test_data() -> None:
    # Initialize handlers with the database name and URI
    secret = Secret()
    db_name = secret.dbName
    uri = secret.uri
    mongo_client = MongoClient(uri)
    
    user_handler = UserHandler(db_name=db_name, connection=mongo_client)
    product_handler = ProductHandler(db_name=db_name, connection=mongo_client)
    provider_handler = ProviderHandler(db_name=db_name, connection=mongo_client)
    sale_handler = SaleHandler(db_name=db_name, connection=mongo_client)

    # Create test users
    users = [
        User(name='John', lastname='Doe', email='john.doe@example.com', cellphone=1234567890, password='password', role='admin'),
        User(name='Jane', lastname='Smith', email='jane.smith@example.com', cellphone=2345678901, password='password', role='user')
    ]
    for user in users:
        user_handler.userRegister(user)

    # Create test products
    products = [
        Product(name='Product One', description='Description for product one', category='Category A', price=10.0, status='available', quantity=100),
        Product(name='Product Two', description='Description for product two', category='Category B', price=20.0, status='available', quantity=200)
    ]
    for product in products:
        product_handler.productRegister(product)
        product._id = mongo_client[db_name].products.find_one({'name': product.name})['_id']

    # Create test providers
    providers = [
        Provider(name='Provider One', address='123 Main St'),
        Provider(name='Provider Two', address='456 Elm St')
    ]
    for provider in providers:
        provider_handler.addProvider(provider)
        provider._id = mongo_client[db_name].providers.find_one({'name': provider.name})['_id']

    # Create test sales
    sales = [
        Sale(id_seller=1, id_client=2, products=[{'idProducto': products[0]._id, 'quantity': 5}, {'idProducto': products[1]._id, 'quantity': 10}], date=datetime.datetime.now().isoformat())
    ]
    for sale in sales:
        sale_handler.makeSale(sale.id_seller, sale.id_client, sale.products, sale.date)

def generate_sales(n: int) -> None:
    # Initialize handlers with the database name and
    secret = Secret()
    db_name = secret.dbName
    uri = secret.uri
    mongo_client = MongoClient(uri)
    sale_handler = SaleHandler(db_name=db_name, connection=mongo_client)
    product_handler = ProductHandler(db_name=db_name, connection=mongo_client)
    user_handler = UserHandler(db_name=db_name, connection=mongo_client)
    provider_handler = ProviderHandler(db_name=db_name, connection=mongo_client)

    # Get all products
    products = product_handler.getProducts()
    # Get all users
    users = user_handler.getUsers()
    
    # Create n sales
    for i in range(n):
        # Randomly select a seller and a client
        seller = users[i % len(users)]
        client = users[(i + 1) % len(users)]
        # Randomly select a number of products to buy
        num_products = i % len(products) + 1
        # Randomly select products to buy
        products_to_buy = []
        for j in range(num_products):
            product = products[j]
            quantity = (j + 1) * 5
            products_to_buy.append({'idProducto': product._id, 'quantity': quantity})
        # Randomly select a date
        date = datetime.datetime.now().isoformat()
        # Make the sale
        sale_handler.makeSale(seller._id, client._id, products_to_buy, date)

if __name__ == '__main__':
    #create_test_data()
    generate_sales(89)