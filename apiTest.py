import pytest
import requests
from datetime import datetime, timedelta
import logging
import http.client as http_client

http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

BASE_URL = "http://localhost:5000"
TEST_USER = {"email": "john.doe@example.com", "password": "password"}

@pytest.fixture
def auth_token():
    """Fixture to get authentication token"""
    response = requests.post(f"{BASE_URL}/login", json=TEST_USER)
    assert response.status_code == 200
    return response.json()["token"]

def test_login():
    """Test login endpoint"""
    response = requests.post(f"{BASE_URL}/login", json=TEST_USER)
    assert response.status_code == 200
    assert "token" in response.json()

def test_product_operations(auth_token):
    """Test product CRUD operations"""
    headers = {"X-Access-Token": auth_token}
    
    # Test POST
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "category": "Test Category",
        "price": 99.99,
        "status": "Available",
        "quantity": 10
    }
    response = requests.post(f"{BASE_URL}/product", headers=headers, json=product_data)
    assert response.status_code == 201
    
    # Test GET all
    response = requests.get(f"{BASE_URL}/product", headers=headers)
    assert response.status_code == 200
    products = response.json()
    product_id = products[-1]["_id"]["$oid"]
    
    # Test GET one
    response = requests.get(f"{BASE_URL}/product/{product_id}", headers=headers)
    assert response.status_code == 200
    
    # Test PUT
    product_data["name"] = "Updated Product"
    response = requests.put(f"{BASE_URL}/product/{product_id}", headers=headers, json=product_data)
    assert response.status_code == 200
    
    # Test DELETE
    response = requests.delete(f"{BASE_URL}/product/{product_id}", headers=headers)
    assert response.status_code == 200

def test_provider_operations(auth_token):
    """Test provider CRUD operations"""
    headers = {"X-Access-Token": auth_token}
    
    # Test POST
    provider_data = {
        "name": "Test Provider",
        "address": "Test Address"
    }
    response = requests.post(f"{BASE_URL}/provider", headers=headers, json=provider_data)
    assert response.status_code == 201
    
    # Test GET all
    response = requests.get(f"{BASE_URL}/provider", headers=headers)
    assert response.status_code == 200
    providers = response.json()
    provider_id = providers[-1]["_id"]["$oid"]
    
    # Test GET one
    response = requests.get(f"{BASE_URL}/provider/{provider_id}", headers=headers)
    assert response.status_code == 200
    
    # Test PUT
    provider_data["name"] = "Updated Provider"
    response = requests.put(f"{BASE_URL}/provider/{provider_id}", headers=headers, json=provider_data)
    assert response.status_code == 200
    
    # Test DELETE
    response = requests.delete(f"{BASE_URL}/provider/{provider_id}", headers=headers)
    assert response.status_code == 200

def test_sale_operations(auth_token):
    """Test sale operations"""
    headers = {"X-Access-Token": auth_token}
    
    # Test POST
    sale_data = {
        "id_seller": "test_seller",
        "id_client": "test_client",
        "products": [{"idProducto": "672312212da7ae7986157674", "quantity": 5}, {"idProducto": "672312222da7ae7986157675", "quantity": 3}],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    response = requests.post(f"{BASE_URL}/sale", headers=headers, json=sale_data)
    assert response.status_code == 201
    
    # Test GET all
    response = requests.get(f"{BASE_URL}/sale", headers=headers)
    assert response.status_code == 200
    
    # Test GET by date
    date_lo = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    date_hi = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    response = requests.get(
        f"{BASE_URL}/sale/date",
        headers=headers,
        params={"dateLo": date_lo, "dateHi": date_hi}
    )
    assert response.status_code == 200

def test_user_operations(auth_token):
    """Test user CRUD operations"""
    headers = {"X-Access-Token": auth_token}
    
    # Test POST
    user_data = {
        "name": "Test User",
        "lastname": "Test Lastname",
        "email": "testuser@example.com",
        "cellphone": "1234567890",
        "password": "testpass",
        "role": "user"
    }
    response = requests.post(f"{BASE_URL}/user", headers=headers, json=user_data)
    assert response.status_code == 201
    
    # Test GET all
    response = requests.get(f"{BASE_URL}/user", headers=headers)
    assert response.status_code == 200
    users = response.json()
    user_id = users[-1]["_id"]["$oid"]
    
    # Test GET one
    response = requests.get(f"{BASE_URL}/user/{user_id}", headers=headers)
    assert response.status_code == 200
    
    # Test PUT
    user_data["name"] = "Updated User"
    response = requests.put(f"{BASE_URL}/user/{user_id}", headers=headers, json=user_data)
    assert response.status_code == 200
    
    # Test DELETE
    response = requests.delete(f"{BASE_URL}/user/{user_id}", headers=headers)
    assert response.status_code == 200

def test_logout(auth_token):
    """Test logout endpoint"""
    headers = {"X-Access-Token": auth_token}
    response = requests.post(f"{BASE_URL}/logout", headers=headers)
    assert response.status_code == 200