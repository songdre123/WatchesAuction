from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # initialize a flask application

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/Users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

'''
SQL Set-Up code
CREATE TABLE Auction (
    auction_id INT AUTO_INCREMENT PRIMARY KEY,
    auction_item VARCHAR(255) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    start_price FLOAT NOT NULL,
    current_price FLOAT NOT NULL
);

'''

db = SQLAlchemy(app)

class Auction(db.Model):
    __tablename__ = 'Auction'

    auction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auction_item = db.Column(db.String(255))
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    start_price = db.Column(db.Float)
    current_price = db.Column(db.Float)


    def __init__(self, auction_id,auction_item, start_time, end_time, start_price, current_price):
        self.auction_id = auction_id
        self.auction_item = auction_item
        self.start_time = start_time
        self.end_time = end_time
        self.start_price = start_price
        self.current_price = current_price

    def json(self):
        return {
            "auction_id": self.auction_id,
            "auction_item": self.auction_item,
            "start_time": self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            "start_price": self.start_price,
            "current_price": self.current_price
        }



# get all auctions
@app.route('/auction')
def get_all():
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
@app.route('/auction/<string:auction_id>')
def find_by_auction_id(auction_id):
    auction = db.session.scalars(
        db.select(auction).filter_by(auction_id=auction_id).limit(1)
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
@app.route('/user/<string:auction_id>', methods=['POST'])
def create_auction(auction_id):
    if (db.session.scalars(db.select(Auction).filter_by(auction_id=auction_id).limit(1)).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "auction_id": auction_id
                },
                "message": "Auction ID is already in use."
            }
        ), 400

    data = request.get_json()
    auction = Auction(auction_id, **data)

    try:
        db.session.add(auction)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "auction_id": auction_id
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
@app.route('/user/<string:auction_id>', methods=['PUT'])
def edit_auction(auction_id):
    auction = db.session.query(Auction).filter_by(auction_id=auction_id).first()

    if not auction:
        return jsonify({
            "code": 404,
            "message": "Auction not found."
        }), 404

    data = request.get_json()
    
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
@app.route('/user/<string:auction_id>', methods=['DELETE'])
def delete_auction(auction_id):
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



if __name__ == '__main__':
    app.run(port=5000, debug=True)
