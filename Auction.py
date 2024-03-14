from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db_config import set_database_uri

from flasgger import Swagger

import stripe

stripe.api_key = "rk_test_51OrZSVC6Ev8NcoAAsL8tWKsJQRCKKCry61vycl0wbj3FrQkTJ4qs56KKb9AXwAyW63S6no13Rws6Ao5kLWBm504M00jybuhTVc"


app = Flask(__name__)  # initialize a flask application

path = "Auction"
set_database_uri(app, path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize flasgger 
app.config['SWAGGER'] = {
    'title': 'Auction microservice API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Allows create, retrieve, update, and delete of Auctions'
}
swagger = Swagger(app)




#should test database see if this work. coz i tried and they say need configure mySQL strict mode. i configure the following then it works. if it works for you then its okay
"""
#the query below remove no zero date and make sure that auction can take in not null dates
SELECT @@sql_mode; #this line and the one below check the sql mode and its restriction
show variables like 'sql_mode' ; 
set global explicit_defaults_for_timestamp = ON;
#default sql_mode='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
set global sql_mode = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'; #this line and the one below do the ame thing 
SET @@sql_mode = sys.list_drop(@@sql_mode, 'NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO');
SELECT @@SESSION.sql_mode; #check the sql mode again

"""
'''
#auction closed = 0
#auction open = 1


SQL Set-Up code
CREATE TABLE Auction (
    auction_id INT AUTO_INCREMENT PRIMARY KEY,
    auction_item VARCHAR(255) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NULL,
    start_price FLOAT NOT NULL,
    current_price FLOAT NOT NULL,
    auction_winner_id INT,
    auction_status INT DEFAULT 1,
    watch_ref VARCHAR(255) NOT NULL,
    watch_condition VARCHAR(255) NOT NULL,
    watch_brand VARCHAR(255) NOT NULL,
    watch_box_present BOOLEAN NOT NULL,
    watch_papers_present BOOLEAN NOT NULL,
    watch_image1 VARCHAR(255) NOT NULL,
    watch_image2 VARCHAR(255) NOT NULL,
    watch_image3 VARCHAR(255) NOT NULL,
    stripe_product_id VARCHAR(255) DEFAULT NULL
);

'''

db = SQLAlchemy(app)

class Auction(db.Model):
    __tablename__ = 'Auction'
    #should include nullable=False to prevent error when executing different end points for important attribute such as start time start etc. 
    auction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auction_item = db.Column(db.String(255)) 
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    start_price = db.Column(db.Float)
    current_price = db.Column(db.Float)
    auction_winner_id = db.Column(db.Integer)
    auction_status = db.Column(db.Integer, default=1)
    watch_ref = db.Column(db.String(255))
    watch_condition = db.Column(db.String(255))
    watch_brand = db.Column(db.String(255))
    watch_box_present = db.Column(db.Boolean)
    watch_papers_present = db.Column(db.Boolean)
    watch_image1 = db.Column(db.String(255))
    watch_image2 = db.Column(db.String(255))
    watch_image3 = db.Column(db.String(255))
    stripe_product_id = db.Column(db.String(255))




    def __init__(self, auction_item, start_time, end_time, start_price, current_price, auction_winner_id, auction_status, watch_ref, watch_condition, watch_brand, watch_box_present, watch_papers_present, watch_image1, watch_image2, watch_image3):
        self.auction_item = auction_item
        self.start_time = start_time
        self.end_time = end_time
        self.start_price = start_price
        self.current_price = current_price
        self.auction_winner_id = auction_winner_id
        self.auction_status = auction_status
        self.watch_ref = watch_ref
        self.watch_condition = watch_condition
        self.watch_brand = watch_brand
        self.watch_box_present = watch_box_present
        self.watch_papers_present = watch_papers_present
        self.watch_image1 = watch_image1
        self.watch_image2 = watch_image2
        self.watch_image3 = watch_image3
        

    def json(self):
        return {
            "auction_id": self.auction_id,
            "auction_item": self.auction_item,
            "start_time": self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            "start_price": self.start_price,
            "current_price": self.current_price,
            "auction_winner_id": self.auction_winner_id,
            "auction_status": self.auction_status,
            "watch_condition": self.watch_condition,
            "watch_ref": self.watch_ref,
            "watch_brand": self.watch_brand,
            "watch_box_present": self.watch_box_present,
            "watch_papers_present": self.watch_papers_present,
            "watch_image1": self.watch_image1,
            "watch_image2": self.watch_image2,
            "watch_image3": self.watch_image3


        }

def store_winner(auction_id, auction_winner_id):
    auction = db.session.query(Auction).filter_by(auction_id=auction_id).first()
    auction.auction_winner_id = auction_winner_id
    auction.auction_status = 0
    db.session.commit()

# get all auctions
@app.route('/auction')
def get_all():
    """
    Get all Auctions
    ---
    responses:
        200:
            description: Return all Auctions
        404:
            description: There are no auctions
    """
    auctions = db.session.scalars(db.select(Auction)).all()

    if len(auctions):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "auctions": [auction.json() for auction in auctions]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no auctions."
        }
    ), 404


# get specific auction
@app.route('/auction/<int:auction_id>')
def find_by_auction_id(auction_id):
    """
    Find by Auctions
    ---
    parameters:
      - name: auction_id
        in: path
        description: ID of the auction to retrieve
        required: true
        schema:
          type: integer
    responses:
        200:
            description: Return specific auction
        404:
            description: Auction does not exist
    """
    auction = db.session.scalars(
        db.select(Auction).filter_by(auction_id=auction_id).limit(1)
    ).first()
    if auction:
        return jsonify(
            {
                "code": 200,
                "data": auction.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Auction does not exist."
        }
    ), 404


# create auction
@app.route('/auction', methods=['POST'])
def create_auction():
    """
    Create Auction
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              auction_item:
                type: string
              start_time:
                type: string
              end_time:
                type: string
              start_price:
                type: number
              current_price:
                type: number
              auction_winner_id:
                type: integer
              watch_ref:
                type: string
              auction_status:
                type: integer
              watch_condition:
                type: string
              watch_brand:
                type: string
              watch_box_present:
                type: boolean
              watch_papers_present:
                type: boolean
              watch_image1:
                type: string
              watch_image2:
                type: string
              watch_image3:
                type: string
    responses:
      201:
        description: Auction created
      400:
        description: Bad request
      500:
        description: An error occurred creating the auction
    """
    #when creating auction, i can still be creating the same item even though item already exist(2 items but different id no.(?)). TLDR i think there no point checking for id of auction. coz its auto increment in sql. when creating, seller wont ask to put id of auction

    data = request.get_json()
    #auction_id is auto increment. dont need to include. if done this way, user will need to provide auction id but they wont know. id is for us
    auction = Auction(**data)
    start_time = datetime.strptime(auction.start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(auction.end_time, '%Y-%m-%d %H:%M:%S')
    if start_time > end_time:
        return jsonify(
            {
                "code": 400,
                "data": {},
                "message": "Start time is after end time."
            }
        ), 400
    if auction.start_price < 0:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "auction_id": auction.auction_id
                },
                "message": "Start price cannot be negative."
            }
        ), 400
    if start_time < datetime.now():
        return jsonify(
            {
                "code": 400,
                "data": {
                    "auction_id": auction.auction_id
                },
                "message": "Start time must be later than the current time."
            }
        ), 400
    try:

        product = stripe.Product.create(
        name= auction.auction_item,
        type="good",
        description="Deposit for" + auction.auction_item
        )

        print("Product created:", product)

        # Store the product ID for later reference
        product_id = product.id
        auction.stripe_product_id = product_id

        # Create a price for the product
        price = stripe.Price.create(
            unit_amount=int(auction.start_price * 10),
            currency="sgd",
            product=product_id,
        )

        print("Price created:", price)
        db.session.add(auction)
        db.session.commit()




    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "auction_id": auction.auction_id
                },
                "message": "An error occurred creating the auction.",
                "error": str(e),
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": auction.json()
        }
    ), 201

#edit auction data
@app.route('/auction/<int:auction_id>', methods=['PUT'])
def edit_auction(auction_id):
    """
    Edit Auction
    ---
    parameters:
      - name: auction_id
        in: path
        description: ID of the auction to update
        required: true
        schema:
          type: integer
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        auction_item:
                            type: string
                        start_time:
                            type: string
                        end_time:
                            type: string
                        start_price:
                            type: number
                        current_price:
                            type: number
                        watch_ref:
                            type: string
                        auction_winner_id:
                            type: integer
                        auction_status:
                            type: integer
                        watch_condition:
                            type: string
                        watch_brand:
                            type: string
                        watch_box_present:
                            type: boolean
                        watch_papers_present:
                            type: boolean
                        watch_image1:
                            type: string
                        watch_image2:
                            type: string
                        watch_image3:
                            type: string
    responses:
        200:
            description: Auction updated
        400:
            description: Bad request
        404:
            description: Auction not found
        500:
            description: An error occurred updating the auction
    """
    auction = db.session.query(Auction).filter_by(auction_id=auction_id).first()

    if not auction:
        return jsonify({
            "code": 404,
            "message": "Auction not found."
        }), 404
    # if auction.auction_status == 0:
    #     return jsonify({
    #         "code": 400,
    #         "message": "Auction is closed."
    #     }), 400

    data = request.get_json()
    print(data)
    # Update user attributes based on the provided data
    for key, value in data.items():
        setattr(auction, key, value)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "data": {"auction_id": auction_id},
            "message": "An error occurred while updating the auction.",
            "error": str(e)
        }), 500

    return jsonify({
        "code": 200,
        "data": auction.json(),
        "message": "Auction updated successfully."
    }), 200

#delete auction
@app.route('/auction/<int:auction_id>', methods=['DELETE'])
def delete_auction(auction_id):
    """
    Delete Auction
    ---
    parameters:
      - name: auction_id
        in: path
        description: ID of the auction to delete
        required: true
        schema:
          type: integer
    responses:
        200:
            description: Auction deleted
        404:
            description: Auction not found
        500:
            description: An error occurred deleting the auction
    """
    auction = db.session.query(Auction).filter_by(auction_id=auction_id).first()

    if not auction:
        return jsonify({
            "code": 404,
            "message": "Auction not found."
        }), 404

    try:
        db.session.delete(auction)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "data": {"auction_id": auction_id},
            "message": "An error occurred while deleting the auction.",
            "error": str(e)
        }), 500

    return jsonify({
        "code": 200,
        "message": "Auction deleted successfully."
    }), 200
#function that closes auction when the passed time is greater than the end time
def close_auction():
    """
    Close Auction
    ---
    responses:
        200:
            description: Auction closed

            
    """
    auctions = db.session.query(Auction).filter(Auction.end_time < datetime.now()).all()
    for auction in auctions:
        auction.auction_status = 0
        db.session.commit()
        #store_winner(auction.auction_id, auction.auction_winner_id)
    return jsonify({
        "code": 200,
        "message": "Auction closed successfully."
    }), 200
def open_auction():
    auctions = db.session.query(Auction).filter(Auction.start_time < datetime.now()).all()
    for auction in auctions:
        auction.auction_status = 1
        db.session.commit()
    return jsonify({
        "code": 200,
        "message": "Auction opened successfully."
    }), 200

#get all open auctions
@app.route('/open_auctions', methods=['GET'])
def get_open_auctions():
    """
    Get all Open Auctions
    ---
    responses:
        200:
            description: Return all Open Auctions
        404:
            description: There are no open auctions
    """
    auctions = db.session.query(Auction).filter_by(auction_status=1).all()

    if len(auctions):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "auctions": [auction.json() for auction in auctions]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no open auctions."
        }
    ), 404

#get all closed auctions
@app.route('/closed_auctions', methods=['GET'])
def get_closed_auctions():
    """
    Get all Closed Auctions
    ---
    responses:
        200:
            description: Return all Closed Auctions
        404:
            description: There are no closed auctions
    """
    auctions = db.session.query(Auction).filter_by(auction_status=0).all()

    if len(auctions):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "auctions": [auction.json() for auction in auctions]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no closed auctions."
        }
    ), 404









if __name__ == '__main__':
    app.run(port=5001, debug=True)
