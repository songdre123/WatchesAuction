
CREATE DATABASE IF NOT EXISTS `bids` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `bids`;

DROP TABLE IF EXISTS `Bids`;
-- Create Bids table
CREATE TABLE IF NOT EXISTS `Bids` (
    bid_id INT AUTO_INCREMENT PRIMARY KEY,
    bid_amount FLOAT NOT NULL,
    auction_id INT,
    user_id INT,
    bid_time TIMESTAMP NOT NULL,
    FOREIGN KEY (auction_id) REFERENCES Auction(auction_id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Insert sample data into the Bids table
INSERT INTO Bids (bid_amount, auction_id, user_id, bid_time)
VALUES 
    (100.0, 1, 1495768, 28383, '2023-12-01 10:00:00'),
    (150.0, 1, 2432348, 38492, '2023-12-01 10:15:00'),
    (200.0, 2, 1493839, 40593,'2023-12-02 09:30:00'),
    (180.0, 2, 3301938, 60293, '2023-12-02 09:45:00');


