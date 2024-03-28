from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from flasgger import Swagger
import requests
import pika
import json
import amqp_connection
from os import environ

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SWAGGER"] = {
    "title": "ProcessBids microservice API",
    "version": 1.0,
    "openapi": "3.0.2",
    "description": "Authenticate Bid",
}
swagger = Swagger(app)


########################### urls ########################
auction_url=environ.get('auction_url') or 'http://localhost:5001/auction'
bids_url=environ.get('bids_url') or 'http://localhost:5002/bid'


######################################################################################
# RabbitMQ configuration
rabbitmq_connection = amqp_connection.create_connection() 
rabbitmq_channel = rabbitmq_connection.channel()


# Function to publish notification to RabbitMQ
def publish_notification(notification, recipient_id):
    exchangename = "notification_direct" 
    notification["recipient_id"] = recipient_id
    rabbitmq_channel.basic_publish(
        exchange=exchangename,
        body=json.dumps(notification),
        properties=pika.BasicProperties(delivery_mode = 2),
        routing_key='Notification'
    )


# Function to get start price of auction
def get_auction_start_price(auction_id):
    response = requests.get(f"{auction_url}/{auction_id}")
    if response.status_code == 200:
        return response.json()["data"]["start_price"]
    else:
        return None


# Function to create bid
def create_bid(auction_id, user_id, bid_amount):
    create_bid_response = requests.post(
        bids_url,
        json={"auction_id": auction_id, "user_id": user_id, "bid_amount": bid_amount}
    )

    if create_bid_response.status_code == 201:
        return jsonify({"code": 201, "message": "Authenticated Bid Created"}), 201
    elif create_bid_response.status_code == 400:
        return jsonify({"code": 400, "message": "Bad Request: Invalid bid data"}), 400
    else:
        return (
            jsonify(
                {
                    "code": create_bid_response.status_code,
                    "message": "Error creating bid in the Bids microservice",
                }
            ),
            create_bid_response.status_code,
        )


# Function to update auction
def update_auction(auction_id, user_id, bid_amount):
    update_auction_response = requests.put(
        f"{auction_url}/{auction_id}",
        json={"auction_winner_id": user_id, "current_price": bid_amount}
    )

    if update_auction_response.status_code == 200:
        return (
            jsonify(
                {
                    "code": 200,
                    "message": "Auction Updated & Reflected",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "code": update_auction_response.status_code,
                    "message": "Error updating auction data",
                }
            ),
            update_auction_response.status_code,
        )


######################################################################################


# Authenticate Bid, Places Bid, Updates Auction
@app.route("/authbid", methods=["POST"])
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

    bids_response = requests.get(f"{bids_url}/auction/{auction_id}")
    # Proceed to process bids if there are existing bids
    if bids_response.status_code == 200:
        highest_bid_response = requests.get(f"{bids_url}/highest/{auction_id}")

        if highest_bid_response.status_code == 200:
            highest_bid_amount = highest_bid_response.json()["data"]["highest_bid"][0][
                "bid_amount"
            ]

            if bid_amount > highest_bid_amount:
                # bid authenticated

                create_bid_response, create_bid_status_code = create_bid(
                    auction_id, user_id, bid_amount
                )

                # when bid is succesfully created, only then auction database will be updated
                if create_bid_status_code == 201:

                    # Notify previous highest bidder that he got outbidded
                    previous_highest_bidder = highest_bid_response.json()["data"][
                        "highest_bid"
                    ][0]["user_id"]
                    outbid_notification = {
                        "auction_id": auction_id,
                        "notification_type": "outbid",
                    }
                    publish_notification(outbid_notification, previous_highest_bidder)

                    # Update Auction to reflect latest bid
                    update_auction(auction_id, user_id, bid_amount)

            else:
                return (
                    jsonify(
                        {
                            "code": 400,
                            "message": "Bid amount is not higher than the current highest bid",
                        }
                    ),
                    400,
                )
        else:
            # Error retrieving the highest bid
            return (
                jsonify(
                    {
                        "code": highest_bid_response.status_code,
                        "message": "Error retrieving highest bid information",
                    }
                ),
                highest_bid_response.status_code,
            )

    # No existing bids, compare with start price to process bid
    elif bids_response.status_code == 404:
        start_price = get_auction_start_price(auction_id)

        if start_price is not None and bid_amount >= start_price:
            # Bid authenticated
            create_bid_response, create_bid_status_code = create_bid(
                auction_id, user_id, bid_amount
            )

            # when bid is succesfully created, only then auction database will be updated
            if create_bid_status_code == 201:

                # # Notify previous highest bidder that he got outbidded
                # previous_highest_bidder = highest_bid_response.json()["data"][
                #     "highest_bid"
                # ][0]["user_id"]
                # outbid_notification = {
                #     "auction_id": auction_id,
                #     "notification_type": "outbid",
                # }
                # publish_notification(outbid_notification, previous_highest_bidder)

                # Update Auction to reflect latest bid
                update_auction(auction_id, user_id, bid_amount)

        else:
            # Bid not higher than start price
            return (
                jsonify(
                    {
                        "code": 400,
                        "message": "Bid amount is not higher than the start price",
                    }
                ),
                400,
            )
    else:
        return (
            jsonify(
                {
                    "code": bids_response.status_code,
                    "message": "Error retrieving bids information",
                }
            ),
            bids_response.status_code,
        )

    return create_bid_response, create_bid_status_code


@app.route("/getAllAuctionAndUserhighestBidByUser/<int:user_id>")
def getAllAuctionAndUserhighestBidByUser(user_id):
    #checking for bids from the user
    user_id=int(user_id)
    getBid = requests.get(f"{bids_url}/GethighestBidsByUserId/{user_id}")
    if getBid.status_code not in range (200,300):
        return jsonify({"code": 404, "message": "No bids found for the specified user ID", "data":[]}),404
    print(getBid.json())
    allAuction=[]
    for bid in getBid.json()["data"]:
        auction_id=int(bid["auction_id"])
        auction = requests.get(f"{auction_url}/{auction_id}")
        if auction.status_code not in range(200,300) or auction.json()["data"]["auction_status"]!=1:
            continue
        auction=auction.json()["data"]
        auction["user_id"]=user_id
        auction["bid_amount"]=bid["bid_amount"]
        auction["bid_id"]=bid["bid_id"]
        allAuction.append(auction)
    print(allAuction)
    return jsonify({"code": 200, "message": "Get auction with user highest bids successfully", "data":allAuction}),200

        


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
