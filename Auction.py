from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # initialize a flask application

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/Auction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    #should include nullable=False to prevent error when executing different end points for important attribute such as start time start etc. 
    auction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auction_item = db.Column(db.String(255)) 
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    start_price = db.Column(db.Float)
    current_price = db.Column(db.Float)


    def __init__(self, auction_id,auction_item, start_time, end_time, start_price, current_price):
        #dont need include id coz its auto increment
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
@app.route('/auction/<int:auction_id>')
def find_by_auction_id(auction_id):
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
@app.route('/auction/<int:auction_id>', methods=['POST'])
def create_auction(auction_id):
    #when creating auction, i can still be creating the same item even though item already exist(2 items but different id no.(?)). TLDR i think there no point checking for id of auction. coz its auto increment in sql. when creating, seller wont ask to put id of auction
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
    #auction_id is auto increment. dont need to include. if done this way, user will need to provide auction id but they wont know. id is for us
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
@app.route('/auction/<int:auction_id>', methods=['PUT'])
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
@app.route('/auction/<int:auction_id>', methods=['DELETE'])
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
    app.run(port=5001, debug=True)
