from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from invokes import invoke_http
import amqp_connection
import pika
import json

app = Flask(__name__)

connection = amqp_connection.create_connection() 
channel = connection.channel()  


def check_auctions():
  # Check if the datetime matches the current time
  # If it does, call the process() function
  print("Checking auctions at: ", datetime.now())
  auctions = invoke_http("http://localhost:5001/auction", "get") #? maybe only get all auctions that are from today onwards to reduce complexity?
  five_seconds_ago = datetime.now() - timedelta(seconds=5)
  #! how many rollbacks are we handling? how to keep track of rollbacks?
  #! what is the rollback duration? (1Hr?)
  rollback_time = datetime.now() - timedelta(hours=1)
  five_seconds_ago_rollback = rollback_time - timedelta(seconds=5)
  for auction in auctions['data']['auctions']:
    end_time = datetime.strptime(auction['end_time'], '%Y-%m-%d %H:%M:%S')
    if end_time <= five_seconds_ago:
    # if end_time <= five_seconds_ago and datetime.now() >= end_time:
      # check the above if statement to ensure that it checks the 5 second window
      # case where auction has ended
      process(auction)
    elif end_time <= five_seconds_ago_rollback and rollback_time >= end_time:
      #! check if payment made so there is no need to rollback is there a variable for this?
      

      # if payment not made, rollback the auction
      auction_id = auction['auction_id']
      #find next highest bidder from this auction
    else:
      # case where auction is still ongoing
      pass 
  pass


def process(auction):
  exchangename = "notification_direct" 
  seller_id = 1  #! REPLACE with the actual seller id

  # check if there is a winner
  if auction['auction_winner_id'] != None:
    print("Winner for", auction['auction_id'] ,"is", auction['auction_winner_id'])
    # call AMQP to send a message to the winner
    message = {
      "recipient_id": auction['auction_winner_id'],
      "auction_id": auction['auction_id'],
      "notification_type": "winandpayremind"
    }
    message = json.dumps(message)
    channel.basic_publish(exchange=exchangename, body=message, properties=pika.BasicProperties(delivery_mode = 2),routing_key="Notification")
  else:
    print(auction['auction_id'], "has no winner")
    # call AMQP to send a message to the seller
    message = {
      "recipient_id": seller_id,
      "auction_id": auction['auction_id'],
      "notification_type": "informseller" #! REPLACE with the actual notification type
    }
    message = json.dumps(message)
    channel.basic_publish(exchange=exchangename, body=message, properties=pika.BasicProperties(delivery_mode = 2),routing_key="Notification")

if __name__ == '__main__':
  scheduler = BackgroundScheduler()
  scheduler.add_job(check_auctions, 'interval', seconds=5)  # Run the code every 5 seconds
  scheduler.start()
  app.run(port=5005)