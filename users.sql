CREATE DATABASE IF NOT EXISTS `Users` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Users`;

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
(1, '1', NULL, 'email2@sample.com', 'Person', 'M', 9, '1', 'd74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1', '90909090', NULL, '2024-02-23 11:29:45');
