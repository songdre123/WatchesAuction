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

