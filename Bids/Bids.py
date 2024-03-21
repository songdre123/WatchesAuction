from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flasgger import Swagger
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Flask CORS
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("dbURL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SWAGGER"] = {
    "title": "Bids microservice API",
    "version": 1.0,
    "openapi": "3.0.2",
    "description": "Allows create, retrieve, update, and delete bids \n Get highest bid and get bids of a specific auction",
}


swagger = Swagger(app)

"""
API Endpoints:
1. GET /bid - Get all bids
2. GET /bid/all/<int:auction_id> - Get all bids from a specific auction
3. GET /bid/highest/<int:auction_id> - Get highest bid from a specific auction
4. POST /bid/<int:bid_id> - Create a bid
5. PUT /bid/<int:bid_id> - Edit a bid
6. DELETE /bid/<int:bid_id> - Delete a user

PORT: 5002
DATABASE: bids
TABLE: Bids
SQL Credentials: root:password
SQL Port: 3306
SQL dbURL: mysql+mysqlconnector://root:password@localhost:3306/Bids
"""

db = SQLAlchemy(app)


class Bids(db.Model):
    __tablename__ = "Bids"

    bid_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    bid_amount = db.Column(db.Float, nullable=False)
    auction_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    bid_time = db.Column(db.TIMESTAMP, nullable=False)

    def __init__(self, bid_amount, auction_id, user_id, bid_time):
        self.bid_amount = bid_amount
        self.auction_id = auction_id
        self.user_id = user_id
        self.bid_time = bid_time

    def json(self):
        return {
            "bid_id": self.bid_id,
            "bid_amount": self.bid_amount,
            "auction_id": self.auction_id,
            "user_id": self.user_id,
            "bid_time": self.bid_time,
        }


# get all bids
@app.route("/bid")
def get_all_bids():
    """
    Get all bids
    ---
    responses:
        200:
            description: Return all bids
        404:
            description: No bids

    """
    bids_data = Bids.query.all()
    if len(bids_data):
        return jsonify(
            {"code": 200, "data": {"bids": [bid.json() for bid in bids_data]}}
        )
    return jsonify({"code": 404, "message": "There are no Bids"}), 404


# create a bid
@app.route("/bid", methods=["POST"])
def create_bid():
    """
    Create a new bid

    ---
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
                            example: 46
    responses:
        201:
            description: Bid created successfully
        400:
            description: Bid has already been placed or bad request
        500:
            description: Internal server error
            
    """
    try:
        data = request.json
        bid_amount = data.get("bid_amount")
        auction_id = data.get("auction_id")
        user_id = data.get("user_id")
        bid_time = datetime.now()

        # Create a new Bid object and add it to the database session
        new_bid = Bids(
            bid_amount=bid_amount,
            auction_id=auction_id,
            user_id=user_id,
            bid_time=bid_time,  # not necessary since bid_time will be auto based on the current datetime
        )
        db.session.add(new_bid)
        db.session.commit()

        return jsonify(
            {
                "code": 201,
                "data": {"bid_id": new_bid.bid_id},
                "message": "Bid created successfully",
            }
        ), 201
    except IntegrityError as e:
        # Handle integrity constraint violation (e.g., bid has already been placed)
        db.session.rollback()
        return jsonify(
            {
                "code": 400,
                "data": {"message": "Bid has already been placed"},
            }
        ), 400
    except Exception as e:
        # Handle other exceptions
        db.session.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {"message": "An error occurred while creating bid", "error": str(e)},
            }
        ), 500


# edit bid
@app.route("/bid/<int:bid_id>", methods=["PUT"])
def edit_bid(bid_id):
    """
    Edit an existing bid with the given bid ID

    ---
    parameters:
        - name: bid_id
          in: path
          description: ID of the bid to edit
          required: true
          schema:
              type: integer
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    type: object
                    description: Updated bid data
    responses:
        200:
            description: Bid updated successfully
        404:
            description: Bid not found
        500:
            description: Internal server error
            
    """
    bid = db.session.query(Bids).filter_by(bid_id=bid_id).first()

    # When bid cannot be found
    if not bid:
        return (
            jsonify(
                {
                    "code": 404,
                    "message": "Bid not found",
                }
            ),
            404,
        )

    data = request.get_json()

    for key, value in data.items():
        setattr(bid, key, value)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "code": 500,
                    "data": {"bid_id": bid_id},
                    "message": "An error occured while updating the bid",
                    "error": str(e),
                }
            ),
            500,
        )
    return (
        jsonify(
            {
                "code": 200,
                "data": bid.json(),
                "message": "Bid updated successfully",
            }
        ),
        200,
    )


# delete bid
@app.route("/bid/<int:bid_id>", methods=["DELETE"])
def delete_bid(bid_id):
    """
    Delete a bid with the given bid ID

    ---
    parameters:
        - name: bid_id
          in: path
          description: ID of the bid to delete
          required: true
          schema:
              type: integer
    responses:
        200:
            description: Bid deleted successfully
        404:
            description: Bid not found
        500:
            description: Internal server error
    """
    bid = db.session.query(Bids).filter_by(bid_id=bid_id).first()

    if not bid:
        return (
            jsonify(
                {
                    "code": 404,
                    "message": "Bid not found",
                }
            ),
            404,
        )

    try:
        db.session.delete(bid)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "code": 500,
                    "data": {"bid_id": bid_id},
                    "message": f"Failed to delete bid: {str(e)}",
                    "error": str(e),
                }
            ),
            500,
        )
    return (
        jsonify(
            {
                "code": 200,
                "data": bid.json(),
                "message": "Bid deleted successfully",
            }
        ),
        200,
    )


# get highest bid by auction_id, filter by earliest timestamp if there are more than one row for highest bid
@app.route("/bid/highest/<int:auction_id>")
def get_highest_bid(auction_id):
    """
    Get the highest bid for a specific auction ID

    ---
    parameters:
        - name: auction_id
          in: path
          description: ID of the auction to get the highest bid for
          required: true
          schema:
              type: integer
    responses:
        200:
            description: Highest bid found
        404:
            description: No bids found for the specified auction ID
        500:
            description: Internal server error

    """

    highest_bid_amount = (
        db.session.query(db.func.max(Bids.bid_amount))
        .filter_by(auction_id=auction_id)
        .scalar()
    )

    try:
        # Get the highest bid amount for the specified auction_id
        highest_bid_amount = (
            db.session.query(db.func.max(Bids.bid_amount))
            .filter_by(auction_id=auction_id)
            .scalar()
        )

        # If no bids are found for the specified auction_id, highest_bid_amount will be None
        if highest_bid_amount is not None:
            # Get the earliest bid time for the highest bid amount
            earliest_bid_time = (
                db.session.query(db.func.min(Bids.bid_time))
                .filter_by(auction_id=auction_id, bid_amount=highest_bid_amount)
                .scalar()
            )

            # Query the bids with the highest bid amount and earliest bid time
            highest_bids = Bids.query.filter_by(
                auction_id=auction_id,
                bid_amount=highest_bid_amount,
                bid_time=earliest_bid_time,
            ).all()

            # Return the highest bids as JSON response
            return (
                jsonify(
                    {
                        "code": 200,
                        "data": {"highest_bid": [bid.json() for bid in highest_bids]},
                    }
                ),
                200,
            )
        else:
            # No bids found for the specified auction_id
            return (
                jsonify(
                    {
                        "code": 404,
                        "message": "No bids found for the specified auction ID",
                    }
                ),
                404,
            )
    except Exception as e:
        # Handle any unexpected exceptions
        return (
            jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}),
            500,
        )


@app.route("/bid/all/<int:auction_id>")
def get_all_bids_from_auction(auction_id):
    """
    Get all bids from a specific auction ID

    ---
    parameters:
        - name: auction_id
          in: path
          description: ID of the auction to get all bids from
          required: true
          schema:
              type: integer
    responses:
        200:
            description: Bids found for the specified auction ID
            
        404:
            description: No bids found for the specified auction ID

    """

    bids_from_auction = Bids.query.filter_by(auction_id=auction_id).all()

    # Check if any bids were found for the specified auction ID
    if bids_from_auction:
        # If bids were found, return them in the response
        bids_data = [
            {
                "bid_id": bid.bid_id,
                "bid_amount": bid.bid_amount,
                "auction_id": bid.auction_id,
                "user_id": bid.user_id,
                "bid_time": bid.bid_time,
            }
            for bid in bids_from_auction
        ]
        return jsonify({"code": 200, "data": bids_data})
    else:
        # If no bids were found, return a 404 response
        return (
            jsonify(
                {"code": 404, "message": "No bids found for the specified auction ID"}
            ),
            404,
        )

@app.route("/bid/all/<int:user_id>")
def get_all_bids_by_user(user_id):
    """
    Get all bids from a specific user ID

    ---
    parameters:
        - name: user_id
          in: path
          description: ID of the user to get all bids from
          required: true
          schema:
              type: integer
    responses:
        200:
            description: Bids found for the specified user ID

        404:
            description: No bids found for the specified user ID

    """

    bids_by_user = Bids.query.filter_by(user_id=user_id).all()

    if bids_by_user:
        bids_data = [
            {
                "bid_id": bid.bid_id,
                "bid_amount": bid.bid_amount,
                "auction_id": bid.auction_id,
                "user_id": bid.user_id,
                "bid_time": bid.bid_time,
            }
            for bid in bids_by_user
        ]
        return jsonify({"code": 200, "data": bids_data})
    else:
        # If no bids were found, return a 404 response
        return (
            jsonify(
                {"code": 404, "message": "No bids found for the specified user ID"}
            ),
            404,
        )


if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host="0.0.0.0", port=5002, debug=True)
