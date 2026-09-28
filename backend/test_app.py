import os

os.environ.setdefault("DB_HOST", "database")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "deveats")
os.environ.setdefault("DB_USER", "deveats")
os.environ.setdefault("DB_PASSWORD", "deveats123")

from app import app


def test_health_endpoint():
    app.config["TESTING"] = True

    with app.test_client() as c:
        response = c.get("/api/health")

    assert response.status_code == 200


def test_restaurants_endpoint():
    app.config["TESTING"] = True

    with app.test_client() as c:
        response = c.get("/api/restaurants")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_missing_restaurant():
    app.config["TESTING"] = True

    with app.test_client() as c:
        response = c.get("/api/restaurants/999999")

    assert response.status_code == 404
