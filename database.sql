
-- OLX Clone SQL Database Schema with Sample Data

-- 1. USERS TABLE
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    profile_picture VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. LOCATIONS TABLE
CREATE TABLE locations (
    location_id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Pakistan'
);

-- 3. CATEGORIES TABLE
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    parent_id INT,
    FOREIGN KEY (parent_id) REFERENCES categories(category_id) ON DELETE SET NULL
);

-- 4. ADS / LISTINGS TABLE
CREATE TABLE ads (
    ad_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    location_id INT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    `condition` ENUM('New', 'Used') NOT NULL,
    is_sold BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- 5. IMAGES FOR ADS
CREATE TABLE ad_images (
    image_id INT PRIMARY KEY AUTO_INCREMENT,
    ad_id INT,
    image_url VARCHAR(255),
    FOREIGN KEY (ad_id) REFERENCES ads(ad_id) ON DELETE CASCADE
);

-- 6. FAVORITES / WISHLIST
CREATE TABLE favorites (
    user_id INT,
    ad_id INT,
    PRIMARY KEY (user_id, ad_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (ad_id) REFERENCES ads(ad_id) ON DELETE CASCADE
);

-- 7. MESSAGES (Chat between buyer and seller)
CREATE TABLE messages (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    ad_id INT NOT NULL,
    message TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id),
    FOREIGN KEY (ad_id) REFERENCES ads(ad_id)
);

-- 8. REPORTS (Ad Reports by Users)
CREATE TABLE reports (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    ad_id INT,
    reported_by INT,
    reason TEXT,
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ad_id) REFERENCES ads(ad_id),
    FOREIGN KEY (reported_by) REFERENCES users(user_id)
);

-- 9. TRANSACTIONS
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    ad_id INT,
    buyer_id INT,
    seller_id INT,
    amount DECIMAL(10, 2),
    status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending',
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ad_id) REFERENCES ads(ad_id),
    FOREIGN KEY (buyer_id) REFERENCES users(user_id),
    FOREIGN KEY (seller_id) REFERENCES users(user_id)
);

-- SAMPLE DATA INSERTS

-- Users
INSERT INTO users (full_name, email, phone, password, profile_picture)
VALUES 
('Ali Khan', 'ali@example.com', '03001234567', 'hashed_password1', 'ali.jpg'),
('Sara Malik', 'sara@example.com', '03009876543', 'hashed_password2', 'sara.jpg'),
('Ahmed Raza', 'ahmed@example.com', '03111234567', 'hashed_password3', 'ahmed.jpg');

-- Locations
INSERT INTO locations (city, state)
VALUES 
('Lahore', 'Punjab'),
('Karachi', 'Sindh'),
('Islamabad', 'Capital Territory');

-- Categories
INSERT INTO categories (name, parent_id)
VALUES
('Electronics', NULL),
('Mobiles', 1),
('Vehicles', NULL),
('Cars', 3),
('Home Appliances', NULL);

-- Ads
INSERT INTO ads (user_id, category_id, location_id, title, description, price, `condition`)
VALUES
(1, 2, 1, 'iPhone 13 Pro for Sale', 'Used iPhone in excellent condition.', 195000, 'Used'),
(2, 4, 2, 'Honda Civic 2020', 'Neat and clean car, family used.', 3800000, 'Used'),
(3, 5, 1, 'Haier Air Conditioner 1.5 Ton', 'Brand new AC with warranty.', 75000, 'New');

-- Ad Images
INSERT INTO ad_images (ad_id, image_url)
VALUES
(1, 'iphone13.jpg'),
(2, 'civic2020.jpg'),
(3, 'haier_ac.jpg');

-- Favorites
INSERT INTO favorites (user_id, ad_id)
VALUES
(2, 1),
(1, 2),
(3, 1);

-- Messages
INSERT INTO messages (sender_id, receiver_id, ad_id, message)
VALUES
(2, 1, 1, 'Hi, is the iPhone still available?'),
(1, 2, 1, 'Yes, it is.'),
(3, 2, 2, 'Can you share more pictures of the car?');

-- Reports
INSERT INTO reports (ad_id, reported_by, reason)
VALUES
(2, 1, 'Misleading price'),
(3, 2, 'Duplicate post');

-- Transactions
INSERT INTO transactions (ad_id, buyer_id, seller_id, amount, status)
VALUES
(1, 2, 1, 195000, 'Completed'),
(3, 1, 3, 75000, 'Pending');
