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

print(df)
