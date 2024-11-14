from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///properties.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    is_admin = db.Column(db.Boolean, default = False)
    
@app.route('/users', methods = ['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    is_admin = data.get('is_admin', False)

    if not username:
        return jsonify({'message': 'Username is required'}), 400

    if User.query.filter_by(username = username).first():
        return jsonify({'message': 'Username already exists'}), 409

    new_user = User(username = username, is_admin = is_admin)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201