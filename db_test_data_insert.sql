-- Insert dummy data into Users table
INSERT INTO Users (Username, Email, PasswordHash)
VALUES 
('user1', 'user1@example.com', 'passwordhash1'),
('user2', 'user2@example.com', 'passwordhash2'),
('user3', 'user3@example.com', 'passwordhash3');

-- Insert dummy data into Categories table
INSERT INTO Categories (Name, Description)
VALUES 
('Mindfulness', 'Meditations focused on mindfulness'),
('Relaxation', 'Meditations for relaxation and stress relief'),
('Focus', 'Meditations to improve focus and concentration');

-- Insert dummy data into Meditations table
INSERT INTO Meditations (UserID, CategoryID, Category, TextContent, AudioFilePath, VisualContentPath, Duration)
VALUES 
(1, 1, 'Mindfulness', 'Meditation content 1', 'audio1.mp3', 'visual1.jpg', 600),
(2, 2, 'Relaxation', 'Meditation content 2', 'audio2.mp3', 'visual2.jpg', 1200),
(3, 3, 'Focus', 'Meditation content 3', 'audio3.mp3', 'visual3.jpg', 900);

-- Insert dummy data into UserFeedback table
INSERT INTO UserFeedback (UserID, MeditationID, Rating, Comments)
VALUES 
(1, 1, 5, 'Very helpful!'),
(2, 2, 4, 'Relaxing, but a bit long.'),
(3, 3, 3, 'Good, but could be more focused.');

-- Insert dummy data into UsageReports table
INSERT INTO UsageReports (UserID, MeditationID, SessionDate, Duration, EngagementLevel)
VALUES 
(1, 1, '2024-01-01 10:00:00', 600, 'High'),
(2, 2, '2024-01-02 11:00:00', 1200, 'Medium'),
(3, 3, '2024-01-03 12:00:00', 900, 'Low');

-- Insert dummy data into Achievements table
INSERT INTO Achievements (UserID, Type, Description)
VALUES 
(1, 'Daily Streak', 'Completed 7 days of meditation'),
(2, 'First Meditation', 'Completed the first meditation'),
(3, 'Focus Master', 'Completed 10 focus meditations');

-- Insert dummy data into Subscriptions table
INSERT INTO Subscriptions (UserID, PlanType, StartDate, EndDate, Status)
VALUES 
(1, 'Monthly', '2024-01-01', '2024-01-31', 'Active'),
(2, 'Annual', '2024-01-01', '2024-12-31', 'Active'),
(3, 'Trial', '2024-01-01', '2024-01-07', 'Expired');

-- Insert dummy data into Payments table
INSERT INTO Payments (UserID, Amount, PaymentMethod, PaymentDate, Status)
VALUES 
(1, 9.99, 'Credit Card', '2024-01-01', 'Completed'),
(2, 99.99, 'PayPal', '2024-01-01', 'Completed'),
(3, 0.00, 'Trial', '2024-01-01', 'Completed');
