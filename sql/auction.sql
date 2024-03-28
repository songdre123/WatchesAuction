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
    watch_image1 VARCHAR(500) NOT NULL,
    watch_image2 VARCHAR(500) NOT NULL,
    watch_image3 VARCHAR(500) NOT NULL,
    stripe_product_id VARCHAR(500) DEFAULT NULL
);

INSERT INTO Auction (auction_item, start_time, end_time, start_price, manufacture_year, current_price, auction_winner_id, auction_status, watch_ref, watch_condition, watch_brand, watch_box_present, watch_papers_present, watch_image1, watch_image2, watch_image3, stripe_product_id) 
VALUES 
('Sample Item', '2024-03-11 12:00:00', '2024-03-12 12:00:00', 100.00, 2022, 120.00, NULL, 1, 'Sample Ref', 'Sample Condition', 'Sample Brand', TRUE, TRUE, 'image1.jpg', 'image2.jpg', 'image3.jpg', NULL);
