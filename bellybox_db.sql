CREATE DATABASE IF NOT EXISTS bellybox_db;
USE bellybox_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    user_type ENUM('admin', 'customer', 'delivery') NOT NULL DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

CREATE TABLE dishes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    image_url VARCHAR(255),
    category_id INT,
    is_special BOOLEAN DEFAULT FALSE,
    availability ENUM('available', 'not_available') DEFAULT 'available',
    FOREIGN KEY (category_id) REFERENCES menu_categories(id) ON DELETE SET NULL
);

CREATE TABLE specials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dish_id INT,
    special_date DATE,
    FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_type ENUM('delivery', 'takeaway') DEFAULT 'delivery',
    delivery_address TEXT,
    status ENUM('pending', 'accepted', 'preparing', 'out_for_delivery', 'delivered', 'cancelled') DEFAULT 'pending',
    total_price DECIMAL(10,2),
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_partner_id INT DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (delivery_partner_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    dish_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (dish_id) REFERENCES dishes(id)
);

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    payment_method ENUM('credit_card', 'paypal', 'upi', 'cod') NOT NULL,
    payment_status ENUM('paid', 'pending', 'failed') DEFAULT 'pending',
    payment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE chefs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    bio TEXT,
    image_url VARCHAR(255),
    popularity INT DEFAULT 0
);

CREATE TABLE chef_dishes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chef_id INT,
    dish_id INT,
    FOREIGN KEY (chef_id) REFERENCES chefs(id),
    FOREIGN KEY (dish_id) REFERENCES dishes(id)
);

CREATE TABLE takeaway_counters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    address TEXT,
    contact_number VARCHAR(20)
);

CREATE TABLE takeaway_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    counter_id INT,
    preferred_pickup_time DATETIME,
    total_price DECIMAL(10,2),
    status ENUM('pending', 'accepted', 'ready_for_pickup', 'picked_up', 'cancelled') DEFAULT 'pending',
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (counter_id) REFERENCES takeaway_counters(id)
);

CREATE TABLE takeaway_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    takeaway_order_id INT,
    dish_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (takeaway_order_id) REFERENCES takeaway_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (dish_id) REFERENCES dishes(id)
);

CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    dish_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (dish_id) REFERENCES dishes(id)
);


CREATE TABLE offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    image_url VARCHAR(255),
    start_date DATE,
    end_date DATE
);


INSERT INTO users (username, email, password, phone, user_type)
VALUES ('admin', 'admin@bellybox.com', MD5('admin'), '9999999999', 'admin');

INSERT INTO users (username, email, password, phone, user_type)
VALUES 
('john_doe', 'john@example.com', MD5('john123'), '9876543210', 'customer');

INSERT INTO users (username, email, password, phone, user_type)
VALUES 
('delivery_1', 'delivery1@bellybox.com', MD5('pass123'), '9123456780', 'delivery'),
('delivery_2', 'delivery2@bellybox.com', MD5('pass123'), '9123456781', 'delivery');

INSERT INTO menu_categories (name, description)
VALUES 
('Beverages', 'Refreshing drinks and coolers'),
('Starter', 'Tasty appetizers to begin your meal'),
('Sea Food', 'Fresh and flavorful seafood dishes'),
('Desserts', 'Sweet treats to finish your meal'),
('Others', 'Other delicious options');

INSERT INTO dishes (name, description, price, image_url, category_id, is_special, availability)
VALUES
('Lemon Mint Cooler', 'A refreshing minty drink', 99.00, 'images/beverages/lemon_mint.jpg', 1, FALSE, 'available'),
('Tandoori Paneer Tikka', 'Grilled paneer with spices', 199.00, 'images/starters/paneer_tikka.jpg', 2, TRUE, 'available'),
('Garlic Butter Prawns', 'Juicy prawns sautéed in garlic butter', 349.00, 'images/seafood/prawns.jpg', 3, FALSE, 'available'),
('Chocolate Lava Cake', 'Warm chocolate cake with gooey center', 129.00, 'images/desserts/lava_cake.jpg', 4, TRUE, 'available'),
('Veg Biryani', 'Fragrant rice with spiced vegetables', 199.00, 'images/others/biryani.jpg', 5, FALSE, 'not_available');

INSERT INTO specials (dish_id, special_date)
VALUES
(2, CURDATE()), -- Tandoori Paneer Tikka
(4, CURDATE()); -- Chocolate Lava Cake

INSERT INTO chefs (name, bio, image_url, popularity)
VALUES 
('Chef Aman', 'Master of North Indian cuisine', 'images/chefs/aman.jpg', 45),
('Chef Lisa', 'Specialist in Desserts & Baking', 'images/chefs/lisa.jpg', 80);

INSERT INTO chef_dishes (chef_id, dish_id)
VALUES 
(1, 2), -- Chef Aman -> Paneer Tikka
(2, 4); -- Chef Lisa -> Lava Cake

INSERT INTO takeaway_counters (name, address, contact_number)
VALUES 
('BellyBox Main Kitchen', '123 Cloud Lane, Food City', '9870001122'),
('BellyBox Express', '45 QuickServe Street, Food City', '9870001123');

INSERT INTO offers (title, description, image_url, start_date, end_date)
VALUES 
('Get 20% Off!', 'Order above ₹500 and get 20% off.', 'images/offers/20percent.jpg', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 7 DAY)),
('Free Dessert!', 'Get a free dessert with orders above ₹700.', 'images/offers/free_dessert.jpg', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 5 DAY));

INSERT INTO feedback (user_id, dish_id, rating, comment)
VALUES 
(1, 2, 5, 'Amazing taste, perfectly grilled!'),
(2, 4, 4, 'Delicious lava cake, but slightly too sweet.');


