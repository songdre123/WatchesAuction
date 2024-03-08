from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from flasgger import Swagger
import requests

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SWAGGER"] = {
    "title": "ProcessBids microservice API",
    "version": 1.0,
    "openapi": "3.0.2",
    "description": "Authenticate Bid"}
swagger = Swagger(app)

######################################################################################
# Function to get start price of auction
def get_auction_start_price(auction_id):
    response = requests.get(f"http://localhost:5001/auction/{auction_id}")
    if response.status_code == 200:
        return response.json()["data"]["start_price"]
    else:
        return None
    
# Function to create bid
def create_bid(auction_id, user_id, bid_amount):
    create_bid_response = requests.post(
        f"http://localhost:5002/bid/{auction_id}",
        json={"auction_id": auction_id, "user_id": user_id, "bid_amount": bid_amount}
    )

    if create_bid_response.status_code == 201:
        return jsonify(
            {
                "code": 200, 
                "message": "Authenticated Bid Created"
            }
        ), 200
    else:
        
        return jsonify(
            {
                "code": create_bid_response.status_code, 
                "message": "Error creating bid in the Bids microservice"
            }
        ), create_bid_response.status_code

# Function to update auction
def update_auction(auction_id, user_id, bid_amount):
    update_auction_response = requests.put(
        f"http://localhost:5001/auction/{auction_id}",
        json={"auction_winner_id": user_id, "current_price": bid_amount}
    )
    
    if update_auction_response.status_code == 200:
        return jsonify(
            {
                "code": 200,
                "message": "Auction Updated & Reflected",
            }
        ), 200
    else:
        return (
            jsonify(
                {
                    "code": update_auction_response.status_code,
                    "message": "Error updating auction data",
                }
            ), update_auction_response.status_code
        )
    

######################################################################################

# Authenticate Bid, Places Bid, Updates Auction
@app.route("/authbid" , methods=["POST"])
def authenticate_bid():
    """
    Authenticate a bid by comparing the bid amount with the current highest bid for the specified auction.
    If the new bid is higher, create the bid. Once Bid is created, update Auction with new highest bid (user_id and current_price)

    ---
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        auction_id:
                            type: integer
                        user_id:
                            type: integer
                        bid_amount:
                            type: number
                            format: float
    responses:
        200:
            description: Bid Authenticated & Updated in Auction
        400:
            description: Bid amount is not higher than the current highest bid
        404:
            description: No bids found for the specified auction ID
        500:
            description: Internal server error
    """

    data = request.json
    auction_id = data.get("auction_id")
    user_id = data.get("user_id")
    bid_amount = data.get("bid_amount")


    bids_response = requests.get(f"http://localhost:5002/bid/all/{auction_id}")
    # Proceed to process bids if there are existing bids
    if bids_response.status_code == 200 and bids_response.json()["data"]["bids"]:
        highest_bid_response = requests.get(f"http://localhost:5002/bid/highest/{auction_id}")

        if highest_bid_response.status_code == 200:
            highest_bid_amount = highest_bid_response.json()["data"]["highest_bid"][0]["bid_amount"]

            if bid_amount > highest_bid_amount:
                #bid authenticated
                create_bid_response = create_bid(auction_id, user_id, bid_amount)
                if create_bid_response.status_code == 200:
                    update_auction(auction_id, user_id, bid_amount)
                
            else:
                return jsonify({"code": 400, "message": "Bid amount is not higher than the current highest bid"}), 400
        else:
            #error retrieving the highest bid
            return jsonify({"code": highest_bid_response.status_code, "message": "Error retrieving highest bid information"}), highest_bid_response.status_code

    # No existing bids, compare with start price to process bid
    elif bids_response.status_code == 404:
        start_price = get_auction_start_price(auction_id)

        if start_price is not None and bid_amount > start_price:
            #bid authentiated
            create_bid_response = create_bid(auction_id, user_id, bid_amount)
            if create_bid_response.status_code == 200:
                update_auction(auction_id, user_id, bid_amount)
            
        else:
            #bid not higher than start price
            return jsonify({"code": 400, "message": "Bid amount is not higher than the start price"}), 400
    else:
        return jsonify({"code": bids_response.status_code, "message": "Error retrieving bids information"}), bids_response.status_code

    return jsonify({"code": 200, "message": "Bid Authenticated & Created. Notification sent."}), 200
    

if __name__ == '__main__':
    app.run(port=5006, debug=True)