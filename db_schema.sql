-- Drop existing database if it exists
DROP DATABASE IF EXISTS meditation_app;

-- Create the new database
CREATE DATABASE meditation_app;

-- Use the new database
USE meditation_app;

-- Drop existing tables if they exist to avoid conflicts
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Meditations;
DROP TABLE IF EXISTS UserFeedback;
DROP TABLE IF EXISTS UsageReports;
DROP TABLE IF EXISTS Achievements;
DROP TABLE IF EXISTS Subscriptions;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Roles;
DROP TABLE IF EXISTS MeditationSessions;

-- Create Roles table
CREATE TABLE Roles (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(50) UNIQUE NOT NULL
);

-- Insert roles into Roles table
INSERT INTO Roles (RoleName) VALUES ('Admin'), ('User');

-- Create Customers table (formerly Users)
CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    RoleID INT NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
);

-- Create Staff table
CREATE TABLE Staff (
    StaffID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    RoleID INT NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
);

-- Create Categories table
CREATE TABLE Categories (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50),
    Description TEXT
);

-- Create Meditations table
CREATE TABLE Meditations (
    MeditationID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    CategoryID INT,
    Category VARCHAR(50),
    TextContent TEXT,
    AudioFilePath VARCHAR(255),
    VisualContentPath VARCHAR(255),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- Create MeditationSessions table
CREATE TABLE MeditationSessions (
    SessionID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    MeditationID INT NOT NULL,
    SessionDate DATE NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (MeditationID) REFERENCES Meditations(MeditationID),
    UNIQUE (CustomerID, SessionDate) -- Ensures one session per day per customer
);

-- Create UserFeedback table
CREATE TABLE UserFeedback (
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    MeditationID INT NOT NULL,
    Rating INT, -- (Rating BETWEEN 1 AND 5) -- To be handled by application logic
    Comments TEXT,
    SubmittedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (MeditationID) REFERENCES Meditations(MeditationID)
);

-- Create UsageReports table
CREATE TABLE UsageReports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    MeditationID INT NOT NULL,
    SessionDate TIMESTAMP,
    EngagementLevel VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (MeditationID) REFERENCES Meditations(MeditationID)
);

-- Create Achievements table
CREATE TABLE Achievements (
    AchievementID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    Type VARCHAR(50),
    Description TEXT,
    AchievedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Create Subscriptions table
CREATE TABLE Subscriptions (
    SubscriptionID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    PlanType VARCHAR(50),
    StartDate TIMESTAMP,
    EndDate TIMESTAMP,
    Status VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Create Payments table
CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    Amount DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    PaymentDate TIMESTAMP,
    Status VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Indexing
CREATE INDEX idx_customer_id_meditations ON Meditations(CustomerID);
CREATE INDEX idx_customer_id_userfeedback ON UserFeedback(CustomerID);
CREATE INDEX idx_customer_id_usagereports ON UsageReports(CustomerID);
CREATE INDEX idx_customer_id_achievements ON Achievements(CustomerID);
CREATE INDEX idx_customer_id_subscriptions ON Subscriptions(CustomerID);
CREATE INDEX idx_customer_id_payments ON Payments(CustomerID);
