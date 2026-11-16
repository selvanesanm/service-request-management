-- Service Request Management System database
-- WARNING: This drops only this project database and deletes its existing data.
DROP DATABASE IF EXISTS service_request_db;
CREATE DATABASE service_request_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE service_request_db;

CREATE TABLE serviceInfo (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    email VARCHAR(128),
    customerID INT UNSIGNED,
    companyName VARCHAR(191),
    customerManual TINYINT(1) NOT NULL DEFAULT 0,
    phoneNumber VARCHAR(30),
    productID VARCHAR(30),
    productType VARCHAR(128),
    issueDescription TEXT,
    locationID INT,
    locationName VARCHAR(128),
    regionID INT,
    regionName VARCHAR(64),
    issueImages TEXT,
    requestTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reqIpAddr VARCHAR(45),
    subcategoryID INT,
    subcategoryName VARCHAR(128),
    status ENUM('RECEIVED','ACKNOWLEDGED','WIP','TECH-COMPLETED','CLOSED') NOT NULL DEFAULT 'RECEIVED',
    userID INT,
    remarks TEXT,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closedAt DATETIME NULL,
    reopened TINYINT(1) NOT NULL DEFAULT 0,
    INDEX idx_request_time (requestTime),
    INDEX idx_status (status),
    INDEX idx_region (regionName),
    INDEX idx_location (locationName),
    INDEX idx_customer (customerID)
) ENGINE=InnoDB;

-- Sample data. Every application field is populated where applicable.
-- createdAt and id are generated automatically by MySQL.
INSERT INTO serviceInfo
(name,email,customerID,companyName,customerManual,phoneNumber,productID,productType,
 issueDescription,locationID,locationName,regionID,regionName,issueImages,requestTime,
 reqIpAddr,subcategoryID,subcategoryName,status,userID,remarks,closedAt,reopened)
VALUES
('Arun Kumar','arun.kumar@example.com',1001,'Chennai Tech Solutions',0,'9876543210','PRD1001','Laptop',
 'Laptop is not starting after the latest update.',1,'Chennai',3,'South','https://example.com/images/laptop.jpg','2026-11-10 09:15:00',
 '192.168.1.10',11,'Hardware','RECEIVED',501,'Customer requested a quick check.',NULL,0),
('Kaviya','kaviya@example.com',1002,'Salem Traders',0,'9876543211','PRD1002','Printer',
 'Printer is showing a paper jam error.',2,'Salem',3,'South','https://example.com/images/printer.jpg','2026-11-11 10:30:00',
 '192.168.1.11',12,'Printer Support','ACKNOWLEDGED',502,'Support team acknowledged the request.',NULL,0),
('Murugan','murugan@example.com',1003,'Madurai Textiles',0,'9876543212','PRD1003','Desktop',
 'Desktop is running slowly and freezing.',3,'Madurai',3,'South','https://example.com/images/desktop.jpg','2026-11-12 11:45:00',
 '192.168.1.12',13,'Performance','WIP',503,'Technician is checking system performance.',NULL,0),
('Priya','priya@example.com',1004,'Coimbatore Exports',0,'9876543213','PRD1004','Laptop',
 'Keyboard keys are not responding.',4,'Coimbatore',3,'South','https://example.com/images/keyboard.jpg','2026-11-08 14:00:00',
 '192.168.1.13',14,'Keyboard','TECH-COMPLETED',504,'Repair completed; waiting for customer confirmation.',NULL,0),
('Selvam','selvam@example.com',1005,'Trichy Industries',0,'9876543214','PRD1005','Scanner',
 'Scanner is not detected by the computer.',5,'Trichy',3,'South','https://example.com/images/scanner.jpg','2026-11-05 09:00:00',
 '192.168.1.14',15,'Connectivity','CLOSED',505,'Issue resolved and confirmed by customer.','2026-11-06 16:30:00',0),
('Nandhini','nandhini@example.com',1006,'Erode Garments',0,'9876543215','PRD1006','Monitor',
 'Monitor screen is flickering.',6,'Erode',3,'South','https://example.com/images/monitor.jpg','2026-11-13 08:20:00',
 '192.168.1.15',16,'Display','RECEIVED',506,'Awaiting technician assignment.',NULL,0),
('Vijay','vijay@example.com',1007,'Bengaluru Systems',0,'9876543216','PRD1007','Router',
 'Office network connection is unstable.',7,'Bengaluru',4,'SouthCentral','https://example.com/images/router.jpg','2026-11-09 13:10:00',
 '192.168.1.16',17,'Network','WIP',507,'Network diagnostics are in progress.',NULL,1),
('Deepa','deepa@example.com',1008,'Mumbai Services',0,'9876543217','PRD1008','Desktop',
 'Unable to log in with the assigned account.',8,'Mumbai',5,'West','https://example.com/images/login.jpg','2026-11-07 15:25:00',
 '192.168.1.17',18,'Account Access','CLOSED',508,'Password reset completed.','2026-11-07 17:00:00',0);
