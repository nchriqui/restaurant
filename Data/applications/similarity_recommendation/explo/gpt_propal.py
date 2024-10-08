import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Collecte des données
data = [
    {
        "nom": "Spaghetti bolognaise",
        "type": "plat",
        "viande": "boeuf",
        "apport_calorique": 500,
        "epicee": False,
    },
    {
        "nom": "Tarte aux pommes",
        "type": "dessert",
        "viande": "vegetarien",
        "apport_calorique": 300,
        "epicee": False,
    },
    {
        "nom": "Poulet tandoori",
        "type": "plat",
        "viande": "poulet",
        "apport_calorique": 600,
        "epicee": True,
    },
    {
        "nom": "Salade de quinoa",
        "type": "entree",
        "viande": "vegetarien",
        "apport_calorique": 400,
        "epicee": False,
    },
    {
        "nom": "Saumon grille",
        "type": "plat",
        "viande": "poisson",
        "apport_calorique": 450,
        "epicee": False,
    },
]

# Prétraitement des données
df = pd.DataFrame(data)
df = pd.get_dummies(df, columns=["type", "viande", "epicee"])

# Construction de la matrice de caractéristiques
features = df.drop(["nom"], axis=1)

# Calcul de la similarité
similarity_matrix = cosine_similarity(features)


# Fonction de recommandation
def recommend_similar_recipes(recipe_name, num_recommendations=3):
    # Trouver l'index de la recette donnée
    index = df[df["nom"] == recipe_name].index[0]
    # Calculer la similarité entre la recette donnée et toutes les autres recettes
    similar_recipes = list(enumerate(similarity_matrix[index]))
    # Trier les recettes en fonction de leur similarité décroissante
    sorted_similar_recipes = sorted(similar_recipes, key=lambda x: x[1], reverse=True)
    # Sélectionner les recettes similaires (à l'exception de la recette donnée)
    top_similar_recipes = sorted_similar_recipes[1 : num_recommendations + 1]
    # Afficher les recettes similaires
    print(f"Recettes similaires à '{recipe_name}':")
    for recipe in top_similar_recipes:
        print(df.iloc[recipe[0]]["nom"])


# Exemple d'utilisation
recommend_similar_recipes("Spaghetti bolognaise", num_recommendations=3)
