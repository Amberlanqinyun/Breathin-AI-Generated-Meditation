-- Drop existing database if it exists
DROP DATABASE IF EXISTS meditation_app;

-- Create the new database
CREATE DATABASE meditation_app;

-- Use the new database
USE meditation_app;

-- Drop existing tables if they exist to avoid conflicts
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Meditations;
DROP TABLE IF EXISTS UserFeedback;
DROP TABLE IF EXISTS Achievements;
DROP TABLE IF EXISTS MeditationSessions;
DROP TABLE IF EXISTS Notifications;
DROP TABLE IF EXISTS Roles;
DROP TABLE IF EXISTS Payments;

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

-- Create Categories table
CREATE TABLE Categories (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50),
    Description TEXT
);

-- Create Meditations table
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

-- Create MeditationSessions table
CREATE TABLE MeditationSessions (
    SessionID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    MeditationID INT NOT NULL,
    SessionDateTime DATETIME NOT NULL,  -- Ensure to keep this format as your Python code expects it
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

-- Create Achievements table
CREATE TABLE Achievements (
    AchievementID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Type VARCHAR(50),
    Description TEXT,
    AchievedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
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
CREATE INDEX idx_user_id_achievements ON Achievements(UserID);
CREATE INDEX idx_user_id_notifications ON Notifications(UserID);
