INSERT INTO "country" ("country_name") VALUES
('United States'),
('India'),
('United Kingdom'),
('France'),
('Japan'),
('South Korea'),
('China'),
('Germany'),
('Italy'),
('Spain');

INSERT INTO "genre" ("genre") VALUES
('Action'),
('Adventure'),
('Animation'),
('Biography'),
('Comedy'),
('Crime'),
('Documentary'),
('Drama'),
('Family'),
('Fantasy'),
('History'),
('Horror'),
('Music'),
('Mystery'),
('Romance'),
('Science Fiction'),
('Sport'),
('Thriller'),
('War'),
('Western');

INSERT INTO "film" (
    "id",
    "name",
    "year",
    "poster",
    "description",
    "rating",
    "duration",
    "country",
    "added_at"
) VALUES
(1, 'The Shawshank Redemption', 1994, 'shawshank.jpg',
 'Two imprisoned men bond over several years, finding solace and eventual redemption through acts of common decency.',
 10, 142, 'United States', 1700000000),

(2, 'The Godfather', 1972, 'godfather.jpg',
 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
 10, 175, 'United States', 1700000000),

(3, 'The Dark Knight', 2008, 'dark_knight.jpg',
 'Batman faces the Joker, a criminal mastermind who plunges Gotham City into chaos and tests the hero’s moral limits.',
 9, 152, 'United States', 1700000000),

(4, 'Pulp Fiction', 1994, 'pulp_fiction.jpg',
 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in a series of unpredictable events.',
 9, 154, 'United States', 1700000000),

(5, 'Forrest Gump', 1994, 'forrest_gump.jpg',
 'The story of a simple man whose kindness and optimism lead him through extraordinary moments in American history.',
 9, 142, 'United States', 1700000000),

(6, 'Inception', 2010, 'inception.jpg',
 'A skilled thief who steals secrets through dream-sharing technology is given a chance to erase his criminal past.',
 9, 148, 'United States', 1700000000),

(7, 'Fight Club', 1999, 'fight_club.jpg',
 'An office worker and a soap maker form an underground fight club that evolves into something much more dangerous.',
 9, 139, 'United States', 1700000000),

(8, 'Interstellar', 2014, 'interstellar.jpg',
 'A group of explorers travel through a wormhole in space in an attempt to ensure humanity’s survival.',
 9, 169, 'United States', 1700000000),

(9, 'Parasite', 2019, 'parasite.jpg',
 'A poor family schemes to become employed by a wealthy household, leading to unexpected and dark consequences.',
 9, 132, 'South Korea', 1700000000),

(10, 'The Lord of the Rings: The Return of the King', 2003, 'lotr_return_king.jpg',
 'The final battle for Middle-earth begins as Frodo and Sam approach Mount Doom to destroy the One Ring.',
 10, 201, 'United States', 1700000000);

INSERT INTO "genre_film" ("id", "genre_id", "film_id") VALUES
-- The Shawshank Redemption
(1, 'Drama', 1),
(2, 'Crime', 1),

-- The Godfather
(3, 'Crime', 2),
(4, 'Drama', 2),

-- The Dark Knight
(5, 'Action', 3),
(6, 'Crime', 3),
(7, 'Thriller', 3),

-- Pulp Fiction
(8, 'Crime', 4),
(9, 'Drama', 4),

-- Forrest Gump
(10, 'Drama', 5),
(11, 'Romance', 5),

-- Inception
(12, 'Action', 6),
(13, 'Science Fiction', 6),
(14, 'Thriller', 6),

-- Fight Club
(15, 'Drama', 7),
(16, 'Thriller', 7),

-- Interstellar
(17, 'Science Fiction', 8),
(18, 'Adventure', 8),
(19, 'Drama', 8),

-- Parasite
(20, 'Drama', 9),
(21, 'Thriller', 9),

-- The Lord of the Rings: The Return of the King
(22, 'Fantasy', 10),
(23, 'Adventure', 10),
(24, 'Action', 10);

INSERT INTO "actor" ("id", "first_name", "last_name", "birth_date", "death_date", "description") VALUES
(1, 'Tim', 'Robbins', '1958-10-16', NULL, 'Known for his role as Andy Dufresne in The Shawshank Redemption.'),
(2, 'Morgan', 'Freeman', '1937-06-01', NULL, 'Portrayed Ellis Boyd "Red" Redding in The Shawshank Redemption.'),
(3, 'Marlon', 'Brando', '1924-04-03', '2004-07-01', 'Famous for his role as Vito Corleone in The Godfather.'),
(4, 'Al', 'Pacino', '1940-04-25', NULL, 'Iconic role as Michael Corleone in The Godfather.'),
(5, 'Christian', 'Bale', '1974-01-30', NULL, 'Played Bruce Wayne / Batman in The Dark Knight.'),
(6, 'Heath', 'Ledger', '1979-04-04', '2008-01-22', 'Portrayed the Joker in The Dark Knight.'),
(7, 'John', 'Travolta', '1954-02-18', NULL, 'Played Vincent Vega in Pulp Fiction.'),
(8, 'Samuel', 'Jackson', '1948-12-21', NULL, 'Portrayed Jules Winnfield in Pulp Fiction.'),
(9, 'Tom', 'Hanks', '1956-07-09', NULL, 'Played Forrest Gump in Forrest Gump.'),
(10, 'Robin', 'Wright', '1966-04-08', NULL, 'Portrayed Jenny Curran in Forrest Gump.'),
(11, 'Leonardo', 'DiCaprio', '1974-11-11', NULL, 'Played Dom Cobb in Inception.'),
(12, 'Joseph', 'Gordon-Levitt', '1981-02-17', NULL, 'Portrayed Arthur in Inception.'),
(13, 'Brad', 'Pitt', '1963-12-18', NULL, 'Played Tyler Durden in Fight Club.'),
(14, 'Edward', 'Norton', '1969-08-18', NULL, 'Portrayed the Narrator in Fight Club.'),
(15, 'Matthew', 'McConaughey', '1969-11-04', NULL, 'Played Cooper in Interstellar.'),
(16, 'Anne', 'Hathaway', '1982-11-12', NULL, 'Portrayed Amelia Brand in Interstellar.'),
(17, 'Song', 'Kang-ho', '1967-01-17', NULL, 'Played Kim Ki-taek in Parasite.'),
(18, 'Cho', 'Yeo-jeong', '1981-02-10', NULL, 'Portrayed Park Yeon-kyo in Parasite.'),
(19, 'Elijah', 'Wood', '1981-01-28', NULL, 'Played Frodo Baggins in The Lord of the Rings: The Return of the King.'),
(20, 'Ian', 'McKellen', '1939-05-25', NULL, 'Portrayed Gandalf in The Lord of the Rings: The Return of the King.');

INSERT INTO "actor_film" ("id", "actor_id", "film_id") VALUES
-- The Shawshank Redemption
(1, 1, 1),
(2, 2, 1),

-- The Godfather
(3, 3, 2),
(4, 4, 2),

-- The Dark Knight
(5, 5, 3),
(6, 6, 3),

-- Pulp Fiction
(7, 7, 4),
(8, 8, 4),

-- Forrest Gump
(9, 9, 5),
(10, 10, 5),

-- Inception
(11, 11, 6),
(12, 12, 6),

-- Fight Club
(13, 13, 7),
(14, 14, 7),

-- Interstellar
(15, 15, 8),
(16, 16, 8),

-- Parasite
(17, 17, 9),
(18, 18, 9),

-- The Lord of the Rings: The Return of the King
(19, 19, 10),
(20, 20, 10);

INSERT INTO "user" (
    "id",
    "first_name",
    "last_name",
    "password",
    "login",
    "email",
    "phone_number",
    "birth_date",
    "photo",
    "additional_info",
    "last_login",
    "created_at"
) VALUES
(1, 'John', 'Doe', '123456', 'johndoe', 'johndoe@example.com', '+10000000001', '1990-01-01', 'photo1.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(2, 'Jane', 'Smith', '123456', 'janesmith', 'janesmith@example.com', '+10000000002', '1991-02-02', 'photo2.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(3, 'Michael', 'Brown', '123456', 'michaelbrown', 'michaelbrown@example.com', '+10000000003', '1988-03-03', 'photo3.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(4, 'Emily', 'Davis', '123456', 'emilydavis', 'emilydavis@example.com', '+10000000004', '1992-04-04', 'photo4.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(5, 'William', 'Wilson', '123456', 'williamwilson', 'williamwilson@example.com', '+10000000005', '1985-05-05', 'photo5.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(6, 'Olivia', 'Martinez', '123456', 'oliviamartinez', 'oliviamartinez@example.com', '+10000000006', '1993-06-06', 'photo6.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(7, 'James', 'Anderson', '123456', 'jamesanderson', 'jamesanderson@example.com', '+10000000007', '1989-07-07', 'photo7.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(8, 'Sophia', 'Thomas', '123456', 'sophiathomas', 'sophiathomas@example.com', '+10000000008', '1994-08-08', 'photo8.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(9, 'Benjamin', 'Taylor', '123456', 'benjamintaylor', 'benjamintaylor@example.com', '+10000000009', '1990-09-09', 'photo9.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(10, 'Ava', 'Moore', '123456', 'avamoore', 'avamoore@example.com', '+10000000010', '1991-10-10', 'photo10.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(11, 'Daniel', 'Jackson', '123456', 'danieljackson', 'danieljackson@example.com', '+10000000011', '1987-11-11', 'photo11.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(12, 'Mia', 'White', '123456', 'miawhite', 'miawhite@example.com', '+10000000012', '1992-12-12', 'photo12.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(13, 'Alexander', 'Harris', '123456', 'alexanderharris', 'alexanderharris@example.com', '+10000000013', '1986-01-13', 'photo13.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(14, 'Isabella', 'Martin', '123456', 'isabellamartin', 'isabellamartin@example.com', '+10000000014', '1993-02-14', 'photo14.jpg', 'No additional info', '2025-12-01', '2025-01-01'),
(15, 'Ethan', 'Lee', '123456', 'ethanlee', 'ethanlee@example.com', '+10000000015', '1989-03-15', 'photo15.jpg', 'No additional info', '2025-12-01', '2025-01-01');

INSERT INTO "feedback" ("id", "user", "film", "grade", "description") VALUES
-- The Shawshank Redemption
(1, 1, 1, 10, 'An inspiring story of hope and friendship, truly a masterpiece.'),
(2, 2, 1, 9, 'Excellent performances and a powerful narrative.'),
(3, 3, 1, 10, 'One of the best movies ever made, timeless classic.'),

-- The Godfather
(4, 4, 2, 10, 'Brilliant storytelling and unforgettable characters.'),
(5, 5, 2, 9, 'A cinematic masterpiece, Marlon Brando is incredible.'),
(6, 6, 2, 10, 'The ultimate mafia movie, perfect from start to finish.'),

-- The Dark Knight
(7, 7, 3, 10, 'Heath Ledger’s Joker performance is legendary.'),
(8, 8, 3, 9, 'Great action and an intense story, one of the best superhero films.'),

-- Pulp Fiction
(9, 9, 4, 9, 'Unique storytelling, witty dialogue, and excellent cast.'),
(10, 10, 4, 10, 'Quentin Tarantino at his finest, cult classic.'),

-- Forrest Gump
(11, 11, 5, 10, 'Heartwarming and unforgettable, Tom Hanks is brilliant.'),
(12, 12, 5, 9, 'A perfect blend of humor, drama, and history.'),

-- Inception
(13, 1, 6, 9, 'Mind-bending and visually stunning, a true cinematic experience.'),
(14, 2, 6, 10, 'Complex and exciting, Christopher Nolan delivers once again.'),

-- Fight Club
(15, 3, 7, 10, 'Dark, edgy, and thought-provoking, a must-watch.'),
(16, 4, 7, 9, 'Brilliant performances and a story that stays with you.'),

-- Interstellar
(17, 5, 8, 10, 'Epic, emotional, and visually spectacular.'),
(18, 6, 8, 9, 'A masterpiece of sci-fi with a heartfelt story.'),

-- Parasite
(19, 7, 9, 10, 'Ingenious and suspenseful, completely deserved the Oscar.'),
(20, 8, 9, 9, 'Clever, gripping, and socially insightful.'),

-- The Lord of the Rings: The Return of the King
(21, 9, 10, 10, 'A perfect epic conclusion to an unforgettable trilogy.'),
(22, 10, 10, 9, 'Spectacular visuals and an emotional journey, truly amazing.'),
(23, 11, 10, 10, 'Epic battles and unforgettable characters, a masterpiece.');