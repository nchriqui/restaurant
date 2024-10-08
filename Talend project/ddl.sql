DROP TABLE favorite_ingredients;
DROP TABLE favorite_recipes;
DROP TABLE consommations;
DROP TABLE recipes_ingredients;
DROP TABLE recipes_restaurant;
DROP TABLE units;
DROP TABLE ingredients;
DROP TABLE recipes;
DROP TABLE users;

CREATE TABLE users (
    user_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    lastname VARCHAR(50) NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    password VARCHAR(200) NOT NULL,
    mail VARCHAR(50) NOT NULL UNIQUE,
    balance FLOAT NOT NULL DEFAULT 0.0
);

CREATE TABLE recipes (
    recipe_id INT NOT NULL PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    type VARCHAR(30) NULL,
    cuisine VARCHAR(60) NULL,
    price FLOAT NULL
);

CREATE TABLE ingredients (
    ingredient_id INT NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(30) NULL,
    price FLOAT NULL,
    nutriscore INT NULL,
    allergen VARCHAR(255) NULL
);

CREATE TABLE units (
    unit_id INT NOT NULL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    quantity VARCHAR(20) NULL
);

CREATE TABLE recipes_ingredients (
    id INT NOT NULL AUTO_INCREMENT,
    recipe_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    ingredient_quantity FLOAT NOT NULL,
    unit_id INT NULL,
    PRIMARY KEY (id, recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON UPDATE CASCADE,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

CREATE TABLE recipes_restaurant (
    recipe_id INT NOT NULL PRIMARY KEY,
    price FLOAT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
);

CREATE TABLE consommations (
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (user_id, recipe_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes_restaurant(recipe_id)
);

CREATE TABLE favorite_recipes (
    fav_r_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    recipe_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
);

CREATE TABLE favorite_ingredients (
    fav_i_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    ingredient_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON UPDATE CASCADE
);

DELETE FROM recipes;
DELETE FROM ingredients;
DELETE FROM units;
DELETE FROM recipes_ingredients;