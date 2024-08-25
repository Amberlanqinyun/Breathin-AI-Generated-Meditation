-- Insert dummy data into Roles
INSERT IGNORE INTO Roles (RoleName) VALUES 
('Admin'),
('User');

-- Insert dummy data into Users
INSERT IGNORE INTO Users (FirstName, LastName, Email, PasswordHash, RoleID) VALUES 
('John', 'Doe', 'john@example.com', 'hashed_password1', 2),  -- User role
('Jane', 'Smith', 'jane@example.com', 'hashed_password2', 2),  -- User role
('Admin', 'User', 'admin@example.com', 'hashed_password3', 1);  -- Admin role

-- Insert dummy data into Admins
INSERT IGNORE INTO Admins (FirstName, LastName, Email, PasswordHash, RoleID) VALUES 
('Alice', 'Admin', 'alice.admin@example.com', 'hashed_password4', 1),
('Bob', 'Admin', 'bob.admin@example.com', 'hashed_password5', 1);

-- Insert dummy data into Categories
-- Insert dummy data into Categories
INSERT INTO Categories (Name, Description) VALUES 
('Mindfulness', 'Meditations for mindfulness and being present.'),
('Relaxation', 'Relaxation techniques to relieve stress.'),
('Sleep', 'Guided meditations for better sleep.'),
('Breathing', 'Breathing exercises to calm the mind.'),
('Focus', 'Meditations to improve concentration.'),
('Gratitude', 'Practices to cultivate gratitude.'),
('Visualization', 'Guided imagery for relaxation.'),
('Stress Relief', 'Meditations to reduce stress.');

-- Insert dummy data into Meditations
INSERT INTO Meditations (CategoryID, TextContent, AudioFilePath, VisualContentPath) VALUES 
(1, 'Mindfulness Peace Within', 'static/music/mindfulness_peace_within.mp3', NULL),
(1, 'Mindfulness Serenity Now', 'static/music/mindfulness_serenity_now.mp3', NULL),
(2, 'Relaxation Calm Waters', 'static/music/relaxation_calm_waters.mp3', NULL),
(2, 'Relaxation Ocean Breeze', 'static/music/relaxation_ocean_breeze.mp3', NULL),
(3, 'Sleep Dreamland', 'static/music/sleep_dreamland.mp3', NULL),
(3, 'Sleep Night Sky', 'static/music/sleep_night_sky.mp3', NULL),
(4, 'Breathing Deep Inhale', 'static/music/breathing_deep_inhale.mp3', NULL),
(4, 'Breathing Slow Exhale', 'static/music/breathing_slow_exhale.mp3', NULL),
(5, 'Focus Clarity Flow', 'static/music/focus_clarity_flow.mp3', NULL),
(5, 'Focus Mindful Attention', 'static/music/focus_mindful_attention.mp3', NULL),
(6, 'Gratitude Grateful Heart', 'static/music/gratitude_grateful_heart.mp3', NULL),
(6, 'Gratitude Warmth', 'static/music/gratitude_warmth.mp3', NULL),
(7, 'Visualization Mountain Path', 'static/music/visualization_mountain_path.mp3', NULL),
(7, 'Visualization Sunset Beach', 'static/music/visualization_sunset_beach.mp3', NULL),
(8, 'Stress Relief Soothing Sounds', 'static/music/stress_relief_soothing_sounds.mp3', NULL),
(8, 'Stress Relief Forest Rain', 'static/music/stress_relief_forest_rain.mp3', NULL);

-- Insert dummy data into MeditationSessions
INSERT INTO MeditationSessions (UserID, MeditationID, SessionDate) VALUES 
(1, 1, '2023-07-01'),
(2, 2, '2023-07-02'),
(3, 3, '2023-07-03');

-- Insert dummy data into UserFeedback
INSERT INTO UserFeedback (UserID, MeditationID, Rating, Comments) VALUES 
(1, 1, 5, 'Very relaxing session.'),
(2, 2, 4, 'Helped me sleep better.'),
(3, 3, 3, 'It was okay, could be better.');

-- Insert dummy data into UsageReports
INSERT INTO UsageReports (UserID, MeditationID, SessionDate, EngagementLevel) VALUES 
(1, 1, '2023-07-01', 'High'),
(2, 2, '2023-07-02', 'Medium'),
(3, 3, '2023-07-03', 'Low');

-- Insert dummy data into Achievements
INSERT INTO Achievements (UserID, Type, Description) VALUES 
(1, 'Milestone', 'Completed 10 meditation sessions.'),
(2, 'Consistency', 'Meditated every day for a week.'),
(3, 'Stress Free', 'Reduced stress levels significantly.');

-- Insert dummy data into Subscriptions
INSERT INTO Subscriptions (UserID, PlanType, StartDate, EndDate, Status) VALUES 
(1, 'Monthly', '2023-06-01', '2023-07-01', 'Active'),
(2, 'Annual', '2023-01-01', '2024-01-01', 'Active'),
(3, 'Monthly', '2023-07-01', '2023-08-01', 'Inactive');

-- Insert dummy data into Payments
INSERT INTO Payments (UserID, Amount, PaymentMethod, PaymentDate, Status) VALUES 
(1, 9.99, 'Credit Card', '2023-06-01', 'Completed'),
(2, 99.99, 'PayPal', '2023-01-01', 'Completed'),
(3, 9.99, 'Credit Card', '2023-07-01', 'Failed');
