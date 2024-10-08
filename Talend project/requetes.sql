-- Désactiver les contraintes de clé étrangère temporairement
SET FOREIGN_KEY_CHECKS = 0;

-- Modifier les IDs supérieures à 2000 en ID-997 dans la table principale
UPDATE ingredients SET ingredient_id = ingredient_id - 997 WHERE ingredient_id > 1999;

-- Mettre à jour les IDs dans les tables liées
-- Remplacez "table_liee1" et "table_liee2" par les noms réels de vos tables liées
UPDATE recipes_ingredients SET ingredient_id = ingredient_id - 997 WHERE ingredient_id > 1999;
UPDATE favorite_ingredients SET ingredient_id = ingredient_id - 997 WHERE ingredient_id > 1999;

-- Réactiver les contraintes de clé étrangère
SET FOREIGN_KEY_CHECKS = 1;

UPDATE ingredients SET type = REPLACE(type, "champignon", "Champignon");
UPDATE ingredients SET type = REPLACE(type, "Boisson alcoolisée", "Boisson Alcoolisée");

INSERT INTO recipes_restaurant (recipe_id, price)
    VALUES 
        (1599, 7.80),
	    (3390, 6.90),
	    (5672, 12.20),
        (7255, 15.20),
        (8433, 9.00),
	    (9854, 7.30),
        (10867, 11.00),
        (14222, 17.00),
    	(15985, 14.60),
        (16077, 15.00),
        (17852, 9.75),
        (17064, 8.60),
	    (18762, 9.80),
        (19037, 9.70),
	    (21478, 11.60),
	    (22430, 7.45),
        (23264, 10.10),
	    (24573, 14.00),
        (26817, 16.20),
	    (28421, 10.00),
        (30366, 11.00),
        (34072, 11.00),
        (35192, 15.20),
        (37964, 12.25),
        (39524, 12.00),
        (41080, 8.20),
        (42131, 13.60),
        (44657, 14.20),
        (44887, 15.00),
        (45672, 13.00);