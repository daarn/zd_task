from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from schemas import UserSchema, PropertySchema

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///properties.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

##### MODELS #####


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    postcode = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("properties", lazy=True))


user_schema = UserSchema()
property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)

with app.app_context():
    db.create_all()


##### API #####


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"message": "Username is required"}), 400

    try:
        data = user_schema.load(data)
    except ValidationError as err:
        return err.messages, 422

    is_admin = data.get("is_admin", False)

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409

    new_user = User(username=username, is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(
        {"message": "User created successfully", "user_id": new_user.id}
    ), 201


@app.route("/properties", methods=["POST"])
def create_property():
    data = request.json

    if not data:
        return {"message": "No input data provided"}, 400
    try:
        data = property_schema.load(data)
    except ValidationError as err:
        return err.messages, 422

    user_id = data.get("user_id")
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    new_property = Property(
        address=data["address"],
        postcode=data["postcode"],
        city=data["city"],
        number_of_rooms=data["number_of_rooms"],
        created_by=user.id,
    )
    db.session.add(new_property)
    db.session.commit()
    return jsonify({"message": "Property created successfully"}), 201


@app.route("/properties", methods=["GET"])
def list_properties():
    user_id = request.args.get("user_id")
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    properties = Property.query.all()
    result = properties_schema.dump(properties)
    return {"properties": result}


@app.route("/properties/<int:property_id>", methods=["GET"])
def get_property(property_id):
    user_id = request.args.get("user_id")
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    property = db.session.get(Property, property_id)
    if not property:
        return jsonify({"message": "Property not found"}), 400

    property_result = property_schema.dump(property)
    return {"property": property_result}


@app.route("/properties/<int:property_id>", methods=["DELETE"])
def delete_property(property_id):
    user_id = request.args.get("user_id")
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    property = db.session.get(Property, property_id)
    if not property:
        return jsonify({"message": "Property not found"}), 400
    elif property.created_by != user.id:
        return jsonify({"message": "User does not own the specified property"}), 404

    db.session.delete(property)
    db.session.commit()
    return jsonify({"message": "Property deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
