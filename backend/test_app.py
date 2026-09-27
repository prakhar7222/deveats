import os
os.environ.setdefault('DB_HOST','localhost'); os.environ.setdefault('DB_PORT','5432'); os.environ.setdefault('DB_NAME','deveats'); os.environ.setdefault('DB_USER','deveats'); os.environ.setdefault('DB_PASSWORD','deveats')
from app import app

def test_health_endpoint():
    app.config['TESTING']=True
    with app.test_client() as c: assert c.get('/api/health').status_code in (200,503)

def test_restaurants_endpoint():
    app.config['TESTING']=True
    with app.test_client() as c: assert c.get('/api/restaurants').status_code in (200,500)

def test_missing_restaurant():
    app.config['TESTING']=True
    with app.test_client() as c: assert c.get('/api/restaurants/999999').status_code in (404,500)
