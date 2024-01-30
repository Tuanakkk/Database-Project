DROP DATABASE IF EXISTS YemekSepetiDatabase;
CREATE DATABASE YemekSepetiDatabase;
USE YemekSepetiDatabase;

CREATE TABLE Customers (
    customerID INT AUTO_INCREMENT NOT NULL,
    address VARCHAR(200),
    customer_name VARCHAR(20),
    password VARCHAR(250),
    email VARCHAR(50),
    telephoneNumber INT,
    PRIMARY KEY (customerID)
);

CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT NOT NULL,
    totalAmount float,
    orderDate date,
    customerID int,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (customerID) REFERENCES Customers(customerID)
);

CREATE TABLE Payment (
    PaymentID INT AUTO_INCREMENT NOT NULL,
    amount float,
    payment_date VARCHAR(50),
    payment_type VARCHAR(20),
    orderID INT,
    PRIMARY KEY (PaymentID),
    FOREIGN KEY (orderID) REFERENCES Orders(OrderID)
);

CREATE TABLE Restaurant (
    restaurantID INT AUTO_INCREMENT NOT NULL,
    address VARCHAR(200),
    restaurant_name VARCHAR(20),
    telephoneNumber INT,
    openingTimes VARCHAR(50),
    closingTimes VARCHAR(50),
    openDays VARCHAR(50),
    PRIMARY KEY (restaurantID)
);

CREATE TABLE Reviews (
    reviewID INT AUTO_INCREMENT NOT NULL,
    customerID int,
    score int,
    customer_comment VARCHAR(200),
    review_date DATE,
    restaurantID INT,
    PRIMARY KEY (reviewID),
    FOREIGN KEY (customerID) REFERENCES Customers(customerID),
    FOREIGN KEY (restaurantID) REFERENCES Restaurant(restaurantID)
);

Create TABLE Menu (
    menuID INT AUTO_INCREMENT NOT NULL,
    menuName VARCHAR(50),
    menuPrice INT,
    RestaurantID INT,
    PRIMARY KEY (menuID),
    FOREIGN KEY (restaurantID) REFERENCES Restaurant(restaurantID)
);

-- Inserting 10 random values into the Customers table
INSERT INTO Customers (address, customer_name, password, email, telephoneNumber)
VALUES
    ('123 Main St', 'John Doe', 'admin', 'john.doe@email.com', 1234567890),
    ('456 Oak Ave', 'Jane Smith', 'admin', 'jane.smith@email.com', 9876543210),
    ('789 Pine Blvd', 'Alice Johnson', 'admin', 'alice.johnson@email.com', 5551234567),
    ('321 Elm Ln', 'Bob Anderson', 'admin', 'bob.anderson@email.com', 7890123456),
    ('567 Maple Rd', 'Emily White', 'admin', 'emily.white@email.com', 2345678901),
    ('890 Birch Dr', 'David Brown', 'admin', 'david.brown@email.com', 8765432109),
    ('432 Cedar St', 'Sarah Miller', 'admin', 'sarah.miller@email.com', 3456789012),
    ('654 Pineapple Ave', 'Michael Taylor', 'admin', 'michael.taylor@email.com', 9012345678),
    ('876 Orange Rd', 'Laura Davis', 'admin', 'laura.davis@email.com', 6789012345),
    ('987 Lemon Ln', 'Christopher Wilson', 'admin', 'christopher.wilson@email.com', 1237894560);



-- Inserting 10 random values into the Orders table
INSERT INTO Orders (totalAmount, orderDate, customerID)
VALUES
    (50.25, '2024-01-12', 1),
    (30.50, '2024-01-13', 2),
    (75.80, '2024-01-14', 3),
    (45.60, '2024-01-15', 4),
    (60.75, '2024-01-16', 5),
    (25.40, '2024-01-17', 6),
    (90.20, '2024-01-18', 7),
    (35.90, '2024-01-19', 8),
    (55.15, '2024-01-20', 9),
    (70.30, '2024-01-21', 10);


-- Inserting 10 random values into the Payment table
INSERT INTO Payment (amount, payment_date, payment_type, orderID)
VALUES
    (25.00, '2024-01-12', 'Credit Card', 1),
    (15.75, '2024-01-13', 'PayPal', 2),
    (40.20, '2024-01-14', 'Cash', 3),
    (30.50, '2024-01-15', 'Credit Card', 4),
    (50.80, '2024-01-16', 'Cash', 5),
    (20.30, '2024-01-17', 'Credit Card', 6),
    (75.90, '2024-01-18', 'PayPal', 7),
    (22.45, '2024-01-19', 'Cash', 8),
    (35.60, '2024-01-20', 'Credit Card', 9),
    (45.75, '2024-01-21', 'PayPal', 10);


-- Inserting 10 random values into the Restaurant table
INSERT INTO Restaurant (address, restaurant_name, telephoneNumber, openingTimes, closingTimes, openDays)
VALUES
    ('123 Oak St', 'Tasty Grill', 1234567890, '10:00 AM', '8:00 PM', 'Monday - Sunday'),
    ('456 Maple Ave', 'Spice Palace', 9876543210, '11:30 AM', '9:00 PM', 'Tuesday - Sunday'),
    ('789 Pineapple Blvd', 'Pizza Haven', 5551234567, '12:00 PM', '10:00 PM', 'Monday - Saturday'),
    ('321 Lemon Ln', 'Sushi Express', 7890123456, '1:00 PM', '9:30 PM', 'Wednesday - Sunday'),
    ('567 Orange Rd', 'Burger Joint', 2345678901, '11:00 AM', '10:30 PM', 'Monday - Friday'),
    ('890 Cherry Dr', 'Italian Delight', 8765432109, '12:30 PM', '8:30 PM', 'Thursday - Sunday'),
    ('432 Grape St', 'Mexican Fiesta', 3456789012, '2:00 PM', '9:00 PM', 'Monday - Saturday'),
    ('654 Berry Ave', 'Healthy Bites', 9012345678, '10:30 AM', '7:30 PM', 'Monday - Sunday'),
    ('876 Plum Rd', 'Asian Fusion', 6789012345, '12:00 PM', '10:00 PM', 'Tuesday - Sunday'),
    ('987 Pear Ln', 'Seafood Delight', 1237894560, '3:00 PM', '8:00 PM', 'Wednesday - Saturday');


-- Inserting 10 random values into the Reviews table
INSERT INTO Reviews (customerID, score, customer_comment, review_date, restaurantID)
VALUES
    (1, 4, 'Great food and service!', '2024-01-12', 1),
    (2, 5, 'Amazing flavors, highly recommended!', '2024-01-13', 2),
    (3, 3, 'Decent experience, but could be better.', '2024-01-14', 3),
    (4, 4, 'Friendly staff and tasty dishes.', '2024-01-15', 4),
    (5, 5, 'Excellent service and a diverse menu.', '2024-01-16', 5),
    (6, 2, 'Disappointed with the quality of food.', '2024-01-17', 6),
    (7, 4, 'Impressed with the ambiance and flavors.', '2024-01-18', 7),
    (8, 5, 'Healthy options and delicious choices.', '2024-01-19', 8),
    (9, 3, 'Average experience, nothing special.', '2024-01-20', 9),
    (10, 4, 'Fresh seafood and great presentation.', '2024-01-21', 10);

INSERT INTO Menu (menuName, menuPrice, restaurantID)
VALUES
    ('Burger', 10, 1),
    ('Pizza', 15, 2),
    ('Salad', 8, 3),
    ('Pasta', 12, 4),
    ('Sushi', 20, 5),
    ('Steak', 25, 6),
    ('Chicken Alfredo', 18, 7),
    ('Fish Tacos', 14, 8),
    ('Vegetarian Stir Fry', 16, 9),
    ('Ice Cream Sundae', 7, 10);



