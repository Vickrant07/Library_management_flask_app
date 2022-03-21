DROP TABLE IF EXISTS books;

CREATE TABLE books
(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    author TEXT NOT NULL,
    price REAL NOT NULL,
    rent REAL NOT NULL,
    stock INTEGER NOT NULL,
    description TEXT,
    image_name TEXT NOT NULL,
    image_attribute NOT NUll
);

INSERT INTO books 
( name, author, price, rent, stock, description, image_name, image_attribute)
VALUES
('101 Essays',                 'Brianna Weist',  12.33, 1.50, 20, 'A list of ways to improve thinking.',    '101_essays.jpg',                 'Photo by Thought Catalog on Unsplash'),
('Art of not giving a Fuck',   'Mark Manson',    17.99, 1.50, 25, 'A self improvement journey',             'art_of_not_giving_fuck.jpg',     'Photo by Varad Parulekar on Unsplash'),
('Crazy Love',                 'Francis Chan',   12.40, 1.50, 15, 'Love life fantasy.',                     'crazy_love.jpg',                 'Photo by Zia King on Unsplash'),
('Happy',                      'Alex Lemon',     15.99, 1.50, 20, 'A nice state called Happyness.',         'happy.jpg',                      'Photo by Josh Felise on Unsplash'),
('The Heart is Sea',           'Nikita Gill',    18.99, 1.50, 25, 'Explore the state of the Heart.',        'heart_is_sea.jpg',               'Photo by Thought Catalog on Unsplash'),
('How Innovation Works',       'Matt Ridley',    15.50, 1.50, 15, 'A documentary of Innovation.',           'how_innovation_works.jpg',       'Photo by Matt Ridley on Unsplash'),
('Letters I should Have Sent', 'Rania Naim',     21.99, 1.50, 30, 'Great novel about expressing yourself.', 'letters_i_should_have_sent.jpg', 'Photo by Thought Catalog on Unsplash'),
('Milk and Honey',             'Rupi Kaur',      17.99, 1.50, 25, 'A nice story.',                          'milk_and_honey.jpg',             'Photo by Sincerely Media on Unsplash'),
('Psycology of Money',         'Morgan Housel',  16.99, 1.50, 20, 'Few wise words on Money.',               'psycology_of_money.jpg',         'Photo by Morgan Housel on Unsplash'),
('Salt Water',                 'Brianna Wiest',  13.99, 1.50, 15, 'A crazy novel when lonely.',             'salt_water.jpg',                 'Photo by Thought Catalog on Unsplash'),
('Soul is River',              'Nikita Gill',    14.99, 1.50, 20, 'Explore the state of soul.',             'soul_is_river.jpg',              'Photo by Thought Catalog on Unsplash'),
('Stop Worrying',              'Dale Carnegie',  11.99, 1.50, 25, 'Utilise your time by living happy.',     'stop_worrying.jpg',              'Photo by Cody Board on Unsplash'),
('The Two Towers',             'J.R.R. Tolkien', 12.99, 1.50, 30, 'A nice novel by world famous author.',   'the_two_towers.jpg',             'Photo by Madalyn Cox on Unsplash'),
('Waves',                      'Sharon Dogar',   19.99, 1.50, 35, 'A nice pass time read.',                 'waves.jpg',                      'Photo by NMG Network on Unsplash');

  
DROP TABLE IF EXISTS customers;

CREATE TABLE customers
(
    customer_id TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS admins;

CREATE TABLE admins
(
    admin_id TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS orders;

CREATE TABLE orders
(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL,
    books_id_str TEXT NOT NULL,
    name_str TEXT NOT NULL,
    quantity_str TEXT NOT NULL,
    total_price REAL,
    total_rent REAL
);
