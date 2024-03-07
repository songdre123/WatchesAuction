from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from invokes import invoke_http

from mailbox import Message

'''

scenario when user will receive the notification (notification Type)
1) outbid- when someone out bidded the customer (highest bid changed). send to previous person with highest bid 
2) winandpayremind/rollbackandpayremind- when the person win the bid and it will tell the user to pay 
3) paysucess-notify user when payment is successful 
4) schedulesuccess - notifiy user about successful schedule of collection time

'''
########## URL ##########
user_url="http://localhost:5000/user"
auction_url="http://localhost:5001/auction"
notification_url="http://localhost:5004/notification"


########## For RabbitMQ ##########
e_queue_name = 'Notification'

#1) receiveNotification- RabbitMQ consumer
def receiveNotification(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=e_queue_name, on_message_callback=callback, auto_ack=True)
        print('Notification microservice: Consuming from queue:', e_queue_name)
        channel.start_consuming() # an implicit loop waiting to receive messages; 
        #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    except pika.exceptions.AMQPError as e:
        print(f"Notification microservice: Failed to connect: {e}") 

    except KeyboardInterrupt:
        print("Notification microservice: Program interrupted by user.")



"""
########## initiate flask ##########
app = Flask(__name__)  # initialize a flask application

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root:root@localhost:3306/Notification"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

password = "password@0000"
db = SQLAlchemy(app)

########## declaring mail ##########

app.config["MAIL_SERVER"] = "smtp.office365.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "watchauctiononlineplatform@outlook.com"
app.config["MAIL_PASSWORD"] = "password@0000"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)

########## notification header ##########
notification_header = {
    "outbid": "Out bidded on Watch Auction online platform",
    "winandpayremind": "Watch Auction online platform",
    "paysucess": "Payment success on Watch Auction online platform",
    "rollbackandpayremind": "Watch Auction online platform",
}

notification_body = {
    "outbid": "your item has been outbidded by someone else in the auction. Do log into Watch Auction to bid for a higher price. You noose u lose bitch ",
    "winandpayremind": "uh uh u win liao but then horh u need to pay la. uh uh O$P$. no money no talk. one hand money, one hand your goods",
    "paysucess": "very very good u have successfull make the payment. but u jus to schedule the meeting. ",
    "rollbackandpayremind": "hello even since u have lost the auction but the previous person zao liao. so now u the win la. okay enough talk O$P$",
}


notification_body_real = {
    "outbid": "The item that you have recently bidded for has been outbidded by an annoymous bidder. Do log into our Watch Auction Online Platform to place a higher bid. \n \n Thank you and good luck on your bid \n \n Best Regards, \n Watch Auction",
    "winandpayremind": "Congratulation on winning the bid! Do log into our Watch Auction Online platform and pay for the item within 1 hour. Or else, you may lose your item and the item will be offered to the second highest bidder.\n \n Thank you for dealing with Watch Auction Online platform. \n \n Best Regards, \n Watch Auction",
    "paysucess": "We have sucessfully receive your payment for the item. Do log into our Watch Auction Online Platform to schedule a timing for the collection of the watch! \n \n Thank you for dealing with Watch Auction Online platform. \n \n Best Regards, \n Watch Auction",
    "rollbackandpayremind": "Congratulation on winning the bid! As the highest bidder has given up the offer, the item will be offered to you! Do log into our Watch Auction Online platform and pay for the item within 1 hour. Or else, you may lose your item and the item will be offered to the second highest bidder.\n \n Thank you for dealing with Watch Auction Online platform. \n \n Best Regards, \n Watch Auction",
}


# database
class Notification(db.Model):
    __tablename__ = "Notification"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipient_id = db.Column(db.Integer, nullable=False)
    auction_id = db.Column(db.Integer)
    notification_type = db.Column(db.String(255), nullable=False)
    time_sent = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    is_unread = db.Column(db.Integer, default=1)

    def __init__(self, recipient_id, notification_type, auction_id=None, is_unread=1):
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
            "time_sent": self.time_sent.strftime("%Y-%m-%d %H:%M:%S"),
            "is_unread": self.is_unread,
        }


########## all endpoint URL needed ##########
user_url = "http://localhost:5000/user"
auction_url = "http://localhost:5001/auction"
notification_url = "http://localhost:5004/notification"


# 1. GET /notification/<string:email> - Get all notification that belongs to a user (email)
@app.route("/notification/<string:email>")
def find_notification_by_email(email):
    # get customer details
    specify_user_url = f"{user_url}/{email}"
    response = invoke_http(specify_user_url, method="GET")

    code = response["code"]
    print(response)
    # if code is not ok  - user not exist
    if code not in range(200, 300):
        print("there is some issue with getting the user. user may not exist")
        return jsonify({"code": 404, "message": "User does not exist."}), 404
    user_id = response["data"]["id"]
    # get all the notification that below to the specify user from the database
    allNotification = db.session.scalars(
        db.select(Notification).filter_by(recipient_id=user_id)
    ).all()
    if len(allNotification):
        return jsonify(
            {
                "code": 200,
                "data": {"notifications": [notif.json() for notif in allNotification]},
                "message": "retrieved notification successfully.",
                "error": "NA",
            }
        )
    return (
        jsonify(
            {
                "code": 404,
                "data": {},
                "message": "There is no notification for this user",
                "error": "no notification for this user",
            }
        ),
        404,
    )


# 2. POST /notification/createNotification - create notification in the database
@app.route("/notification/createNotification", methods=["POST"])
def create_notification():
    new_notif = request.get_json()

    # check if user and auction exist
    are_exist = check_user_and_auction(
        new_notif["recipient_id"], new_notif["auction_id"]
    )
    if not are_exist:
        return (
            jsonify(
                {
                    "code": 404,
                    "data": new_notif,
                    "message": "either user or auction does not exist.",
                    "error": "not found",
                }
            ),
            404,
        )

    # initialise new notification
    new_notification = Notification(
        recipient_id=new_notif["recipient_id"],
        notification_type="outbid",
        auction_id=new_notif["auction_id"],
    )
    try:
        db.session.add(new_notification)
        db.session.commit()
    except Exception as e:
        print(f"Notification microservice: fail to add new notification")
        return (
            jsonify(
                {
                    "code": 500,
                    "data": {},
                    "message": "An error occurred add new notification to database.",
                    "error": str(e),
                }
            ),
            500,
        )

    return (
        jsonify(
            {
                "code": 201,
                "data": new_notif,
                "message": "added notification into the database successfully.",
                "error": "NA",
            }
        ),
        201,
    )


# check if user and auction exist
def check_user_and_auction(userID, auctionID):
    specify_user_url = f"{user_url}/{userID}"
    user_response = invoke_http(specify_user_url, method="GET")

    specify_auction_url = f"{user_url}/{auctionID}"
    auction_response = invoke_http(specify_auction_url, method="GET")

    if user_response["code"] in range(200, 300) and auction_response["code"] in range(
        200, 300
    ):
        return True
    return False


"""
{
    "recipient": {
        "code": 200,
        "data": {
            "account_status": 1,
            "account_type": "customer",
            "address": "123 Street,City",
            "email": "kaijie.wang.2022@smu.edu.sg",
            "first_name": "Kaijie",
            "gender": "M",
            "id": 1,
            "last_name": "Wang",
            "password": "password",
            "phone_number": "1234567890",
            "profile_picture": "https://example.com/profile.jpg",
            "registration_date": "2024-02-24 10:19:27"
            }
        },
        "auction": {
            "code": 200,
            "data": {
                "auction_id": 1,
                "auction_item": "Watch",
                "current_price": 120.0,
                "end_time": "2024-02-23 12:00:00",
                "start_price": 100.0,
                "start_time": "2024-02-23 10:00:00"
                }
            },
        "type": "outbid"

    }
"""

# POST /notification/sendEmail - sending a email to the receipient regarding update on his bid
@app.route("/notification/sendEmail", methods=["POST"])
def sendEmail():
    email_info = request.get_json()
    # print(email_info)

    # creating the body of notification/email
    sender_email = "watchauctiononlineplatform@outlook.com"
    recipient_email = email_info["recipient"]["data"]["email"]
    # print(recipient_email)
    subject = (
        notification_header[email_info["type"]]
        + "for item: "
        + email_info["auction"]["data"]["auction_item"]
    )
    print(subject)
    message = notification_body[email_info["type"]]
    print(message)

    # Set up the SMTP server
    smtp_server = "smtp-mail.outlook.com"
    port = 587
    username = (
        "watchauctiononlineplatform@outlook.com"  # Update with your Outlook email
    )
    password = "password@0000"  # Update with your Outlook password

    # Create message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(username, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("message has been sent successfully")
        return "message has been sent successfully"
    except Exception as e:
        return "Error: " + str(e)


if (
    __name__ == "__main__"
):  # execute this program only if it is run as a script (not by 'import')
    app.run(port=5004, debug=True)
"""
