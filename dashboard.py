from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
from secret import Secret
from pymongo import MongoClient
import sys

"""
This script creates a Dash app that displays a table with the sales data and the products of the providers from the database.

# Example of sale document
```json
{
  "id_seller": {
    "$oid": "672312202da7ae7986157672"
  },
  "id_client": {
    "$oid": "672312212da7ae7986157673"
  },
  "products": [
    {
      "idProducto": {
        "$oid": "672312212da7ae7986157674"
      },
      "quantity": 5
    }
  ],
  "date": "2024-10-31T00:17:45.343090",
  "total": 50
}
```

# Graphs
- pie chart with most sold products -> requieres a function that returns a dataframe with the products and the quantity sold
- bar chart with sales per day -> requieres a function that returns a dataframe with the date and the total sales
- bar chart with sales per seller -> requieres a function that returns a dataframe with the seller and the total sales
- bar chart with sales per provider (Not yet)*
- bar chart with sales per week -> requieres a function that returns a dataframe with the week and the total sales
- bar chart with sales per month -> requieres a function that returns a dataframe with the month and the total sales

"""

def enhancedRetrieveData(secret: Secret) -> pd.DataFrame:
    mongo = MongoClient(secret.uri)
    db = mongo[secret.dbName]
    
    # Retrieve all sales
    sales = list(db.sales.find())
    
    # Retrieve all users and products in bulk
    user_ids = {sale['id_seller'] for sale in sales}.union({sale['id_client'] for sale in sales})
    product_ids = {product['idProducto'] for sale in sales for product in sale['products']}
    
    users = {user['_id']: user for user in db.users.find({'_id': {'$in': list(user_ids)}})}
    products = {product['_id']: product for product in db.products.find({'_id': {'$in': list(product_ids)}})}
    
    # Process sales data
    salesResult = [
        {
            'seller': users[sale['id_seller']]['name'],
            'client': users[sale['id_client']]['name'],
            'products': [{'idProducto': products[product['idProducto']]['name'], 'quantity': product['quantity']} for product in sale['products']],
            'date': sale['date'],
            'total': sale['total']
        }
        for sale in sales
    ]
    
    return pd.DataFrame(salesResult)

def retrieveData(secret: Secret) -> pd.DataFrame:
    mongo = MongoClient(secret.uri)
    db = mongo[secret.dbName]
    sales = db.sales.find()
    # replace id_seller and id_client and idProducto with the actual names
    
    salesResult = []
    for sale in sales:
        sellerInfo = db.users.find_one({'_id': sale['id_seller']})
        clientInfo = db.users.find_one({'_id': sale['id_client']})
        productsList = []
        for product in sale['products']:
            productInfo = db.products.find_one({'_id': product['idProducto']})
            productsList.append({'idProducto': productInfo['name'], 'quantity': product['quantity']})
        salesResult.append({'seller': sellerInfo['name'], 'client': clientInfo['name'], 'products': productsList, 'date': sale['date'], 'total': sale['total']})
    return pd.DataFrame(salesResult)    

def getProductsSales(df: pd.DataFrame) -> pd.DataFrame:
    products = []
    for products_list in df['products']:
        for product in products_list:
            products.append({'product': product['idProducto'], 'quantity': product['quantity']})
    
    result = {}
    for product in products:
        if product['product'] in result:
            result[product['product']] += product['quantity']
        else:
            result[product['product']] = product['quantity']
    
    return pd.DataFrame(result.items(), columns=['products', 'quantity'])         

def getSalesPerDay(df: pd.DataFrame) -> pd.DataFrame:
    salesPerDay = df.groupby('date').sum()['total']
    return salesPerDay.reset_index()

def getSalesPerWeek(df: pd.DataFrame) -> pd.DataFrame:
    #convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    #generate week column from date
    df['week'] = df['date'].dt.isocalendar().week
    #generate year column from date
    df['year'] = df['date'].dt.isocalendar().year
    #drop all entries from a year that is not the current year
    df = df[df['year'] == pd.Timestamp.now().year]
    df = df.drop(columns=['year'])
    df = df.drop(columns=['seller'])
    df = df.drop(columns=['client'])
    df = df.drop(columns=['products'])
    df = df.drop(columns=['date'])
    result = {}
    for entry in df.to_dict('records'):
        if str(entry['week']) in result:
            result[entry['week']] += entry['total']
        else:
            result[entry['week']] = entry['total']
    return pd.DataFrame(result.items(), columns=['week', 'total']).sort_values(by='week')

def getSalesPerMonth(df: pd.DataFrame) -> pd.DataFrame:
    #generate month column from date
    df['month'] = df['date'].dt.month
    #generate year column from date
    df['year'] = df['date'].dt.year
    #drop all entries from a year that is not the current year
    df = df[df['year'] == pd.Timestamp.now().year]
    df = df.drop(columns=['year'])
    df = df.drop(columns=['seller'])
    df = df.drop(columns=['client'])
    df = df.drop(columns=['products'])
    df = df.drop(columns=['date'])
    result = {}
    for entry in df.to_dict('records'):
        if str(entry['month']) in result:
            result[entry['month']] += entry['total']
        else:
            result[entry['month']] = entry['total']
    return pd.DataFrame(result.items(), columns=['month', 'total']).sort_values(by='month')

def getSalesPerSeller(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=['date'])
    salesPerSeller = df.groupby('seller').sum()['total']
    return salesPerSeller.reset_index()


# Load data

if __name__ == '__main__':
    secret = Secret()
    print('Retrieving data...')
    df = enhancedRetrieveData(secret)
    dfSales = getProductsSales(df)
    dfWeek = getSalesPerWeek(df)
    dfMonth = getSalesPerMonth(df)
    dfSeller = getSalesPerSeller(df)

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        # Pie chart with most sold products
        html.Div([
            html.H2('Most Sold Products', style={'font-family': 'Montserrat'}),
            dcc.Graph(
                figure=px.pie(dfSales, names='products', values='quantity'),
                style={'height': '90vh'}
            )
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
        # Other graphs
        html.Div([
            html.H2('Sales Per Week', style={'font-family': 'Montserrat'}),
            dcc.Graph(
                figure=px.bar(dfWeek, x='week', y='total'),
                style={'height': '25vh'}
            ),
            html.H2('Sales Per Month', style={'font-family': 'Montserrat'}),
            dcc.Graph(
                figure=px.bar(dfMonth, x='month', y='total'),
                style={'height': '25vh'}
            ),
            html.H2('Sales Per Seller', style={'font-family': 'Montserrat'}),
            dcc.Graph(
                figure=px.bar(dfSeller, x='seller', y='total'),
                style={'height': '25vh'}
            )
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'})
    ], style={'display': 'flex'})
], style={'background-color': '#ffffff'})  # Set your desired background color here

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Running in dev mode')
        app.run(debug=True, port=5000, host='0.0.0.0')
    elif sys.argv[1] == 'https':
        print('Running dev with https')
        app.run(port=8080, host='0.0.0.0', ssl_context='adhoc', debug=True)
    elif sys.argv[1] == 'prod':
        print('Running in production mode')
        app.run(port=8080, host='0.0.0.0', ssl_context='adhoc', debug=False)
    elif len(sys.argv) == 3 and sys.argv[1] == 'test':
        port = int(sys.argv[2])
        print(f'Running in production test at port {port}')
        app.run(port=port, host='0.0.0.0', ssl_context='adhoc', debug=False)
    else:
        print('Running in dev mode')
        app.run(debug=True, port=5000, host='0.0.0.0')