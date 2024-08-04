-- Create Users table
CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    SubscriptionStatus VARCHAR(50),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Meditations table
CREATE TABLE Meditations (
    MeditationID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    Category VARCHAR(50),
    TextContent TEXT,
    AudioFilePath VARCHAR(255),
    VisualContentPath VARCHAR(255),
    Duration INT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Categories table
CREATE TABLE Categories (
    CategoryID SERIAL PRIMARY KEY,
    Name VARCHAR(50),
    Description TEXT
);

-- Create UserFeedback table
CREATE TABLE UserFeedback (
    FeedbackID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    MeditationID INT REFERENCES Meditations(MeditationID),
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Comments TEXT,
    SubmittedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create UsageReports table
CREATE TABLE UsageReports (
    ReportID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    MeditationID INT REFERENCES Meditations(MeditationID),
    SessionDate TIMESTAMP,
    Duration INT,
    EngagementLevel VARCHAR(50)
);

-- Create Achievements table
CREATE TABLE Achievements (
    AchievementID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    Type VARCHAR(50),
    Description TEXT,
    AchievedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Subscriptions table
CREATE TABLE Subscriptions (
    SubscriptionID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    PlanType VARCHAR(50),
    StartDate TIMESTAMP,
    EndDate TIMESTAMP,
    Status VARCHAR(50)
);

-- Create Payments table
CREATE TABLE Payments (
    PaymentID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    Amount DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    PaymentDate TIMESTAMP,
    Status VARCHAR(50)
);
