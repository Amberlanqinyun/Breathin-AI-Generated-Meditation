Use meditation_app;
-- Create Users table
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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
    Category VARCHAR(50),
    TextContent TEXT,
    AudioFilePath VARCHAR(255),
    VisualContentPath VARCHAR(255),
    Duration INT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- Create UserFeedback table
CREATE TABLE UserFeedback (
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    MeditationID INT NOT NULL,
    Rating INT, -- (Rating BETWEEN 1 AND 5) -- To be handled by application logic
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
    Duration INT,
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

-- Indexing
CREATE INDEX idx_user_id_meditations ON Meditations(UserID);
CREATE INDEX idx_user_id_userfeedback ON UserFeedback(UserID);
CREATE INDEX idx_user_id_usagereports ON UsageReports(UserID);
CREATE INDEX idx_user_id_achievements ON Achievements(UserID);
CREATE INDEX idx_user_id_subscriptions ON Subscriptions(UserID);
CREATE INDEX idx_user_id_payments ON Payments(UserID);

