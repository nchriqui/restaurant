import mysql.connector
import json

from Data.BD.config import config

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

    # Récupérer les id des utilisateurs
    query = "SELECT user_id FROM users ORDER BY user_id"

    cursor.execute(query)

    # Récupérer les résultats de la requête
    resultsUsers = cursor.fetchall()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    all_recipe_ids = []
    all_ingredient_ids = []
    all_users_ids = []

    for row in resultsRecipes:
        all_recipe_ids.append(row[0])

    for row in resultsIngredients:
        all_ingredient_ids.append(row[0])

    for row in resultsUsers:
        all_users_ids.append(row[0])
    
    return all_recipe_ids, all_ingredient_ids, all_users_ids


def create_vectors(data, all_user_ids, all_recipe_ids, all_ingredient_ids, save=True):
    # Créer un dictionnaire pour stocker les vecteurs pour chaque utilisateur
    user_vectors = {}

    # Boucle sur chaque utilisateur
    for user_data in all_user_ids:
        # Initialiser les listes de recettes et d'ingrédients à partir de 1
        max_recipe_id = max(all_recipe_ids)
        max_ingredient_id = max(all_ingredient_ids)
        recipes_ids = [0] * (max_recipe_id + 1)
        ingredient_ids = [0] * (max_ingredient_id + 1)

        # Initialiser le vecteur pour cet utilisateur avec des zéros
        user_vector = {}
        user_vector = (recipes_ids, ingredient_ids)

        # Mettre à jour le vecteur pour les recettes favorites de cet utilisateur
        for recipe_id in data[str(user_data)][0]:
            user_vector[0][int(recipe_id)] = 1
        
        # Mettre à jour le vecteur pour les ingrédients favoris de cet utilisateur
        for ingredient_id in data[str(user_data)][1]:
            user_vector[1][int(ingredient_id)] = 1

        user_vectors[str(user_data)] = user_vector
        
    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/knn_recommendation/data/user_vector.json", "w") as f:
            json.dump(user_vectors, f, indent=4)

    return user_vectors

def real_score(user_vectors, all_user_ids, save=True):
    score = {}

    # Boucle sur chaque utilisateur
    for i in all_user_ids:
        # Initialiser le dictionnaire de scores pour cet utilisateur
        user_score = {}
        
        # Boucle sur les autres utilisateurs
        for j in all_user_ids:
            if i != j:
                # Calculer le score de parité entre les vecteurs de recettes favorites
                recipe_score = sum(abs(a - b) for a, b in zip(user_vectors[str(i)][0], user_vectors[str(j)][0]))
                
                # Calculer le score de parité entre les vecteurs d'ingrédients favoris
                ingredient_score = sum(abs(a - b) for a, b in zip(user_vectors[str(i)][1], user_vectors[str(j)][1]))
                
                # Stocker les scores de parité dans le dictionnaire de scores pour cette paire d'utilisateurs
                user_score[str(j)] = {
                    "recipe_score": recipe_score,
                    "ingredient_score": ingredient_score
                }
            
        # Stocker le dictionnaire de scores pour cet utilisateur dans le dictionnaire de scores global
        score[str(i)] = user_score

    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/knn_recommendation/data/user_real_score.json", "w") as f:
            json.dump(score, f, indent=4)
    
    return score

def compute_scores(user_vectors, all_user_ids, save=True):
    # Calculer la moyenne des scores de recettes et d'ingrédients pour chaque paire d'utilisateurs
    user_similarity = {}
    for i in all_user_ids:
        user_similarity[str(i)] = {}
        for j in all_user_ids:
            if i != j:
                recipe_sum = sum([abs(a - b) for a, b in zip(user_vectors[str(i)][0], user_vectors[str(j)][0])])
                ingredient_sum = sum([abs(a - b) for a, b in zip(user_vectors[str(i)][1], user_vectors[str(j)][1])])
                # avg_score = (recipe_sum + ingredient_sum) / 2
                user_similarity[str(i)][str(j)] = recipe_sum

    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/knn_recommendation/data/user_scores.json", "w") as f:
            json.dump(user_similarity, f, indent=4)

    return user_similarity

def compute_nearest_neighbors(user_similarity, k, all_user_ids, save=True):
    # Trier les résultats par ordre décroissant pour obtenir les k plus proches voisins
    nearest_neighbors = {}
    for i in all_user_ids:
        sorted_similarity = sorted(user_similarity[str(i)].items(), key=lambda x: x[1])
        nearest_neighbors[str(i)] = {"nearest_N": [int(j[0]) for j in sorted_similarity[:k]]}

    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/knn_recommendation/data/user_nn.json", "w") as f:
            json.dump(nearest_neighbors, f, indent=4)

    return nearest_neighbors



all_recipe_ids, all_ingredient_ids, all_user_ids = get_data()

# Opening JSON file
with open('Data/applications/knn_recommendation/data/user_data.json') as f:  
    data = json.load(f)

user_vectors = create_vectors(data, all_user_ids, all_recipe_ids, all_ingredient_ids)
scores = real_score(user_vectors, all_user_ids)
user_similarity = compute_scores(user_vectors, all_user_ids)
k = 10
nearest_neighbors = compute_nearest_neighbors(user_similarity, k, all_user_ids)
