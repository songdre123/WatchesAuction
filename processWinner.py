from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from invokes import invoke_http
import amqp_connection
import pika
import json

app = Flask(__name__)

connection = amqp_connection.create_connection() 

def check_auctions():
  # Check if the datetime matches the current time
  # If it does, call the process() function
  print("Checking auctions at: ", datetime.now())
  auctions = invoke_http("http://localhost:5001/auction", "get") #? maybe only get all auctions that have a certin status then split the below up so that it doesnt need to process all auctions
  five_seconds_ago = datetime.now() - timedelta(seconds=5)

  for auction in auctions['data']['auctions']:

    #?convert time into readable format
    end_time = datetime.strptime(auction['end_time'], '%Y-%m-%d %H:%M:%S')
    start_time = datetime.strptime(auction['start_time'], '%Y-%m-%d %H:%M:%S')

    #? if auction started then change status from 0 to 1
    if start_time <= five_seconds_ago and datetime.now() >= start_time:
      #? send put request to change status of auction from 0 to 1 to show that auction has started
      if auction['status'] == 0:
        auction['status'] = 1
        update_status = invoke_http("http://localhost:5001/auction", "put", json=auction.json())

        #? error handling for the put request
        if update_status['code'] != 200:
          email_seller("auctionstartfail")
        else:
          email_seller("auctionstarted")

    #? if auction ended then change status from 1 to 2 and process the top bidder (switch the if statements)
    elif end_time <= five_seconds_ago:
    # elif end_time <= five_seconds_ago and datetime.now() >= end_time:
      #? send put request to change status of auction from 1 to 2 to show that auction has ended
      if auction['status'] == 1:
        #? process the top bidder of the auctionl
        process(auction)
        auction['status'] = 2
        update_status = invoke_http("http://localhost:5001/auction", "put", json=auction.json())

        #? error handling for the put request
        if update_status['code'] != 200:
          email_seller("auctionendfail")
        else:
          email_seller("auctionended") #! maybe can send the seller a list of all the bids that was received for this auction?
        # if payment not made, rollback the auction
        auction_id = auction['auction_id']
        #find next highest bidder from this auction
    else:
      # case where auction is still ongoing
      pass 
  pass


def process(auction):
  exchangename = "notification_direct" 

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
    email_seller("nowinner")


def email_seller(notification_type):
  exchangename = "notification_direct" 
  seller_id = 1  #! REPLACE with the actual seller id
  message = {
    "recipient_id": seller_id,
    "auction_id": auction['auction_id'],
    "notification_type": notification_type #! REPLACE with the actual notification type
  }
  message = json.dumps(message)
  channel.basic_publish(exchange=exchangename, body=message, properties=pika.BasicProperties(delivery_mode = 2),routing_key="Notification")

if __name__ == '__main__':
  scheduler = BackgroundScheduler()
  scheduler.add_job(check_auctions, 'interval', seconds=5)  # Run the code every 5 seconds
  scheduler.start()
  app.run(port=5005)