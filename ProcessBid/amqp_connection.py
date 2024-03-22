"""
this file will be amended in the future if there is more use cases for ampq
for now is just notification - kaijie

exchange-
1) notification_direct

queue-
1) Notification
"""

import time
import pika
from os import environ

hostname = environ.get('rabbit_host') or 'localhost' # default hostname
port = environ.get('rabbit_port') or 5672          # default port
exchangename = "notification_direct" # exchange name
exchangetype = "direct"

# function to create a connection to the broker
def create_connection(max_retries=12, retry_interval=5):
    print('amqp_connection: Create_connection')
    
    retries = 0
    connection = None
    
    # loop to retry connection upto 12 times with a retry interval of 5 seconds
    while retries < max_retries:
        try:
            print('amqp_connection: Trying connection')
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=hostname, port=port,
                                 heartbeat=3600, blocked_connection_timeout=3600)) 
             
            print("amqp_connection: Connection established successfully")
            break  
        except pika.exceptions.AMQPConnectionError as e:
            print(f"amqp_connection: Failed to connect: {e}")
            retries += 1
            print(f"amqp_connection: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    if connection is None:
        raise Exception("Unable to establish a connection to RabbitMQ after multiple attempts")
    
    return connection

# function to check if the exchange exists
def check_exchange(channel, exchangename, exchangetype):
    try:    
        channel.exchange_declare(exchangename, exchangetype, durable=True, passive=True) 

    except Exception as e:
        print('Exception:', e)
        return False
    return True

def create_channel(connection):
    print('amqp_setup:create_channel')
    channel = connection.channel()
    # Set up the exchange if the exchange doesn't exist
    print('amqp_setup:create exchange')
    channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True) 
    return channel

#function to create queues
def create_queues(channel):
    print('amqp_setup:create queues')
    create_notification_queue(channel)


# function to create Error queue
def create_notification_queue(channel):
    print('amqp_setup:create_notification_queue')
    e_queue_name = 'Notification'
    channel.queue_declare(queue=e_queue_name, durable=True )
    channel.queue_bind(exchange=exchangename, queue=e_queue_name)

if __name__ == "__main__":
    connection = create_connection()
    channel = create_channel(connection)
    create_queues(channel)