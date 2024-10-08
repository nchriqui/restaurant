import json
import os

import mysql.connector

from Data.BD.config import config

def generate_recipes_data():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Requête SQL pour récupérer la liste des ID d'ingrédients pour chaque recette
    query = """
    SELECT r.recipe_id, GROUP_CONCAT(ri.ingredient_id) AS ingredient_ids
    FROM recipes r
    JOIN recipes_ingredients ri ON r.recipe_id = ri.recipe_id
    GROUP BY r.recipe_id;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    recipes = {}
    for row in results:
        recipe_id = row[0]
        ingredient_ids = row[1]
        # print(f"Recette {recipe_id}: Liste des ID d'ingrédients: {ingredient_ids}")
        substrings = ingredient_ids.split(",") if row[1] else []

        # Convertir les sous-chaînes en entiers
        integer_list = [int(substring) for substring in substrings]
        recipes[recipe_id] = integer_list

    cursor.close()
    conn.close()

    directory = "data/"
    file_path = os.path.join(directory, "recipes_data.json")
    with open(file_path, "w") as file:
        json.dump(recipes, file)

    if os.path.exists(file_path):
        print("Le fichier a été enregistré avec succès.")
    else:
        print("Une erreur s'est produite lors de l'enregistrement du fichier.")


def generate_recipes_limited_ingredients():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Requête SQL pour récupérer la liste des ID d'ingrédients pour chaque recette
    query = """
        SELECT r.recipe_id,
            GROUP_CONCAT(DISTINCT i.ingredient_id SEPARATOR ',') AS id_ingredients
        FROM recipes r
        JOIN recipes_ingredients ri ON r.recipe_id = ri.recipe_id
        JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
        WHERE i.type IN ('Viande', 'Poisson', 'Champignon', 'Fruits de mer', 'Légume', 'Légumineuse')  
        ORDER BY r.recipe_id 
        GROUP BY r.name;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    recipes = {}
    for row in results:
        recipe_id = row[0]
        ingredient_ids = row[1]
        substrings = ingredient_ids.split(",") if row[1] else []

        integer_list = [int(substring) for substring in substrings]
        recipes[recipe_id] = integer_list

    cursor.close()
    conn.close()

    directory = "data/"
    file_path = os.path.join(directory, "recipes_data_limited_ingredients.json")
    with open(file_path, "w") as file:
        json.dump(recipes, file, indent=4)

    if os.path.exists(file_path):
        print("Le fichier a été enregistré avec succès.")
    else:
        print("Une erreur s'est produite lors de l'enregistrement du fichier.")


def generate_recipes_origines():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Requête SQL pour récupérer la liste des ID d'ingrédients pour chaque recette
    query = """
        SELECT r.recipe_id,
            GROUP_CONCAT(DISTINCT i.type SEPARATOR ',') AS categories, r.cuisine
        FROM recipes r
        JOIN recipes_ingredients ri ON r.recipe_id = ri.recipe_id
        JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
        GROUP BY r.name;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    recipes = {}
    for row in results:
        recipe_id = row[0]
        categories = row[1]
        #cuisine = row[2]
        # print(f"Recette {recipe_id}: Liste des ID d'ingrédients: {ingredient_ids}")
        substrings = categories.split(",") if row[1] else []

        # Convertir les sous-chaînes en entiers
        categories_split = [substring for substring in substrings]
        #recipes[recipe_id] = (categories_split, cuisine)
        recipes[recipe_id] = (categories_split)


    cursor.close()
    conn.close()

    directory = "data/"
    file_path = os.path.join(directory, "recipes_data_origines.json")
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(recipes, file, indent=4, ensure_ascii=False)

    if os.path.exists(file_path):
        print("Le fichier a été enregistré avec succès.")
    else:
        print("Une erreur s'est produite lors de l'enregistrement du fichier.")


def extract_all_types():
    """
    Select all types and return the list ordered to binarize later
    """
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Requête SQL pour récupérer la liste des ID d'ingrédients pour chaque recette
    query = """
        SELECT DISTINCT type FROM ingredients ORDER BY type; 
    """

    cursor.execute(query)
    results = cursor.fetchall()

    types = []
    for row in results:
        types.append(row[0])

    cursor.close()
    conn.close()

    return types


def extract_all_cuisines():
    """
    Select all types and return the list ordered to binarize later
    """
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Requête SQL pour récupérer la liste des ID d'ingrédients pour chaque recette
    query = """
        SELECT DISTINCT cuisine FROM recipes ORDER BY cuisine; 
    """

    cursor.execute(query)
    results = cursor.fetchall()

    types = []
    for row in results:
        types.append(row[0])

    cursor.close()
    conn.close()

    return types


def extract_all_ingredients_with_chosen_type():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Requête SQL pour récupérer la liste des ID d'ingrédients pour chaque recette
    query = """
    SELECT DISTINCT i.ingredient_id
    FROM ingredients i
    WHERE i.type IN ('Champignon');    
    """

    cursor.execute(query)
    results = cursor.fetchall()

    types = []
    for row in results:
        types.append(row[0])

    cursor.close()
    conn.close()

    return types


if __name__ == "__main__":
    # generate_recipes_data()
    # generate_recipes_origines()
    generate_recipes_limited_ingredients()
    print(extract_all_types())
    print("////")
    print(extract_all_cuisines())
