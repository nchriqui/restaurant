import random
import mysql.connector

from Data.BD.config import config

N = 5000

def get_data():
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les id des recettes
    query = "SELECT recipe_id FROM recipes"

    cursor.execute(query)

    # Récupérer les résultats de la requête
    resultsRecipes = cursor.fetchall()

    # Récupérer les id des ingrédients
    query = "SELECT ingredient_id FROM ingredients"

    cursor.execute(query)

    # Récupérer les résultats de la requête
    resultsIngredients = cursor.fetchall()

    # Récupérer les id des ingrédients
    query = "SELECT user_id FROM users"

    cursor.execute(query)

    # Récupérer les résultats de la requête
    resultsUsers = cursor.fetchall()

    # Récupérer les id des ingrédients
    query = "SELECT recipe_id FROM recipes_restaurant"

    cursor.execute(query)

    # Récupérer les résultats de la requête
    resultsRecipesRestaurant = cursor.fetchall()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    all_recipe_ids = []
    all_ingredient_ids = []
    all_users_ids = []

    all_recipe_resto_ids = []

    for row in resultsRecipes:
        all_recipe_ids.append(row[0])

    for row in resultsIngredients:
        all_ingredient_ids.append(row[0])

    for row in resultsUsers:
        all_users_ids.append(row[0])

    for row in resultsRecipesRestaurant:
        all_recipe_resto_ids.append(row[0])
    
    return all_recipe_ids, all_ingredient_ids, all_users_ids, all_recipe_resto_ids

def generate_fav(all_recipe_ids, all_ingredient_ids, all_user_ids):
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Insérer les données dans les tables consommations, favorite_recipes & favorite_ingredients
    for _ in range(N):
        recipe_id = random.choice(all_recipe_ids)
        user_id = random.choice(all_user_ids)
        ingredient_id = random.choice(all_ingredient_ids)

        query = "INSERT INTO favorite_recipes (recipe_id, user_id) SELECT %s, %s FROM DUAL WHERE NOT EXISTS (SELECT * FROM favorite_recipes WHERE recipe_id=%s AND user_id=%s)"
        data = (recipe_id, user_id, recipe_id, user_id)
        cursor.execute(query, data)

        query = "INSERT INTO favorite_ingredients (ingredient_id, user_id) SELECT %s, %s FROM DUAL WHERE NOT EXISTS (SELECT * FROM favorite_ingredients WHERE ingredient_id=%s AND user_id=%s)"
        data = (ingredient_id, user_id, ingredient_id, user_id)
        cursor.execute(query, data)
    
    # Valider les modifications dans la base de données
    cnx.commit()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

def generate_cons(all_user_ids, all_recipe_resto_ids):
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    for _ in range(2000):
        recipe_id = random.choice(all_recipe_resto_ids)
        user_id = random.choice(all_user_ids)

        # Vérifier si la combinaison utilisateur-recette existe déjà
        query = "SELECT * FROM consommations WHERE user_id = %s AND recipe_id = %s"
        data = (user_id, recipe_id)
        cursor.execute(query, data)
        existing_row = cursor.fetchone()

        if existing_row:
            # La combinaison utilisateur-recette existe déjà, augmenter la quantité
            query = "UPDATE consommations SET quantity = quantity + 1 WHERE user_id = %s AND recipe_id = %s"
            cursor.execute(query, data)
        else:
            # Insérer une nouvelle consommation avec une quantité initiale de 1
            query = "INSERT INTO consommations (user_id, recipe_id, quantity) VALUES (%s, %s, %s)"
            data = (user_id, recipe_id, 1)
            cursor.execute(query, data)

    # Valider les modifications dans la base de données
    cnx.commit()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

all_recipe_ids, all_ingredient_ids, all_user_ids, all_recipe_resto_ids = get_data()

generate_fav(all_recipe_ids, all_ingredient_ids, all_user_ids)
generate_cons(all_user_ids, all_recipe_resto_ids)