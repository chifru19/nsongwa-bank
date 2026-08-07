import pytest
from app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Nsongwa Credit Union" in response.data

def test_registration_and_login_flow(client):
    """Test user registration and subsequent login."""
    # Register a new member
    response = client.post("/register", data={
        "user_id": "1005",
        "pin": "1234",
        "name": "Frank Fru"
    }, follow_redirects=True)
    assert response.status_code == 200

    # Login with the created credentials
    response = client.post("/login", data={
        "user_id": "1005",
        "pin": "1234"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome, Frank Fru!" in response.data
