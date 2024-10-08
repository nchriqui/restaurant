import random
import mysql.connector

from Data.BD.config import config

# Connexion à la base de données
cnx = mysql.connector.connect(**config)

# Génération de prix aléatoires pour chaque recette
cursor = cnx.cursor()
cursor.execute("SELECT r.recipe_id FROM recipes r LEFT JOIN recipes_restaurant rr ON r.recipe_id = rr.recipe_id WHERE rr.recipe_id IS NULL")
recipe_ids = cursor.fetchall()

for recipe_id in recipe_ids:
    price = round(random.uniform(5.0, 20.0), 2)  # Génère un prix aléatoire entre 5.0 et 20.0
    query = "UPDATE recipes SET price = %s WHERE recipe_id = %s"
    values = (price, recipe_id[0])
    cursor.execute(query, values)

cnx.commit()

# Fermeture de la connexion à la base de données
cursor.close()
cnx.close()
