import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_create_normal_user(client):
    new_user = {
        "username": "testuser"
    }
    response = client.post('/users', json=new_user)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User created successfully'
    assert 'user_id' in data

def test_create_admin_user(client):
    new_user = {
        "username": "testuser",
        "is_admin": True
    }
    response = client.post('/users', json=new_user)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User created successfully'
    assert 'user_id' in data
    
def test_create_user_without_username(client):
    new_user = {
        "is_admin": True
    }
    response = client.post('/users', json=new_user)
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'Username is required'

def test_create_duplicate_user(client):
    user1 = {
        "username": "duplicateuser",
        "is_admin": False
    }
    response1 = client.post('/users', json=user1)
    assert response1.status_code == 201

    user2 = {
        "username": "duplicateuser",
        "is_admin": True
    }
    response2 = client.post('/users', json=user2)
    assert response2.status_code == 409
    data = response2.get_json()
    assert data['message'] == 'Username already exists'