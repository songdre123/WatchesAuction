CREATE DATABASE IF NOT EXISTS `Schedule` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE Schedule;
CREATE TABLE Schedule (
    auction_id INT PRIMARY KEY,
    user_id INT,
    collection_time TIMESTAMP NULL
);