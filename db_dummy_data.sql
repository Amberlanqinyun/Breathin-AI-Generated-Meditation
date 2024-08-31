-- Insert dummy data into Roles
INSERT IGNORE INTO Roles (RoleName) VALUES 
('Admin'),
('User');

-- Insert dummy data into Users
INSERT IGNORE INTO Users (FirstName, LastName, Email, PasswordHash, RoleID) VALUES 
('John', 'Doe', 'john@example.com', '$2b$12$JxP1gD/J5vZjDHCmTVTnZ.eF1TV0QTFM.yjG3fxtKlzjY8Ph7G2LC', 2),  -- User role; Password: userpassword
('Jane', 'Smith', 'jane@example.com', '$2b$12$aP3sLDaV3i7AUpiMaU89J.0PGft/0FH2nOK9e0Zy3K3AfzLx/dCnq', 2),  -- User role; Password: userpassword
('Admin', 'User', 'admin@example.com', '$2b$12$GzP5tL3yV7zD/Cy1mA9eB.PjZfF2F1bS0UvxDbjlF8uP1U8jzGkXm', 1);  -- Admin role; Password: adminpassword

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
INSERT INTO MeditationSessions (UserID, MeditationID, SessionDateTime) VALUES 
(1, 1, '2023-07-01 08:00:00'),
(2, 2, '2023-07-02 09:00:00'),
(3, 3, '2023-07-03 10:00:00');

-- Insert dummy data into UserFeedback
INSERT INTO UserFeedback (UserID, MeditationID, Rating, Comments) VALUES 
(1, 1, 5, 'Very relaxing session.'),
(2, 2, 4, 'Helped me sleep better.'),
(3, 3, 3, 'It was okay, could be better.');

-- Insert dummy data into Achievements
INSERT INTO Achievements (UserID, Type, Description) VALUES 
(1, 'Milestone', 'Completed 10 meditation sessions.'),
(2, 'Consistency', 'Meditated every day for a week.'),
(3, 'Stress Free', 'Reduced stress levels significantly.');

-- Insert dummy data into Notifications
INSERT INTO Notifications (UserID, Details, NotificationTime, Status) VALUES 
(1, 'Welcome to the meditation app! Your journey begins now.', CURRENT_TIMESTAMP, 0),
(2, 'You have earned a new achievement: Consistency!', CURRENT_TIMESTAMP, 0);

