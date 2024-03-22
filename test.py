"""
use this file for testing the endpoint
delete after we have a working complex microservice which we can call/test - kaijie
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ
import pika
import json
import amqp_connection

app = Flask(__name__)
CORS(app)


user_url=environ.get('user_url')  or 'http://localhost:5000/user'
auction_url=environ.get('auction_url') or 'http://localhost:5001/auction'
notification_url=environ.get('notification_url') or 'http://localhost:5004/notification'

exchangename = "notification_direct" 
exchangetype = "direct" 


#create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

#testing notification see if rabbitMQ works -last test- 24 feb 2024
@app.route("/test")
def testNotification():
    if request.is_json:
        try:
            notif = request.get_json() 
            message=json.dumps(notif)
            print("\nReceived an notification in JSON:", notif)
            #publish to notification to create and send notification
            
            print(channel.basic_publish(exchange=exchangename, body=message, properties=pika.BasicProperties(delivery_mode = 2),routing_key="Notification") )
            
            return jsonify({
                "code": 200,        
                "message": "ok",
            }), 200
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "test.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,        
        "message": "Invalid JSON input: " + str(request.get_data()),
    }), 400





# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
  
