CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255)
);

CREATE TABLE restorations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    original_image VARCHAR(255),
    restored_image VARCHAR(255),
    restoration_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);