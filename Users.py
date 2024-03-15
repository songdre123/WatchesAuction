from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib
from flasgger import Swagger
from db_config import set_database_uri

app = Flask(__name__)  # initialize a flask application
CORS(app, origins=["http://localhost:3000"])

# Swagger UI configuration
app.config["SWAGGER"] = {
    "title": "User microservice API",
    "version": 1.0,
    "openapi": "3.0.2",
    "description": "Allows interaction with the Users microservice",
}
swagger = Swagger(app)

path = "Users"
set_database_uri(app, path)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

"""
API Endpoints:
1. GET /user - Get all users
2. GET /user/<string:email> - Get a specific user
3. POST /user/<string:email> - Create a user
4. PUT /user/<string:email> - Edit a user
5. DELETE /user/<string:email> - Delete a user
6. POST /user/login/<string:email> - Check user password

PORT: 5000
DATABASE: Users
TABLE: Users
SQL Credentials: root:root
SQL Port: 3306


SQL Database creation code:
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender CHAR(1),
    address VARCHAR(255),
    account_type VARCHAR(50) NOT NULL,
    profile_picture VARCHAR(255),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    account_status INT DEFAULT 1
);
"""


def hash_password(password):
    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def check_password(password, hashed_password):
    # Hash the provided password and check if it matches the stored hashed password
    return hashed_password == hashlib.sha256(password.encode()).hexdigest()


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    gender = db.Column(db.String(1))
    address = db.Column(db.String(255))
    account_type = db.Column(db.String(50), nullable=False)
    profile_picture = db.Column(db.String(255))
    registration_date = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp()
    )
    account_status = db.Column(db.Integer, default=1)

    def __init__(
        self,
        email,
        password,
        account_type,
        phone_number=None,
        first_name=None,
        last_name=None,
        date_of_birth=None,
        gender=None,
        address=None,
        profile_picture=None,
        account_status=1,
    ):
        self.email = email
        self.password = password
        self.account_type = account_type
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.address = address
        self.profile_picture = profile_picture
        self.account_status = account_status

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "address": self.address,
            "account_type": self.account_type,
            "profile_picture": self.profile_picture,
            "registration_date": self.registration_date.strftime("%Y-%m-%d %H:%M:%S"),
            "account_status": self.account_status,
        }

    def getPasswordHash(self):
        return self.password


# get all users
@app.route("/user")
def get_all():
    """
    Get all users
    ---
    responses:
        200:
            description: Return all books
        404:
            description: No users
    """

    Users = db.session.scalars(db.select(User)).all()

    if len(Users):
        return jsonify(
            {"code": 200, "data": {"users": [user.json() for user in Users]}}
        )
    return jsonify({"code": 404, "message": "There are no Users currently."}), 404


# get specific user by email
@app.route("/user/<string:email>")
def find_by_email(email):
    """
    Get a specifc user by email
    ---
    parameters:
        -   in: email of user
            name: email
            required: true

    responses:
        200:
            description: Return user information with matching email
        404:
            description: No user exists that currently uses that email
    """

    user = db.session.scalars(db.select(User).filter_by(email=email).limit(1)).first()
    if user:
        return jsonify({"code": 200, "data": user.json()})
    return jsonify({"code": 404, "message": "User does not exist."}), 404


# get specific user by id
@app.route("/user/<int:user_id>")
def find_by_id(user_id):
    """
    Get user by ID
    ---
    parameters:
        -   in: id of user
            name: id
            required: true

    responses:
        200:
            description: Returns user information with matching ID
        404:
            description: No user exists with that ID
    """

    user = db.session.scalars(db.select(User).filter_by(id=user_id).limit(1)).first()
    if user:
        return jsonify({"code": 200, "data": user.json()})
    return jsonify({"code": 404, "message": "User does not exist."}), 404


# check user password
@app.route("/user/login/<string:email>", methods=["POST"])
def login(email):
    """
    Check user credentials

    ---
    parameters:
        - name: email
          in: path
          description: Email of the user
          required: true
          schema:
              type: string
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        bid_amount:
                            type: number
                            format: float
                            description: Amount of the bid
                            example: 100.0
                        auction_id:
                            type: integer
                            description: ID of the auction associated with the bid
                            example: 123
                        user_id:
                            type: integer
                            description: ID of the user placing the bid
                            example: 456
    responses:
        201:
            description: Bid created successfully
        400:
            description: Bid has already been placed or bad request
        500:
            description: Internal server error

    """

    user = db.session.scalars(db.select(User).filter_by(email=email).limit(1)).first()
    if user:
        data = request.get_json()
        password = data["password"]
        if check_password(password, user.getPasswordHash()):
            return jsonify(
                {"code": 200, "message": "User authenticated.", "data": user.json()}
            )
        else:
            return jsonify({"code": 401, "message": "Incorrect password."}), 401
    return jsonify({"code": 404, "message": "User does not exist."}), 404


# create user
@app.route("/user/<string:email>", methods=["POST"])
def create_user(email):
    """
    Create user
    ---
    parameters:
      - name: email
        in: path
        description: Email of the user
        required: true
        schema:
          type: string
      - name: user_data
        in: body
        description: User data for creating a new user
        required: true
        schema:
          type: object
          properties:
            password:
              type: string
              description: The user's password
            phone_number:
              type: string
              description: The user's phone number
            first_name:
              type: string
              description: The user's first name
            last_name:
              type: string
              description: The user's last name
            gender:
              type: string
              description: The user's gender (M/F)
            address:
              type: string
              description: The user's address
            account_type:
              type: string
              description: The type of user account
            profile_picture:
              type: string
              description: URL or path to the user's profile picture
    responses:
        201:
            description: User created
        400:
            description: Email is already in use
        500:
            description: An error occurred while creating user
    """

    if db.session.scalars(db.select(User).filter_by(email=email).limit(1)).first():
        return (
            jsonify(
                {
                    "code": 400,
                    "data": {"email": email},
                    "message": "Email already in use.",
                }
            ),
            400,
        )

    data = request.get_json()
    data["password"] = hash_password(data["password"])
    user = User(email, **data)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return (
            jsonify(
                {
                    "code": 500,
                    "data": {"email": email},
                    "message": "An error occured while creating user",
                    "error": str(e),
                }
            ),
            500,
        )

    return jsonify({"code": 201, "data": user.json()}), 201


# edit user data
@app.route("/user/<string:email>", methods=["PUT"])
def edit_user(email):
    """
    Edit user data
    ---
    responses:
        200:
            description: User updated successfully
        404:
            description: User does not exist
        500:
            description: An error occurred while updating the user
    """

    user = db.session.query(User).filter_by(email=email).first()

    if not user:
        return jsonify({"code": 404, "message": "User not found."}), 404

    data = request.get_json()

    # Update user attributes based on the provided data
    for key, value in data.items():
        setattr(user, key, value)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while updating the user.",
                    "error": str(e),
                }
            ),
            500,
        )

    return (
        jsonify(
            {"code": 200, "data": user.json(), "message": "User updated successfully."}
        ),
        200,
    )


# delete user
@app.route("/user/<string:email>", methods=["DELETE"])
def delete_user(email):
    """
    Delete User
    ---
    responses:
        200:
            description: User deleted successfully
        404:
            description: User does not exist
        500:
            description: An error occurred while deleting the user
    """

    user = db.session.query(User).filter_by(email=email).first()

    if not user:
        return jsonify({"code": 404, "message": "User not found."}), 404

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "code": 500,
                    "data": {"user_email": email},
                    "message": "An error occurred while deleting the user.",
                    "error": str(e),
                }
            ),
            500,
        )

    return jsonify({"code": 200, "message": "User deleted successfully."}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
