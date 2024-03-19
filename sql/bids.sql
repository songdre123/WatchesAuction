
CREATE DATABASE IF NOT EXISTS `bids` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `bids`;

DROP TABLE IF EXISTS `Bids`;
-- Create Bids table
CREATE TABLE IF NOT EXISTS `Bids` (
    bid_id INT AUTO_INCREMENT PRIMARY KEY,
    bid_amount FLOAT NOT NULL,
    auction_id INT NOT NULL,
    user_id INT NOT NULL,
    bid_time TIMESTAMP NOT NULL
);

-- Insert sample data into the Bids table
INSERT INTO Bids (bid_amount, auction_id, user_id, bid_time)
VALUES 
    (100.00, 1, 1, '2024-03-01 10:00:00'), -- Example bid for auction 1 by user 1 at a specific time
    (150.00, 2, 2, '2024-03-01 11:00:00'), -- Example bid for auction 2 by user 2 at a specific time
    (200.00, 1, 3, '2024-03-01 12:00:00'); -- Example bid for auction 1 by user 3 at a specific time



