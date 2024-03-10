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