import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        test_user = User(username="testuser", is_admin=False)
        db.session.add(test_user)
        db.session.commit()
        yield app.test_client()
        db.drop_all()

def test_create_property(client):
    user = User.query.filter_by(username="testuser").first()

    new_property = {
        "address": "123 Street",
        "postcode": "BT1 3AB",
        "city": "Belfast",
        "number_of_rooms": 5,
        "user_id": user.id 
    }
    response = client.post('/properties', json=new_property)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Property created successfully'