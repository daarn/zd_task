import pytest
from app import app, db, User, Property

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        test_user = User(username="testuser", is_admin=False)
        test_user2 = User(username="testuser2", is_admin=False)
        
        db.session.add(test_user)
        db.session.add(test_user2)
        
        db.session.commit()
        yield app.test_client()
        db.drop_all()

def test_create_property(client):
    user = User.query.filter_by(username="testuser").first()

    new_property = {
        "address": "123 Street",
        "postcode": "BT1 3AB",
        "city": "CreateCity",
        "number_of_rooms": 5,
        "user_id": user.id 
    }
    response = client.post('/properties', json=new_property)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Property created successfully'
    
def test_get_all_properties(client):
    user = User.query.filter_by(username="testuser").first()

    property1 = Property(address="1 Avenue", postcode="BT1 2AB", city="AllCity", number_of_rooms=3, created_by=user.id)
    property2 = Property(address="2 Avenue", postcode="BT2 3BC", city="AllCityTwo", number_of_rooms=2, created_by=user.id)
    db.session.add(property1)
    db.session.add(property2)
    db.session.commit()

    response = client.get(f'/properties?user_id={user.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data.get("properties")) == 2
    assert data.get('properties')[0]['address'] == "1 Avenue"
    assert data.get('properties')[1]['address'] == "2 Avenue"
    
def test_get_specific_property(client):
    user = User.query.filter_by(username="testuser").first()

    property = Property(address="3 Street", postcode="BT3 4DE", city="SpecificCity", number_of_rooms=1, created_by=user.id)
    db.session.add(property)
    db.session.commit()

    response = client.get(f'/properties/{property.id}?user_id={user.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data.get('property')['address'] == "3 Street"
    assert data.get('property')['city'] == "SpecificCity"
    
def test_get_nonexistent_property(client):
    user = User.query.filter_by(username="testuser").first()

    response = client.get(f'/properties/999?user_id={user.id}')
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'Property not found'
    
def test_delete_property(client):
    user = User.query.filter_by(username="testuser").first()

    property = Property(address="4 Street", postcode="BT5 6GH", city="DeleteCity", number_of_rooms=3, created_by=user.id)
    db.session.add(property)
    db.session.commit()
    
    response = client.delete(f'/properties/{property.id}?user_id={2}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'User does not own the specified property'

    response = client.delete(f'/properties/{property.id}?user_id={user.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Property deleted successfully'

    response = client.get(f'/properties/{property.id}?user_id={user.id}')
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'Property not found'