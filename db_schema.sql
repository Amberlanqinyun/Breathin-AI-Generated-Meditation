-- Drop existing database if it exists
DROP DATABASE IF EXISTS meditation_app;

-- Create the new database
CREATE DATABASE meditation_app;

-- Use the new database
USE meditation_app;

-- Drop existing tables if they exist to avoid conflicts
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Admins;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Meditations;
DROP TABLE IF EXISTS UserFeedback;
DROP TABLE IF EXISTS UsageReports;
DROP TABLE IF EXISTS Achievements;
DROP TABLE IF EXISTS Subscriptions;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Roles;
DROP TABLE IF EXISTS MeditationSessions;
DROP TABLE IF EXISTS Notifications;
DROP TABLE IF EXISTS ContactUs;

-- Create Roles table
CREATE TABLE Roles (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(50) UNIQUE NOT NULL
);

-- Insert roles into Roles table
INSERT INTO Roles (RoleName) VALUES ('Admin'), ('User');

-- Create Users table
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    RoleID INT NOT NULL,
    banned TINYINT(1) DEFAULT 0,
    reset_token VARCHAR(255),
    reset_token_expiration DATETIME,
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
);

-- Create Admins table
CREATE TABLE Admins (
    AdminID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    RoleID INT NOT NULL,
    banned TINYINT(1) DEFAULT 0,
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
);

-- Create Categories table
CREATE TABLE Categories (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50),
    Description TEXT
);

-- Create Meditations table (no UserID needed)
CREATE TABLE Meditations (
    MeditationID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryID INT NOT NULL,
    TextContent TEXT,
    AudioFilePath VARCHAR(255),
    VisualContentPath VARCHAR(255),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

CREATE TABLE MeditationSessions (
    SessionID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    MeditationID INT NOT NULL,
    SessionDateTime DATETIME NOT NULL,  -- Include time to track multiple sessions in a day
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (MeditationID) REFERENCES Meditations(MeditationID)
);


-- Create UserFeedback table
CREATE TABLE UserFeedback (
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    MeditationID INT NOT NULL,
    Rating INT,
    Comments TEXT,
    SubmittedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (MeditationID) REFERENCES Meditations(MeditationID)
);

-- Create UsageReports table
CREATE TABLE UsageReports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    MeditationID INT NOT NULL,
    SessionDate TIMESTAMP,
    EngagementLevel VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (MeditationID) REFERENCES Meditations(MeditationID)
);

-- Create Achievements table
CREATE TABLE Achievements (
    AchievementID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Type VARCHAR(50),
    Description TEXT,
    AchievedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Create Subscriptions table
CREATE TABLE Subscriptions (
    SubscriptionID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    PlanType VARCHAR(50),
    StartDate TIMESTAMP,
    EndDate TIMESTAMP,
    Status VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Create Payments table
CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Amount DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    PaymentDate TIMESTAMP,
    Status VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Create ContactUs table
CREATE TABLE ContactUs (
    ContactID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Message TEXT NOT NULL,
    SubmittedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Notifications table
CREATE TABLE Notifications (
    NotificationID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Details TEXT NOT NULL,
    NotificationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Status TINYINT(1) DEFAULT 0,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Indexes
CREATE INDEX idx_user_id_userfeedback ON UserFeedback(UserID);
CREATE INDEX idx_user_id_usagereports ON UsageReports(UserID);
CREATE INDEX idx_user_id_achievements ON Achievements(UserID);
CREATE INDEX idx_user_id_subscriptions ON Subscriptions(UserID);
CREATE INDEX idx_user_id_payments ON Payments(UserID);
CREATE INDEX idx_user_id_notifications ON Notifications(UserID);
