
-- Drop existing database if it exists
DROP DATABASE IF EXISTS meditation_app;

-- Create the new database
CREATE DATABASE meditation_app;

-- Use the new database
USE meditation_app;

-- Drop existing tables if they exist to avoid conflicts
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Admin;
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

-- Create User table (formerly Customers)
CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Firstname VARCHAR(50) NOT NULL,
    Lastname VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    RoleID INT NOT NULL,
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
);

-- Create Admin table (formerly Staff)
CREATE TABLE Admin (
    AdminID INT AUTO_INCREMENT PRIMARY KEY,
    Firstname VARCHAR(50) NOT NULL,
    Lastname VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    RoleID INT NOT NULL,
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
    UserID INT NOT NULL,
    CategoryID INT,
    TextContent TEXT,
    AudioFilePath VARCHAR(255),
    VisualContentPath VARCHAR(255),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- Create MeditationSessions table
CREATE TABLE MeditationSessions (
    SessionID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    MeditationID INT NOT NULL,
    SessionDate DATE NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (MeditationID) REFERENCES Meditations(MeditationID),
    UNIQUE (UserID, SessionDate) -- Ensures one session per day per user
);

-- Create UserFeedback table
CREATE TABLE UserFeedback (
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    MeditationID INT NOT NULL,
    Rating INT, -- (Rating BETWEEN 1 AND 5) -- To be handled by application logic
    Comments TEXT,
    SubmittedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (MeditationID) REFERENCES Meditations(MeditationID)
);

-- Create UsageReports table
CREATE TABLE UsageReports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    MeditationID INT NOT NULL,
    SessionDate TIMESTAMP,
    EngagementLevel VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (MeditationID) REFERENCES Meditations(MeditationID)
);

-- Create Achievements table
CREATE TABLE Achievements (
    AchievementID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Type VARCHAR(50),
    Description TEXT,
    AchievedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Create Subscriptions table
CREATE TABLE Subscriptions (
    SubscriptionID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    PlanType VARCHAR(50),
    StartDate TIMESTAMP,
    EndDate TIMESTAMP,
    Status VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Create Payments table
CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Amount DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    PaymentDate TIMESTAMP,
    Status VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Indexing
CREATE INDEX idx_user_id_meditations ON Meditations(UserID);
CREATE INDEX idx_user_id_userfeedback ON UserFeedback(UserID);
CREATE INDEX idx_user_id_usagereports ON UsageReports(UserID);
CREATE INDEX idx_user_id_achievements ON Achievements(UserID);
CREATE INDEX idx_user_id_subscriptions ON Subscriptions(UserID);
CREATE INDEX idx_user_id_payments ON Payments(UserID);
