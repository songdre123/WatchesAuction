from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)  # initialize a flask application

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/notification'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

'''
API Endpoints:
1. GET /notification/<string:email> - Get all notification that belongs to a user (email)
2. POST /notification/<string:email> - Create a new notication for that customer and send the notification to that customer via email 


scenario when user will receive the notification 
1) when someone out bidded the customer (highest bid changed). send to previous person with highest bid 
2) when the person win the bid and it will tell the user to pay 
3) notify user to pay 
4) notify user when payment is successful 




PORT: 5000
DATABASE: Users
TABLE: Users
SQL Credentials: root:root
SQL Port: 3306


SQL Database creation code:
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender CHAR(1),
    address VARCHAR(255),
    account_type VARCHAR(50) NOT NULL,
    profile_picture VARCHAR(255),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    account_status INT DEFAULT 1
);
'''