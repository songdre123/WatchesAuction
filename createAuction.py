from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/createAuction', methods=['POST'])
def createAuction():
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
      "http://localhost:5001/auction",
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
        # "stripe_product_id": stripe_product_id
      }
    )
    print(auction_response)
    if (auction_response.status_code == 201):
        # auction_id = auction_response.data['auction_id']
        auction_data = auction_response.json()
        auction_id = auction_data['data']['auction_id']
        schedule_response = requests.post(
          f"http://localhost:5003/schedule/create/{auction_id}"
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
                    "code": schedule_response.status_code,
                    "message": "Error creating schedule in the Schedule microservice"
                }
            ), schedule_response.status_code

    else:
      # handle auction creation error
        return jsonify(
            {
                "code": auction_response.status_code,
                "message": "Error creating auction in the Auctions microservice"
            }
        ), auction_response.status_code


if __name__ == '__main__':
    app.run(port=5010, debug=True, host="0.0.0.0")