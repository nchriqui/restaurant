import mysql.connector
import json
import logging 

from Data.BD.config import config

def recipes_colaboratif(user_id, data):
    nn_user_id = data[str(user_id)]['nearest_N'] if str(user_id) in data else None
    print(nn_user_id)

    if nn_user_id is None:
        return -1

    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les données des utilisateurs et de leurs recettes consommées
    query = """
    SELECT DISTINCT r.recipe_id, r.name, r.price
    FROM recipes r
    JOIN favorite_recipes fr ON r.recipe_id = fr.recipe_id
    WHERE fr.user_id = %s OR fr.user_id = %s OR fr.user_id = %s;
    """

    data = (nn_user_id[0], nn_user_id[1], nn_user_id[2])
    cursor.execute(query, data)

    # Récupérer les résultats de la requête
    results = cursor.fetchall()

    # Valider les modifications dans la base de données
    cnx.commit()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    recipes = {"name": [], "recipe_id": [], "price": []}
    for row in results:
        recipe_id = row[0]
        recipe_name = row[1]
        recipe_price = row[2]

        recipes["name"].append(recipe_name)
        recipes["recipe_id"].append(recipe_id)
        recipes["price"].append(recipe_price)

    return recipes

# # Opening JSON file
# with open('Data/applications/knn_recommendation/data/user_nn_cat.json') as f:  
#     data = json.load(f)

# recipes = recipes_colaboratif('1', data)

# print(recipes["name"][0])  # Accéder au nom de la première recette
# print(recipes["id"][0])    # Accéder à l'ID de la première recette
# print(recipes["price"][0]) # Accéder au prix de la première recette

def get_recipe_id(recipe_name):
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les données des utilisateurs et de leurs recettes consommées
    query = """
    SELECT DISTINCT r.recipe_id
    FROM recipes r
    WHERE r.name = %s
    """
    
    data = (recipe_name, )
    cursor.execute(query, data)

    # Récupérer les résultats de la requête
    result = cursor.fetchone()

    # Valider les modifications dans la base de données
    cnx.commit()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    if result is None:
        return -1

    recipe_id = result[0]

    return recipe_id

def recipes_similarity(recipe_name, data):
    recipe_id = get_recipe_id(recipe_name)

    if recipe_id == None:
        return -1
    
    nn_recipe_id = data[recipe_id]['nearest_N']

    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les données des utilisateurs et de leurs recettes consommées
    query = """
    SELECT DISTINCT r.recipe_id, r.name, r.cuisine
    FROM recipes r
    WHERE r.recipe_id = %s OR r.recipe_id = %s OR r.recipe_id = %s
    """

    data = (nn_recipe_id[0], nn_recipe_id[1], nn_recipe_id[2])
    cursor.execute(query, data)

    # Récupérer les résultats de la requête
    results = cursor.fetchall()

    # Valider les modifications dans la base de données
    cnx.commit()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    recipes = {"name": [], "recipe_id": [], "origine": []}
    for row in results:
        recipe_id = row[0]
        recipe_name = row[1]
        recipe_origine = row[2]

        recipes["name"].append(recipe_name)
        recipes["recipe_id"].append(recipe_id)
        recipes["origine"].append(recipe_origine)

    return recipes

# # Opening JSON file
# with open('Data/applications/similarity_recommendation/data/kNN_computed.json') as f:  
#     data = json.load(f)

# recipes_sim = recipes_similarity('Ragoût du sud-ouest', data)

# print(recipes_sim["name"][0])  # Accéder au nom de la première recette
# print(recipes_sim["id"][0])    # Accéder à l'ID de la première recette
# print(recipes_sim["origine"][0]) # Accéder au prix de la première recette

def add_favorite(recipe_id, user_id):
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les données des utilisateurs et de leurs recettes consommées
    query = """
    INSERT INTO favorite_recipes (recipe_id, user_id) VALUES (%s, %s)
    """

    data = (recipe_id, user_id)
    cursor.execute(query, data)

    # Valider les modifications dans la base de données
    cnx.commit()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

def remove_favorite(recipe_id, user_id):
    # Create a connection to the MySQL database
    cnx = mysql.connector.connect(**config)

    # Create a cursor to execute SQL queries
    cursor = cnx.cursor()

    # Delete the favorite recipe entry
    query = """
    DELETE FROM favorite_recipes WHERE recipe_id = %s AND user_id = %s
    """

    data = (recipe_id, user_id)
    cursor.execute(query, data)

    # Validate the changes in the database
    cnx.commit()

    # Close the cursor and the connection
    cursor.close()
    cnx.close()

def check_favorite(recipe_id, user_id):
    # Create a connection to the MySQL database
    cnx = mysql.connector.connect(**config)

    # Create a cursor to execute SQL queries
    cursor = cnx.cursor()

    # Check if the recipe is marked as a favorite for the user
    query = """
    SELECT COUNT(*) FROM favorite_recipes WHERE recipe_id = %s AND user_id = %s
    """

    data = (recipe_id, user_id)
    cursor.execute(query, data)

    count = cursor.fetchone()[0]

    # Close the cursor and the connection
    cursor.close()
    cnx.close()

    # True if it is a favorite and False otherwise.
    return count > 0

def all_recipes():
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les données des utilisateurs et de leurs recettes consommées
    query = """
    SELECT DISTINCT r.recipe_id, r.name, r.price
    FROM recipes r
    """

    cursor.execute(query)

    # Récupérer les résultats de la requête
    results = cursor.fetchall()

    # Valider les modifications dans la base de données
    cnx.commit()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    recipes = {"name": [], "recipe_id": [], "price": []}
    for row in results:
        recipe_id = row[0]
        recipe_name = row[1]
        recipe_price = row[2]

        recipes["name"].append(recipe_name)
        recipes["recipe_id"].append(recipe_id)
        recipes["price"].append(recipe_price)


    return recipes




# Similarity Reco Fonctions 

# logging.basicConfig(level=logging.DEBUG,  # Niveau de journalisation (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#                     format='%(asctime)s - %(levelname)s - %(message)s')  # Format du message de log



def compute_one_knn(recipe_id, recipes_binarized, save=False, file_name="scores.json"):
    scores = {}
    scores[recipe_id] = {}
    for i in recipes_binarized:
        scores[recipe_id][i] = sum(
            abs(a - b)
            for a, b in zip(recipes_binarized[recipe_id], recipes_binarized[i])
        )

    if save:
        # Écrire les données dans un fichier JSON
        with open(f"Data/applications/similarity_recommendation/data/{file_name}", "w") as f:
            json.dump(scores, f)

    return scores


def compute_nearest_neighbors(user_similarity, k, save=True):
    nearest_neighbors = {}
    for i in user_similarity:
        sorted_similarity = sorted(user_similarity[str(i)].items(), key=lambda x: x[1])
        nearest_neighbors[str(i)] = {
            "nearest_N": [int(j[0]) for j in sorted_similarity[1 : k + 1]]
        }

    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/similarity_recommendation/data/kNN_computed.json", "w") as f:
            json.dump(nearest_neighbors, f, indent=4)

    return nearest_neighbors


"""
in : "23965", {'23965': {'nearest_N': [39919, 11013, 11066, 11331, 23344]}}
"""
def get_recipes_from_id(recipe_id, knn):
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    recipe_ids = knn[str(recipe_id)]["nearest_N"]

    where_clause = " OR ".join(["r.recipe_id = %s"] * len(recipe_ids))
    query = """
    SELECT DISTINCT r.recipe_id, r.name, r.cuisine
    FROM recipes r
    WHERE {}
    """.format(where_clause)
    data = tuple(recipe_ids)
    cursor.execute(query, data)

    # Récupérer les résultats de la requête
    results = cursor.fetchall()

    # Valider les modifications dans la base de données
    cnx.commit()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    recipes = {"name": [], "recipe_id": [], "origine": []}
    for row in results:
        recipe_id = row[0]
        recipe_name = row[1]
        recipe_origine = row[2]

        recipes["name"].append(recipe_name)
        recipes["recipe_id"].append(recipe_id)
        recipes["origine"].append(recipe_origine)

    print(recipes)

    return recipes

########################

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


def get_data():
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les types des ingrédients
    query = "SELECT DISTINCT i.type FROM ingredients i ORDER BY i.type"

    cursor.execute(query)

    # Récupérer les résultats de la requête
    resultsCategories = cursor.fetchall()

    # Récupérer les id des utilisateurs
    query = "SELECT user_id FROM users ORDER BY user_id"

    cursor.execute(query)

    # Récupérer les résultats de la requête
    resultsUsers = cursor.fetchall()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    all_ingredient_cats = []
    all_users_ids = []

    for row in resultsCategories:
        all_ingredient_cats.append(row[0])

    for row in resultsUsers:
        all_users_ids.append(row[0])
    
    return all_ingredient_cats, all_users_ids


def create_vectors(data, all_users_ids, all_ingredient_cats, save=True):
    # Créer un dictionnaire pour stocker les vecteurs pour chaque utilisateur
    user_vectors = {}

    # Boucle sur chaque utilisateur
    for user_data in all_users_ids:
        # Initialiser le vecteur pour cet utilisateur avec des zéros
        user_vector = [0] * len(all_ingredient_cats)

        # Mettre à jour le vecteur pour les recettes favorites de cet utilisateur
        for ingredient_cat in data[str(user_data)]:
            if ingredient_cat in all_ingredient_cats:
                index = all_ingredient_cats.index(ingredient_cat)
                user_vector[index] = 1

        user_vectors[str(user_data)] = user_vector
        
    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/knn_recommendation/data/user_vector_cat.json", "w") as f:
            json.dump(user_vectors, f, indent=4)

    return user_vectors

def compute_scores(user_vectors, all_users_ids, save=True):
    # Calculer la moyenne des scores de recettes et d'ingrédients pour chaque paire d'utilisateurs
    user_similarity = {}
    for i in all_users_ids:
        user_similarity[str(i)] = {}
        for j in all_users_ids:
            if i != j:
                category_sum = sum([abs(a - b) for a, b in zip(user_vectors[str(i)], user_vectors[str(j)])])
                user_similarity[str(i)][str(j)] = category_sum

    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/knn_recommendation/data/user_scores_cat.json", "w") as f:
            json.dump(user_similarity, f, indent=4)

    return user_similarity

def compute_nearest_neighbors_u2u(user_similarity, k, all_users_ids, save=True):
    # Trier les résultats par ordre décroissant pour obtenir les k plus proches voisins
    nearest_neighbors = {}
    for i in all_users_ids:
        sorted_similarity = sorted(user_similarity[str(i)].items(), key=lambda x: x[1])
        nearest_neighbors[str(i)] = {"nearest_N": [int(j[0]) for j in sorted_similarity[:k]]}

    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/knn_recommendation/data/user_nn_cat.json", "w") as f:
            json.dump(nearest_neighbors, f, indent=4)

    return nearest_neighbors



# all_ingredient_cats, all_users_ids = get_data()

# # Opening JSON file
# with open('Data/applications/knn_recommendation/data/user_data_cat.json') as f:  
#     data = json.load(f)

# user_vectors = create_vectors(data, all_users_ids, all_ingredient_cats)
# user_similarity = compute_scores(user_vectors, all_users_ids)
# k = 5
# nearest_neighbors = compute_nearest_neighbors(user_similarity, k, all_users_ids)