CREATE DATABASE IF NOT EXISTS quotesdb;
USE quotesdb;

CREATE TABLE IF NOT EXISTS quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    author VARCHAR(255) NOT NULL,
    quote TEXT NOT NULL
);

INSERT INTO quotes (author, quote) VALUES
('Albert Einstein', 'Life is like riding a bicycle. To keep your balance you must keep moving.'),
('Confucius', 'It does not matter how slowly you go as long as you do not stop.'),
('Oscar Wilde', 'Be yourself; everyone else is already taken.'),
('Steve Jobs', 'Stay hungry, stay foolish.'),
('Mother Teresa', 'Spread love everywhere you go. Let no one ever come to you without leaving happier.'),
('Chinggis Khaan', 'Surakh zorigtoi bol suraltsah chadal irne.'),
('Buddha', 'Peace comes from within. Do not seek it without.'),
('Lao Tzu', 'A journey of a thousand miles begins with a single step.'),
('Mahatma Gandhi', 'Be the change that you wish to see in the world.'),
('Mark Twain', 'The secret of getting ahead is getting started.'),
('Nelson Mandela', 'It always seems impossible until it’s done.'),
('George Orwell', 'In a time of deceit telling the truth is a revolutionary act.'),
('J.K. Rowling', 'It is our choices that show what we truly are, far more than our abilities.'),
('Miyamoto Musashi', 'You must understand that there is more than one path to the top of the mountain.'),
('Luvsanvandan Bold', 'Zuv setgeltei khunii zam deer zovlon baragkhgui.'),
('Dalai Lama', 'Happiness is not something ready made. It comes from your own actions.'),
('Stephen Hawking', 'However difficult life may seem, there is always something you can do and succeed at.'),
('Napoleon Hill', 'Strength and growth come only through continuous effort and struggle.'),
('Sun Tzu', 'In the midst of chaos, there is also opportunity.'),
('Bruce Lee', 'Knowing is not enough, we must apply. Willing is not enough, we must do.');