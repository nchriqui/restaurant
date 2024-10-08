import mysql.connector
import json

from Data.BD.config import config

def get_data():
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les id des recettes
    query = "SELECT DISTINCT recipe_id FROM consommations ORDER BY recipe_id"

    cursor.execute(query)

    # Récupérer les résultats de la requête
    resultsRecipes = cursor.fetchall()

    # Récupérer les id des utilisateurs
    query = "SELECT user_id FROM users ORDER BY user_id"

    cursor.execute(query)

    # Récupérer les résultats de la requête
    resultsUsers = cursor.fetchall()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    all_recipe_ids = []
    all_users_ids = []

    for row in resultsRecipes:
        all_recipe_ids.append(row[0])

    for row in resultsUsers:
        all_users_ids.append(row[0])
    
    return all_recipe_ids, all_users_ids


def create_vectors(data, all_users_ids, all_recipe_ids, save=True):
    # Créer un dictionnaire pour stocker les vecteurs pour chaque utilisateur
    user_vectors = {}

    # Boucle sur chaque utilisateur
    for user_data in all_users_ids:
        # Initialiser le vecteur pour cet utilisateur avec des zéros
        user_vector = [0] * len(all_recipe_ids)

        # Mettre à jour le vecteur pour les recettes favorites de cet utilisateur
        for recipe_id in data[str(user_data)]:
            if int(recipe_id) in all_recipe_ids:
                index = all_recipe_ids.index(int(recipe_id))
                user_vector[index] = 1

        user_vectors[str(user_data)] = user_vector
        
    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/knn_recommendation/data/user_vector_cons.json", "w") as f:
            json.dump(user_vectors, f, indent=4)

    return user_vectors

def real_score(user_vectors, all_users_ids, save=True):
    score = {}

    # Boucle sur chaque utilisateur
    for i in all_users_ids:
        # Initialiser le dictionnaire de scores pour cet utilisateur
        user_score = {}
        
        # Boucle sur les autres utilisateurs
        for j in all_users_ids:
            if i != j:
                # Calculer le score de parité entre les vecteurs de categories favorites
                recipe_score = sum(abs(a - b) for a, b in zip(user_vectors[str(i)], user_vectors[str(j)]))
                
                # Stocker les scores de parité dans le dictionnaire de scores pour cette paire d'utilisateurs
                user_score[str(j)] = {
                    "recipe_score": recipe_score
                }
            
        # Stocker le dictionnaire de scores pour cet utilisateur dans le dictionnaire de scores global
        score[str(i)] = user_score

    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/knn_recommendation/data/user_real_score_cons.json", "w") as f:
            json.dump(score, f, indent=4)
    
    return score

def compute_scores(user_vectors, all_users_ids, save=True):
    # Calculer la moyenne des scores de recettes et d'ingrédients pour chaque paire d'utilisateurs
    user_similarity = {}
    for i in all_users_ids:
        user_similarity[str(i)] = {}
        for j in all_users_ids:
            if i != j:
                recipe_sum = sum([abs(a - b) for a, b in zip(user_vectors[str(i)], user_vectors[str(j)])])
                user_similarity[str(i)][str(j)] = recipe_sum

    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/knn_recommendation/data/user_scores_cons.json", "w") as f:
            json.dump(user_similarity, f, indent=4)

    return user_similarity

def compute_nearest_neighbors(user_similarity, k, all_users_ids, save=True):
    # Trier les résultats par ordre décroissant pour obtenir les k plus proches voisins
    nearest_neighbors = {}
    for i in all_users_ids:
        sorted_similarity = sorted(user_similarity[str(i)].items(), key=lambda x: x[1])
        nearest_neighbors[str(i)] = {"nearest_N": [int(j[0]) for j in sorted_similarity[:k]]}

    if save:
        # Écrire les données dans un fichier JSON
        with open("Data/applications/knn_recommendation/data/user_nn_cons.json", "w") as f:
            json.dump(nearest_neighbors, f, indent=4)

    return nearest_neighbors



all_recipe_ids, all_users_ids = get_data()

# Opening JSON file
with open('Data/applications/knn_recommendation/data/user_data_cons.json') as f:  
    data = json.load(f)

user_vectors = create_vectors(data, all_users_ids, all_recipe_ids)
scores = real_score(user_vectors, all_users_ids)
user_similarity = compute_scores(user_vectors, all_users_ids)
k = 5
nearest_neighbors = compute_nearest_neighbors(user_similarity, k, all_users_ids)
