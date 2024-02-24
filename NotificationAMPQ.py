from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from invokes import invoke_http
import amqp_connection
import json
import pika
import os, sys
from invokes import invoke_http

'''
Functions (RabbitMQ)
1) receiveNotification- RabbitMQ consumer
1) callback(channel, method, properties, body)-function to call when there is a message published to notification
2) processNotif(recipient_id,auction_id,notification_type ) - process the notification received from the callback function 
3) customiseNotif(email, aution_item, notification_type) - send the notification through email 


scenario when user will receive the notification 
1) when someone out bidded the customer (highest bid changed). send to previous person with highest bid 
2) when the person win the bid and it will tell the user to pay 
3) notify user to pay 
4) notify user when payment is successful 

'''
########## different notification ##########
notification_type={
    "outbid":"has been outbidded by someone else in the auction. Do log into Watch Auction to bid for a higher price. You noose u lose bitch ", 
    "winandpayremind":"uh uh u win liao but then horh u need to pay la. uh uh O$P$. no money no talk. 一手交钱，一手交货",
    "payremind":"eh i tell u to pay right, why still havent pay later zavier come find u arh",
    "paysucess":"very very good u have successfull make the payment. but u jus to schedule the meeting. ",
    "rollbackandpayremind":"hello even since u have lost the auction but the previous person zao liao. so now u the win la. okay enough talk O$P$"
}


########## URL ##########
user_url="http://localhost:5000/user"
auction_url="http://localhost:5001/auction"
notification_url="http://localhost:5004/notification"


########## For RabbitMQ ##########
e_queue_name = 'Notification'

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
body json- 
{
    recipient_id: id
    auction_id: id
    notification_type: notif type (string)  <- must correspond to database shown above
}
"""
#this function create a log in notification database and send the email to user regarding specific message
def callback(channel, method, properties, body): 
    notif = json.loads(body) # notif will be in json format like the one in the docstring
    print("--JSON:", notif)

    #log the notification into data
    notification_response=invoke_http("http://localhost:5004/notification/createNotification", method="POST",json=notif)
    if notification_response["code"] not in range(200,300):
        print("unable to add into database")
        return
    
    #process to send the notiification to that email  
        #get the specify user email
    recipient_id=notif["recipient_id"]
    specify_user_url= f"{user_url}/{recipient_id}"
    user=invoke_http(specify_user_url,method="GET")
    

        #find the item name 
    aution_id=notif["recipient_id"]
    specify_auction_url= f"{user_url}/{aution_id}"
    auction=invoke_http(specify_auction_url,method="GET")

        #find notification type
    notif_type=notification_response["data"]["notification_type"]
    
    #proceed to send out the email
    is_send=processNotif(user,auction,notif_type)
    # print()


def processNotif(user,auction,notif_type):
    recipient_email=user["data"]["email"]
    auction_name=auction["data"]["auction_item"]
    notification_message=notification_type[notif_type]







if __name__ == "__main__": # execute this program only if it is run as a script (not by 'import')    
    print("Notification microservice: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("Notification microservice: Connection established successfully")
    channel = connection.channel()
    receiveNotification(channel)

