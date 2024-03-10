from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from invokes import invoke_http
#pip3 install flask flask-mail
from mailbox import Message
from jinja2 import Environment, FileSystemLoader
import os
from flasgger import Swagger
from db_config import set_database_uri

'''
API Endpoints:
1. GET /notification/<string:email> - Get all notification that belongs to a user (email)
2. POST /notification/createNotification - create notification in the database  
3. POST /notification/sendEmail - sending a email to the receipient regarding update on his bid


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
    notification_type VARCHAR(50) NOT NULL COMMENT '(outbid, winandpayremind, paysucess,rollbackandpayremind, schedulesuccess)',
    time_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_unread INT DEFAULT 1
);

scenario when user will receive the notification 
1) outbid- when someone out bidded the customer (highest bid changed). send to previous person with highest bid 
2) winandpayremind/rollbackandpayremind- when the person win the bid and it will tell the user to pay 
3) paysucess-notify user when payment is successful 
4) schedulesuccess - notifiy user about successful schedule of collection time

5) auctionstartfail - notify the seller when auction did not start successfully
6) auctionstarted - notify the seller when auction started successfully
7) auctionendfail - notify the seller when auction did not end successfully
8) auctionended - notify the seller when auction end successfully


'''
########## initiate flask ##########
app = Flask(__name__)  # initialize a flask application

path = "Notification"
set_database_uri(app, path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

password="password@0000"
db = SQLAlchemy(app)

########## initiate swagger ##########
# Initialize flasgger 
app.config['SWAGGER'] = {
    'title': 'Notification microservice API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Allows create and retrieve of notification. Additionally, it sends email to the user.'
}
swagger = Swagger(app)

########## declaring mail ##########

app.config['MAIL_SERVER']="smtp.office365.com"
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME'] = "watchauctiononlineplatform@outlook.com"
app.config['MAIL_PASSWORD'] = "password@0000"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL']= True
mail=Mail(app)

########## notification customisation ##########
notification_header="Notification for item: "

subheader={
    "outbid":"Oh No! Hurry!", 
    "winandpayremind":"Congratulations!",
    "paysucess":"Payment success!",
    "rollbackandpayremind":"Congratulations!",
    "schedulesuccess":"Schedule success!",
    "auctionstartfail": "Fail to start Auction :( " ,
    "auctionstarted": "Auction has started!" ,
    "auctionendfail": " Fail to end Auction :(  " ,
    "auctionended": " Auction has started! " 
}

briefMessage={
    "outbid":"Out bidded for item: ", 
    "winandpayremind":"Congratulations on winning the item: ",
    "paysucess":"Payment success for the item: ",
    "rollbackandpayremind":"Congratulations on winning the item: ",
    "schedulesuccess":"You have schedule a time slot to collect the item: ",
    "auctionstartfail": "There is an error in starting your auction for item: " ,
    "auctionstarted": "We have successfully started your auction for item: " ,
    "auctionendfail": " There is an error in ending your auction for item:  " ,
    "auctionended": " We have successfully ended your auction for item: " 
}

notification_body={
    "outbid":"The item that you have recently bidded for has been outbidded by an annoymous bidder. Do log into our Watch Auction Online Platform to place a higher bid.", 

    "winandpayremind":"Congratulation on winning the bid! Do log into our Watch Auction Online platform and pay for the item within 1 hour. Or else, you may lose your item and the item will be offered to the second highest bidder.",

    "paysucess":"We have sucessfully receive your payment for the item. Do log into our Watch Auction Online Platform to schedule a timing for the collection of the watch! ",

    "rollbackandpayremind":"Congratulation on winning the bid! As the highest bidder has given up the offer, the item will be offered to you! Do log into our Watch Auction Online platform and pay for the item within 1 hour. Or else, you may lose your item and the item will be offered to the second highest bidder.",

    "schedulesuccess":"Do take note of the allocated time that you have indicated for the item collection. Vist our website to check the collection point with the seller!",

    "auctionstartfail":"There seems to be an error starting the auction for your item mentioned above. Do log into our website to check on your auction. ",

    "auctionstarted":"Your auction for the following item has open successfully for users to bid for your item. We will send you another email to notify you when the auction has ended. ",

    "auctionendfail":" There seems to be an error ending the auction for your item mentioned above. Do log into our website to check on your auction. ",

    "auctionended":"Your auction for the following item has ended successfully. Do log into our website to check on your auction and the winner's bid!. "

}



########## database ##########
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

########## all endpoint URL needed ##########
user_url="http://localhost:5000/user"
auction_url="http://localhost:5001/auction"
notification_url="http://localhost:5004/notification"


#1. GET /notification/<string:email> - Get all notification that belongs to a user (email)
@app.route('/notification/<string:email>')
def find_notification_by_email(email):
    """
    Get all notification by user email
    ---
    parameters:
        -   name: email
            in: path
            type: string
            required: true
            description: The user's email
    responses:
        200:
            description: retrieve all the notification that user has using the email passed in
        404:
            description: There is no such user. User does not exist
        404-2:
            description: There is no such notification for this user.

    """

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
    #get all the notification that below to the specify user from the database
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
    """
    Create a notification into the database
    ---
    requestBody:
        description: notification creation detail
        required: true
        content:
            application/json:
                schema:
                    properties:
                        recipient_id: 
                            type: integer
                            description: recipient_id
                        auction_id: 
                            type: integer
                            description: auction_id
                        notification_type: 
                            type: string
                            description: notification_type

    responses:
        201:
            description: notification created for user
        404:
            description: either user or auction does not exist
        500:
            description: Internal server error. An error occurred add new notification to database

    """

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
    
    #initialise new notification
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

    }"""
#POST /notification/sendEmail - sending a email to the receipient regarding update on his bid
@app.route('/notification/sendEmail', methods=['POST'])
def sendEmail():
    """
    Create a notification and send it to the user. the notification will be based on the notification type passed in the request body
    ---
    requestBody:
        description: notification creation detail
        required: true
        content:
            application/json:
                schema:
                    properties:
                        recipient:
                            type: object
                            properties:
                                code:
                                    type: integer
                                data:
                                    type: object
                                    properties:
                                        account_status:
                                            type: integer
                                        account_type:
                                            type: string
                                        address:
                                            type: string
                                        email:
                                            type: string
                                        first_name:
                                            type: string
                                        gender:
                                            type: string
                                        id:
                                            type: integer
                                        last_name:
                                            type: string
                                        password:
                                            type: string
                                        phone_number:
                                            type: string
                                        profile_picture:
                                            type: string
                                        registration_date:
                                            type: string
                                            format: date-time
                        auction:
                            type: object
                            properties:
                                code:
                                    type: integer
                                data:
                                    type: object
                                    properties:
                                        auction_id:
                                            type: integer
                                        auction_item:
                                            type: string
                                        current_price:
                                            type: number
                                        end_time:
                                            type: string
                                            format: date-time
                                        start_price:
                                            type: number
                                        start_time:
                                            type: string
                                            format: date-time
                        type:
                            type: string
                        

    responses:
        404:
            description: either user or auction does not exist

    """
    email_info = request.get_json()
    # print(email_info)
    #check if both recipient and auction are valid
    recipient_code=email_info["recipient"]["code"]
    auction_code=email_info["auction"]["code"]

    if recipient_code not in range(200,300) or auction_code not in range(200,300):
        return jsonify({
            "code":404,
            "data":{},
            "message": "either user or auction does not exist.",
            "error": "not found",
        }),400
    
    #creating the body of notification/email
    sender_email = "watchauctiononlineplatform@outlook.com"
    recipient_email =  email_info["recipient"]["data"]["email"]
    # print(recipient_email)
    subject = notification_header+email_info["auction"]["data"]["auction_item"]

    #content for email body 
    schedule=""
    if "schedule" in email_info:
        schedule=email_info["schedule"]
    email_content = {
        "subheader": subheader[email_info["type"]],
        "auctionItem": email_info["auction"]["data"]["auction_item"],
        "briefMessage": briefMessage[email_info["type"]],
        "bodyMessage": notification_body[email_info["type"]],
        "schedule":schedule
    }
    # print(email_content)

    ##config and render the email template 
    # Configure Jinja2
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))

    # Get the template
    template = env.get_template('confirmEmailTemplate.html')

    # Render the template with content
    html_content = template.render(**email_content)

    # Set up the SMTP server
    smtp_server = 'smtp-mail.outlook.com'
    port = 587
    username = "watchauctiononlineplatform@outlook.com" # Update with your Outlook email
    password = 'password@0000'  # Update with your Outlook password

    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

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
        print("Error in sending email")
        return 'Error: ' + str(e)
    
    

if __name__ == "__main__": # execute this program only if it is run as a script (not by 'import')    
    app.run(port=5004, debug=True)
