import mysql.connector
import json

from Data.BD.config import config

def generate_knn_full():
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les données des utilisateurs et de leurs ingrédients et recettes préférés
    query = """
    SELECT u.user_id, GROUP_CONCAT(DISTINCT fr.recipe_id SEPARATOR ',') AS favourite_recipes,
        GROUP_CONCAT(DISTINCT fi.ingredient_id SEPARATOR ',') AS favourite_ingredients
    FROM users u
    LEFT JOIN favorite_ingredients fi ON u.user_id = fi.user_id
    LEFT JOIN favorite_recipes fr ON u.user_id = fr.user_id
    GROUP BY u.user_id
    """

    cursor.execute(query)

    # Récupérer les résultats de la requête
    results = cursor.fetchall()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    # Créer une liste de dictionnaires pour stocker les données des utilisateurs
    users = {}
    for row in results:
        user_id = row[0]
        favourite_recipes = row[1].split(',') if row[1] else []
        favourite_ingredients = row[2].split(',') if row[2] else []

        users[user_id] = (favourite_recipes, favourite_ingredients)

    # Écrire les données dans un fichier JSON
    with open("Data/applications/knn_recommendation/data/user_data.json", "w") as f:
        json.dump(users, f, indent=4)

def generate_knn_categories():
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les données des utilisateurs et de leurs catégories d'ingrédients préférées
    query = """
    SELECT u.user_id, 
        GROUP_CONCAT(DISTINCT i.type SEPARATOR ',') AS favourite_categories
    FROM users u
    LEFT JOIN favorite_recipes fr ON u.user_id = fr.user_id
    LEFT JOIN recipes_ingredients ri ON fr.recipe_id = ri.recipe_id
    LEFT JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
    GROUP BY u.user_id
    """

    cursor.execute(query)

    # Récupérer les résultats de la requête
    results = cursor.fetchall()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    users = {}
    for row in results:
        user_id = row[0]
        favourite_categories = row[1].split(',') if row[1] else []

        users[user_id] = favourite_categories

    # Écrire les données dans un fichier JSON
    with open("Data/applications/knn_recommendation/data/user_data_cat.json", "w", encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def generate_knn_cons():
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les données des utilisateurs et de leurs recettes consommées
    query = """
    SELECT u.user_id,
        GROUP_CONCAT(DISTINCT cons.recipe_id SEPARATOR ',') AS recipes_consumed
    FROM users u
    LEFT JOIN consommations cons ON u.user_id = cons.user_id
    GROUP BY u.user_id
    """

    cursor.execute(query)

    # Récupérer les résultats de la requête
    results = cursor.fetchall()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    # Créer une liste de dictionnaires pour stocker les données des utilisateurs
    users = {}
    for row in results:
        user_id = row[0]
        recipes_consumed = row[1].split(',') if row[1] else []

        users[user_id] = recipes_consumed

    # Écrire les données dans un fichier JSON
    with open("Data/applications/knn_recommendation/data/user_data_cons.json", "w") as f:
        json.dump(users, f, indent=4)


generate_knn_full()
generate_knn_categories()
generate_knn_cons()
