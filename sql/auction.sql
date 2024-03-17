CREATE DATABASE IF NOT EXISTS `Auction` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Auction`;
DROP TABLE IF EXISTS `Auction`;
CREATE TABLE IF NOT EXISTS `Auction` (
    auction_id INT AUTO_INCREMENT PRIMARY KEY,
    auction_item VARCHAR(255) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NULL,
    start_price FLOAT NOT NULL,
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