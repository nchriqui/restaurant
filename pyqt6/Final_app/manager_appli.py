import mysql.connector

from Data.BD.config import config

def get_most_favorite_recipe():
    # Se connecter à la base de données
    db = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = db.cursor()

    # Exécuter la requête pour obtenir la recette la plus préférée
    query = """
        SELECT r.name, COUNT(fr.fav_r_id) AS favorite_count
        FROM recipes r
        JOIN favorite_recipes fr ON r.recipe_id = fr.recipe_id
        GROUP BY r.recipe_id
        ORDER BY favorite_count DESC, r.name
        LIMIT 1
    """
    cursor.execute(query)

    # Récupérer le résultat de la requête
    result = cursor.fetchone()

    # Fermer la connexion à la base de données
    cursor.close()
    db.close()

    if result:
        recipe_name, favorite_count = result
        return recipe_name, favorite_count
    else:
        return None, None


def get_ingredient_proportions(k=10):
    # Se connecter à la base de données MySQL
    db_connection = mysql.connector.connect(**config)
    
    # Créer un curseur pour exécuter des requêtes
    cursor = db_connection.cursor()
    
    # Récupérer la liste des types d'ingrédients distincts
    cursor.execute("SELECT DISTINCT type FROM ingredients")
    ingredient_types = cursor.fetchall()
    
    # Initialiser un dictionnaire pour stocker les proportions
    proportions = {}
    
    # Parcourir chaque type d'ingrédient
    for ingredient_type in ingredient_types:
        # Compter le nombre total d'ingrédients pour ce type
        cursor.execute("SELECT COUNT(*) FROM ingredients WHERE type = %s", (ingredient_type[0],))
        total_count = cursor.fetchone()[0]
        
        # Stocker la proportion dans le dictionnaire
        proportions[ingredient_type[0]] = total_count
    
    # Fermer le curseur et la connexion à la base de données
    cursor.close()
    db_connection.close()
    
    # Calculer les proportions en pourcentage
    total_ingredients = sum(proportions.values())
    for ingredient_type in proportions:
        proportions[ingredient_type] = proportions[ingredient_type] / total_ingredients * 100

    # Trier le dictionnaire par proportion décroissante
    sorted_proportions = sorted(proportions.items(), key=lambda x: x[1], reverse=True)

    # Sélectionner les 10 premiers types avec les proportions les plus élevées
    top_10_types = dict(sorted_proportions[:k])

    # Calculer la proportion "Autre"
    proportion_autre = 100 - sum(top_10_types.values())

    # Ajouter le type "Autre" au dictionnaire
    top_10_types['Autres'] = proportion_autre
    
    return top_10_types

import mysql.connector

def get_cuisine_proportions(k=10):
    # Établir la connexion à la base de données MySQL
    connection = mysql.connector.connect(**config)

    cursor = connection.cursor()

    # Obtenir le total de recettes pour chaque origine culinaire
    query = "SELECT cuisine, COUNT(*) as count FROM recipes GROUP BY cuisine"
    cursor.execute(query)
    result = cursor.fetchall()

    total_recipes = sum([row[1] for row in result])

    cuisine_proportions = {}
    for row in result:
        cuisine = row[0]
        count = row[1]
        proportion = count / total_recipes * 100
        cuisine_proportions[cuisine] = proportion

    cursor.close()
    connection.close()

    # Trier le dictionnaire par proportion décroissante
    sorted_proportions = sorted(cuisine_proportions.items(), key=lambda x: x[1], reverse=True)

    # Sélectionner les 10 premiers types avec les proportions les plus élevées
    top_10_types = dict(sorted_proportions[:k])

    # Calculer la proportion "Autre"
    proportion_autre = 100 - sum(top_10_types.values())

    # Ajouter le type "Autre" au dictionnaire
    top_10_types['Autres'] = proportion_autre
    
    return top_10_types
