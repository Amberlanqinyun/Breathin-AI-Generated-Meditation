-- Insert into Users table
INSERT INTO Users (Username, Email, PasswordHash, SubscriptionStatus)
VALUES 
('john_doe', 'john.doe@example.com', 'hashed_password1', 'active'),
('jane_smith', 'jane.smith@example.com', 'hashed_password2', 'inactive'),
('alice_wonder', 'alice.wonder@example.com', 'hashed_password3', 'active'),
('bob_builder', 'bob.builder@example.com', 'hashed_password4', 'inactive');

-- Insert into Categories table
INSERT INTO Categories (Name, Description)
VALUES 
('Relaxation', 'Meditations focused on relaxation and calmness.'),
('Focus', 'Meditations aimed at improving focus and concentration.'),
('Sleep', 'Guided sessions to help you fall asleep.'),
('Stress Relief', 'Techniques to manage and reduce stress.');

-- Insert into Meditations table
INSERT INTO Meditations (UserID, Category, TextContent, AudioFilePath, VisualContentPath, Duration)
VALUES 
(1, 'Relaxation', 'Guided meditation for relaxation...', 'path/to/audio1.mp3', 'path/to/visual1.jpg', 10),
(2, 'Focus', 'Guided meditation to enhance focus...', 'path/to/audio2.mp3', 'path/to/visual2.jpg', 15),
(3, 'Sleep', 'Calm narration to help with sleep...', 'path/to/audio3.mp3', 'path/to/visual3.jpg', 20),
(4, 'Stress Relief', 'Breathing exercises to manage stress...', 'path/to/audio4.mp3', 'path/to/visual4.jpg', 12);

-- Insert into UserFeedback table
INSERT INTO UserFeedback (UserID, MeditationID, Rating, Comments)
VALUES 
(1, 1, 5, 'Very relaxing meditation.'),
(2, 2, 4, 'Helped me concentrate better.'),
(3, 3, 5, 'Fell asleep quickly, very soothing.'),
(4, 4, 3, 'Good, but not my favorite.');

-- Insert into UsageReports table
INSERT INTO UsageReports (UserID, MeditationID, SessionDate, Duration, EngagementLevel)
VALUES 
(1, 1, '2024-08-04 10:00:00', 10, 'High'),
(2, 2, '2024-08-04 11:00:00', 15, 'Medium'),
(3, 3, '2024-08-04 22:00:00', 20, 'High'),
(4, 4, '2024-08-04 15:00:00', 12, 'Low');

-- Insert into Achievements table
INSERT INTO Achievements (UserID, Type, Description)
VALUES 
(1, 'Streak', 'Completed 5 sessions in a row.'),
(2, 'Milestone', 'Reached 10 hours of meditation.'),
(3, 'Daily Practice', 'Practiced daily for a week.'),
(4, 'New User', 'Completed first meditation.');

-- Insert into Subscriptions table
INSERT INTO Subscriptions (UserID, PlanType, StartDate, EndDate, Status)
VALUES 
(1, 'Monthly', '2024-07-01', '2024-08-01', 'Active'),
(2, 'Yearly', '2024-01-01', '2025-01-01', 'Inactive'),
(3, 'Monthly', '2024-07-15', '2024-08-15', 'Active'),
(4, 'Yearly', '2024-01-15', '2025-01-15', 'Inactive');

-- Insert into Payments table
INSERT INTO Payments (UserID, Amount, PaymentMethod, PaymentDate, Status)
VALUES 
(1, 9.99, 'Credit Card', '2024-07-01', 'Completed'),
(2, 99.99, 'PayPal', '2024-01-01', 'Completed'),
(3, 9.99, 'Credit Card', '2024-07-15', 'Completed'),
(4, 99.99, 'PayPal', '2024-01-15', 'Completed');
