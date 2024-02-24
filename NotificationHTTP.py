from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from invokes import invoke_http


app = Flask(__name__)  # initialize a flask application

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/Notification'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

'''
API Endpoints:
1. GET /notification/<string:email> - Get all notification that belongs to a user (email)
2. POST /notification/createNotification - create notification in the database  


PORT: 5004
DATABASE: Notification
TABLE: notification
SQL Credentials: root:root
SQL Port: 3306


SQL Database creation code:
CREATE TABLE Notification(
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipient_id INT NOT NULL,
    auction_id INT,
    notification_type VARCHAR(50) NOT NULL COMMENT '(outbid, winandpayremind, payremind, paysucess,rollbackandpayremind)',
    time_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_unread INT DEFAULT 1
);
'''

#database
class Notification(db.Model):
    __tablename__ = 'Notification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipient_id = db.Column(db.Integer, nullable=False)
    auction_id = db.Column(db.Integer)
    notification_type = db.Column(db.String(255), nullable=False)
    time_sent = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    is_unread = db.Column(db.Integer, default=1)

    def __init__(self, recipient_id,notification_type, auction_id=None,is_unread=1):
        self.recipient_id = recipient_id
        self.notification_type = notification_type
        self.auction_id = auction_id
        self.is_unread = is_unread
        

    def json(self):
        return {
            "id": self.id,
            "recipient_id": self.recipient_id,
            "auction_id": self.auction_id,
            "notification_type": self.notification_type,
            "time_sent": self.time_sent.strftime('%Y-%m-%d %H:%M:%S'),
            "is_unread": self.is_unread,
        }

user_url="http://localhost:5000/user"
auction_url="http://localhost:5001/auction"
notification_url="http://localhost:5004/notification"

#1. GET /notification/<string:email> - Get all notification that belongs to a user (email)
@app.route('/notification/<string:email>')
def find_notification_by_email(email):
    #get customer details
    specify_user_url = f"{user_url}/{email}"
    response=invoke_http(specify_user_url,method="GET")
    
    code = response["code"]
    print(response)
    #if code is not ok  - user not exist
    if code not in range(200,300):
        print("there is some issue with getting the user. user may not exist")
        return jsonify(
        {
            "code": 404,
            "message": "User does not exist."
        }
    ), 404
    user_id=response["data"]["id"]
    allNotification = db.session.scalars(
        db.select(Notification).filter_by(recipient_id=user_id)).all()
    if len(allNotification):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "notifications": [notif.json() for notif in allNotification]
                },
                "message": "retrieved notification successfully.",
                "error": "NA"
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {},
            "message": "There is no notification for this user",
            "error": "no notification for this user"
        }
    ), 404


#2. POST /notification/createNotification - create notification in the database 
@app.route('/notification/createNotification', methods=['POST'])
def create_notification():
    new_notif = request.get_json()

    #check if user and auction exist
    are_exist=check_user_and_auction(new_notif["recipient_id"],new_notif["auction_id"])
    if not are_exist:
       return jsonify({
            "code":404,
            "data":new_notif,
            "message": "either user or auction does not exist.",
            "error": "not found",
        }),404
    

    new_notification = Notification(recipient_id=new_notif["recipient_id"], notification_type="outbid", auction_id=new_notif["auction_id"])
    try:
        db.session.add(new_notification)
        db.session.commit()
    except Exception as e:
        print(f"Notification microservice: fail to add new notification") 
        return jsonify({
            "code":500,
            "data":{},
            "message": "An error occurred add new notification to database.",
            "error": str(e),
        }),500
    
    return jsonify({
        "code":201,
        "data":new_notif,
        "message": "added notification into the database successfully.",
        "error": "NA",
    }),201


#check if user and auction exist
def check_user_and_auction(userID,auctionID):
    specify_user_url= f"{user_url}/{userID}"
    user_response=invoke_http(specify_user_url,method="GET")

    specify_auction_url= f"{user_url}/{auctionID}"
    auction_response=invoke_http(specify_auction_url,method="GET")

    if user_response["code"] in range(200,300) and auction_response["code"] in range(200,300):
        return True
    return False


if __name__ == "__main__": # execute this program only if it is run as a script (not by 'import')    
    app.run(port=5004, debug=True)

