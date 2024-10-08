import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import json

# Chargement du dataset de recettes et d'ingrédients
with open(
    "C:/Users/ulyss/Workspace/pipo-resto/Data/applications/similarity_recommendation/data/recipes_data_origines.json"
) as f:
    data = json.load(f)

# Récupération des ingrédients de chaque recette
recipes = list(data.values())
ingredients_list = [recipe[0] for recipe in recipes]

# Encodage des ingrédients
label_encoder = LabelEncoder()
all_ingredients = np.unique(np.concatenate(ingredients_list))
label_encoder.fit(all_ingredients)

# Encodage des ingrédients de chaque recette
encoded_recipes = []
for ingredients in ingredients_list:
    encoded_ingredients = label_encoder.transform(ingredients)
    encoded_recipes.append(encoded_ingredients)

# Conversion des données en format numpy
X = np.array(encoded_recipes, dtype=object)
y = np.arange(len(X))

# Création du modèle de réseau de neurones à cinq couches
model = Sequential()
model.add(Dense(256, input_dim=X.shape[1], activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(X.shape[0], activation='softmax'))

# Compilation et entraînement du modèle
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=10, batch_size=32)

# Sauvegarde de l'architecture du modèle
model_json = model.to_json()
with open("model_architecture.json", "w") as json_file:
    json_file.write(model_json)

# Sauvegarde des poids du modèle
model.save_weights("model_weights.h5")

# Sauvegarde de la liste des ingrédients
ingredients_df = pd.DataFrame({'ingredient': all_ingredients})
ingredients_df.to_csv('ingredients_list.csv', index=False)

# Encodage de la recette de référence pour la prédiction
reference_recipe = [
    "Boisson Alcoolisée",
    "Céréales",
    "Herbe",
    "Légume",
    "Produits laitiers"
]
encoded_reference_recipe = label_encoder.transform(reference_recipe)


# Chargement de l'architecture du modèle
with open('model_architecture.json', 'a') as json_file:
    loaded_model_json = json_file.read()

loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model_weights.h5")

# Prédiction de la recette recommandée
encoded_reference_recipe = np.array([encoded_reference_recipe])
prediction = loaded_model.predict(encoded_reference_recipe)
predicted_recipe_index = np.argmax(prediction)
predicted_recipe = list(data.keys())[predicted_recipe_index]

# Affichage de la recette recommandée
print("Recette recommandée :", predicted_recipe)
