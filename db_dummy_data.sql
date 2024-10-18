-- Insert dummy data into Roles
INSERT IGNORE INTO Roles (RoleName) VALUES 
('Admin'),
('User');

-- Insert dummy data into Users
INSERT IGNORE INTO Users (FirstName, LastName, Email, PasswordHash, GoogleID, RoleID) VALUES 
('John', 'Doe', 'john@example.com', '$2b$12$JxP1gD/J5vZjDHCmTVTnZ.eF1TV0QTFM.yjG3fxtKlzjY8Ph7G2LC', '1234567890', 2),  -- User role; Password: userpassword
('Jane', 'Smith', 'jane@example.com', '$2b$12$aP3sLDaV3i7AUpiMaU89J.0PGft/0FH2nOK9e0Zy3K3AfzLx/dCnq', NULL, 2),  -- User role; Password: userpassword
('Admin', 'User', 'admin@example.com', '$2b$12$GzP5tL3yV7zD/Cy1mA9eB.PjZfF2F1bS0UvxDbjlF8uP1U8jzGkXm', NULL, 1);  -- Admin role; Password: adminpassword

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

-- Insert mock meditation sessions for User 1
INSERT INTO MeditationSessions (UserID, MeditationID, SessionDateTime) VALUES
(1, 1, '2023-09-08 06:30:00'),
(1, 2, '2023-09-15 07:00:00'),
(1, 3, '2023-10-01 08:00:00'),
(1, 1, '2023-10-15 09:30:00'),
(1, 2, '2023-11-05 07:45:00'),
(1, 3, '2023-11-20 06:50:00'),
(1, 1, '2023-12-10 08:10:00'),
(1, 2, '2024-01-05 09:05:00'),
(1, 3, '2024-02-01 07:15:00'),
(1, 1, '2024-03-10 08:25:00');

-- Insert mock meditation sessions for User 2
INSERT INTO MeditationSessions (UserID, MeditationID, SessionDateTime) VALUES
(2, 1, '2023-09-09 06:15:00'),
(2, 2, '2023-09-20 07:20:00'),
(2, 3, '2023-10-05 07:45:00'),
(2, 1, '2023-11-01 08:15:00'),
(2, 2, '2023-12-05 09:00:00'),
(2, 3, '2023-12-25 06:40:00'),
(2, 1, '2024-01-10 08:30:00'),
(2, 2, '2024-02-15 09:20:00'),
(2, 3, '2024-03-05 07:00:00'),
(2, 1, '2024-04-01 06:45:00');

-- Insert mock meditation sessions for User 3
INSERT INTO MeditationSessions (UserID, MeditationID, SessionDateTime) VALUES
(3, 1, '2023-09-10 06:45:00'),
(3, 2, '2023-09-25 07:30:00'),
(3, 3, '2023-10-10 08:10:00'),
(3, 1, '2023-10-25 08:50:00'),
(3, 2, '2023-11-10 09:30:00'),
(3, 3, '2023-12-10 06:55:00'),
(3, 1, '2024-01-15 07:25:00'),
(3, 2, '2024-02-10 08:00:00'),
(3, 3, '2024-03-20 07:40:00'),
(3, 1, '2024-04-15 09:15:00');
