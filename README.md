# zd_task  

## Installation

### 1. Clone the Repo 
`git clone https://github.com/daarn/zd_task`

### 2. Set up a Virtual Environment
```
cd zd_task
python3 -m venv venv
source venv/bin/activate
```

### 3. Install packages
`pip install -r requirements.txt`

### 4. Create .env file at project root with SQLite URI eg.:
`SQLALCHEMY_DATABASE_URI=sqlite:///properties.db`

### 5. Run the application
`flask run`

### 6. Alternatively, run the tests:
`PYTHONPATH=. pytest tests`


## API Endpoints
### **User Endpoints**

| Method | Endpoint  | Description       | Request Body                              |
|--------|-----------|-------------------|------------------------------------------|
| POST   | `/users`  | Create a new user | `{ "username": "string", "is_admin": "boolean" }` |

---

### **Property Endpoints**

| Method | Endpoint                   | Description              | Request Body                                                                                              |
|--------|----------------------------|--------------------------|----------------------------------------------------------------------------------------------------------|
| POST   | `/properties`              | Create a property        | `{ "address": "string", "postcode": "string", "city": "string", "number_of_rooms": "integer", "user_id": "integer" }` |
| GET    | `/properties`              | List all properties      | Params:<br>`user_id`: ID of the user retrieving the properties                                   |
| GET    | `/properties/<int:id>`     | Retrieve a property by ID | Params:<br>`user_id`: ID of the user retrieving the property                                     |
| DELETE | `/properties/<int:id>`     | Delete a property by ID  | Params:<br>`user_id`: ID of the user attempting to delete the property                          |
