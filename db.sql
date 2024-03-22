############################################
#                 Users db                  #
############################################
DROP DATABASE IF EXISTS `Users`;
CREATE DATABASE IF NOT EXISTS `Users` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Users`;
DROP TABLE IF EXISTS `Users`;

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

INSERT INTO Users (account_status, account_type, address, email, first_name, gender, id, last_name, password, phone_number, profile_picture, registration_date)
VALUES
(1, 'Regular', 'Bencoolen Street 14', 'solaiym.2022@scis.smu.edu.sg', 'Solaiy', 'M', 1, 'Meyapan', '123', '88684378', NULL, '2024-02-21 22:15:49'),
(1, '1', NULL, 'email1@sample.com', 'Person', 'M', 2, '1', 'pass', '90909090', NULL, '2024-02-22 14:26:46'),
(1, '1', NULL, 'email2@sample.com', 'Person', 'M', 9, '1', 'd74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1', '90909090', NULL, '2024-02-23 11:29:45'),
(1, '1', NULL, 'wangkaijie2011@gmail.com', 'Person', 'M', 8, '1', 'd74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1', '90909090', NULL, '2024-02-23 11:29:45');


############################################
#                Auction db                #
############################################
DROP DATABASE IF EXISTS `Auction`;
CREATE DATABASE IF NOT EXISTS `Auction` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Auction`;
DROP TABLE IF EXISTS `Auction`;

CREATE TABLE Auction (
    auction_id INT AUTO_INCREMENT PRIMARY KEY,
    auction_item VARCHAR(255) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NULL,
    start_price FLOAT NOT NULL,
    manufacture_year INT NOT NULL,
    current_price FLOAT NOT NULL,
    auction_winner_id INT,
    auction_status INT DEFAULT 1,
    watch_ref VARCHAR(255) NOT NULL,
    watch_condition VARCHAR(255) NOT NULL,
    watch_brand VARCHAR(255) NOT NULL,
    watch_box_present BOOLEAN NOT NULL,
    watch_papers_present BOOLEAN NOT NULL,
    watch_image1 VARCHAR(255) NOT NULL,
    watch_image2 VARCHAR(255) NOT NULL,
    watch_image3 VARCHAR(255) NOT NULL,
    stripe_product_id VARCHAR(255) DEFAULT NULL
);

INSERT INTO Auction (auction_item, start_time, end_time, start_price, manufacture_year, current_price, auction_winner_id, auction_status, watch_ref, watch_condition, watch_brand, watch_box_present, watch_papers_present, watch_image1, watch_image2, watch_image3, stripe_product_id) 
VALUES 
('Sample Item', '2024-03-11 12:00:00', '2024-03-12 12:00:00', 100.00, 2022, 120.00, NULL, 1, 'Sample Ref', 'Sample Condition', 'Sample Brand', TRUE, TRUE, 'image1.jpg', 'image2.jpg', 'image3.jpg', NULL);



############################################
#                 Bids db                  #
############################################

DROP DATABASE IF EXISTS `bids`;
CREATE DATABASE IF NOT EXISTS `bids` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `bids`;
DROP TABLE IF EXISTS `Bids`;

-- Create Bids table
CREATE TABLE IF NOT EXISTS `Bids` (
    bid_id INT AUTO_INCREMENT PRIMARY KEY,
    bid_amount FLOAT NOT NULL,
    auction_id INT,
    user_id INT,
    bid_time TIMESTAMP NOT NULL
);

-- Insert sample data into the Bids table
INSERT INTO Bids (bid_amount, auction_id, user_id, bid_time)
VALUES 
    (100.00, 1, 1, '2024-03-01 10:00:00'), -- Example bid for auction 1 by user 1 at a specific time
    (150.00, 2, 2, '2024-03-01 11:00:00'), -- Example bid for auction 2 by user 2 at a specific time
    (200.00, 1, 3, '2024-03-01 12:00:00'); -- Example bid for auction 1 by user 3 at a specific time


############################################
#             Notification db              #
############################################

DROP DATABASE IF EXISTS `Notification`;
CREATE DATABASE IF NOT EXISTS `Notification` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Notification`;
DROP TABLE IF EXISTS `Notification`;

CREATE TABLE Notification(
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipient_id INT NOT NULL,
    auction_id INT,
    notification_type VARCHAR(50) NOT NULL COMMENT '(outbid, winandpayremind, paysucess,rollbackandpayremind, schedulesuccess ,auctionstartfail , auctionstarted , auctionendfail, auctionended)', 
    time_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_unread INT DEFAULT 1
);

INSERT INTO Notification (recipient_id, auction_id, notification_type, time_sent, is_unread) 
VALUES 
    (1, 123, 'outbid', '2024-03-10 09:00:00', 1),
    (2, 124, 'paysuccess', '2024-03-11 10:30:00', 1),
    (3, 999, 'auctionstarted', '2024-03-12 12:45:00', 1);



############################################
#               Schedule db                #
############################################

DROP DATABASE IF EXISTS `Schedule`;
CREATE DATABASE IF NOT EXISTS `Schedule` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Schedule`;
DROP TABLE IF EXISTS `Schedule`;

CREATE TABLE Schedule (
    auction_id INT PRIMARY KEY,
    user_id INT,
    collection_time TIMESTAMP NULL
);

INSERT INTO Schedule (auction_id, user_id, collection_time) 
VALUES 
    (1, 1001, '2024-03-25 10:00:00'),
    (2, 1002, '2024-03-26 11:30:00'),
    (3, 1003, '2024-03-27 12:45:00');