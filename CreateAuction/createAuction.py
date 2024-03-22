from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from flasgger import Swagger
from os import environ

app = Flask(__name__)
CORS(app)

app.config["SWAGGER"] = {
    "title": "User microservice API",
    "version": 1.0,
    "openapi": "3.0.2",
    "description": "Allows interaction with the Users microservice",
}
swagger = Swagger(app)

########## URL ##########
auction_url=environ.get('auction_url') or 'http://localhost:5001/auction'
schedule_url=environ.get('schedule_url') or 'http://localhost:5003/schedule'


@app.route('/createAuction', methods=['POST'])
def createAuction():
    """
    Create auction and schedule for the new item
    ---
    parameters:
      - name: auction_data
        in: body
        description: User data for creating a new user
        required: true
        schema:
          type: object
          properties:
              auction_item:
                    type: string
                    description: The item being auctioned.
              start_time:
                type: string
                format: date-time
                description: The start time of the auction.
              end_time:
                type: string
                format: date-time
                description: The end time of the auction.
              start_price:
                type: number
                description: The starting price of the auction.
              current_price:
                type: number
                description: The current price of the auction.
              auction_winner_id:
                type: integer
                nullable: true
                description: The ID of the auction winner.
              auction_status:
                type: integer
                description: The status of the auction (0 = unopened, 1 = active, 2 = closed, -1 = no winner, -2 = winner has paid.).
              watch_ref:
                type: string
                description: The reference number of the watch.
              watch_condition:
                type: string
                description: The condition of the watch (e.g., new, used, like new).
              watch_brand:
                type: string
                description: The brand of the watch.
              watch_box_present:
                type: boolean
                description: Whether the watch box is present.
              watch_papers_present:
                type: boolean
                description: Whether the watch papers are present.
              watch_images:
                type: array
                items:
                  type: string
                minItems: 3
                maxItems: 3
                description: List of URLs or paths to the images of the watch.
              year:
                type: integer
                description: The year of the watch.
    responses:
        201:
            description: Auction and Schedule Created
        401:
            description: Error in Auction microservice
        402:
            description: Error in Schedule microservice
    """

    data = request.json
    auction_item = data.get('Watch_name')
    start_time = data.get('start_date')
    end_time = data.get('End_date')
    start_price = data.get('Minimum_bid')
    current_price = data.get('Minimum_bid')
    auction_winner_id = None
    auction_status = 0
    watch_ref = data.get('reference_number')
    watch_condition = data.get('Watch_condition')
    watch_brand = data.get('brand')
    watch_box_present = data.get('Watch_box')
    watch_papers_present = data.get('Watch_papers')
    watch_image1 = data.get('image_urls')[0]
    watch_image2 = data.get('image_urls')[1]
    watch_image3 = data.get('image_urls')[2]
    year = data.get('year')
    stripe_product_id = None

    auction_response = requests.post(
      auction_url,
      json={
        "auction_item": auction_item,
        "start_time": start_time,
        "end_time": end_time,
        "start_price": start_price,
        "current_price": current_price,
        "auction_winner_id": auction_winner_id,
        "auction_status": auction_status,
        "watch_ref": watch_ref,
        "watch_condition": watch_condition,
        "watch_brand": watch_brand,
        "watch_box_present": watch_box_present,
        "watch_papers_present": watch_papers_present,
        "watch_image1": watch_image1,
        "watch_image2": watch_image2,
        "watch_image3": watch_image3
        # "year": year,
      }
    )
    print(auction_response)
    if (auction_response.status_code == 201):
        # auction_id = auction_response.data['auction_id']
        auction_data = auction_response.json()
        auction_id = auction_data['data']['auction_id']
        schedule_response = requests.post(
          f"{schedule_url}/create/{auction_id}"
        )
        if (schedule_response.status_code == 201):
            return jsonify(
                {
                    "code": 201,
                    "message": "Auction and Schedule Created",
                }
            ), 201
        else:
          # handle schedule creation error
            return jsonify(
                {
                    "code": 402,
                    "message": "Error creating schedule in the Schedule microservice"
                }
            ), schedule_response.status_code

    else:
      # handle auction creation error
        return jsonify(
            {
                "code": 401,
                "message": "Error creating auction in the Auctions microservice"
            }
        ), auction_response.status_code


if __name__ == '__main__':
    app.run(port=5010, debug=True, host="0.0.0.0")