import json

import mysql.connector

from generate_dataset_similarity import *

RECIPES_COUNT = 45772
INGREDIENTS_COUNT = 1105

def binarize_recipes(
    recipes_dic,
    recipes_count=RECIPES_COUNT,
    ingredients_count=INGREDIENTS_COUNT,
    save=True,
):
    recipes_binarized = {}
    for i in recipes_dic:
        recipes_binarized[str(i)] = [0] * (ingredients_count)
    for i in range(1, recipes_count + 1):
        if str(i) in recipes_dic:
            for id in recipes_dic[str(i)]:
                recipes_binarized[str(i)][int(id) - 1] = 1
    if save:
        # Écrire les données dans un fichier JSON
        with open("data/recipes_binarized.json", "w") as f:
            json.dump(recipes_binarized, f)

    return recipes_binarized


def calculate_scores(recipes_binarized, save=True, file_name="scores.json"):
    scores = {}  # {ID_recipe : {id_recipe : distance }}
    for id in recipes_binarized:
        print(id)
        scores[id] = {}
        for i in recipes_binarized:
            scores[id][i] = sum(
                abs(a - b)
                for a, b in zip(recipes_binarized[id], recipes_binarized[str(i)])
            )

    if save:
        # Écrire les données dans un fichier JSON
        with open(f"data/{file_name}", "w") as f:
            json.dump(scores, f)

    return scores


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
        with open(f"data/{file_name}", "w") as f:
            json.dump(scores, f)

    return scores

def compute_nearest_neighbors(user_similarity, k, save=True, file_name = "kNN_computed.json"):
    nearest_neighbors = {}
    for i in user_similarity:
        sorted_similarity = sorted(user_similarity[str(i)].items(), key=lambda x: x[1])
        nearest_neighbors[str(i)] = {
            "nearest_N": [int(j[0]) for j in sorted_similarity[1 : k + 1]]
        }

    if save:
        # Écrire les données dans un fichier JSON
        with open(f"data/{file_name}", "w") as f:
            json.dump(nearest_neighbors, f, indent=4)

    return nearest_neighbors

    


def binarize_recipes_data_limited_ingredients(recipes_dic, save=True):
    recipes_binarized = {}
    all_ingredients_id = extract_all_ingredients_with_chosen_type()
    print(all_ingredients_id)
    for i in recipes_dic:
        recipes_binarized[i] = [0] * (len(all_ingredients_id))
        for id in recipes_dic[i]:
            recipes_binarized[i][int(all_ingredients_id.index(id))] = 1

    if save:
        # Écrire les données dans un fichier JSON
        with open("data/binarized_recipes_data_limited_ingredients.json", "w") as f:
            json.dump(recipes_binarized, f)

    return recipes_binarized


def binarize_recipes_data_origines(recipes_dic, save=True):
    recipes_binarized = {}
    all_cuisines = extract_all_cuisines()
    all_types = extract_all_types()

    for i in recipes_dic:
        recipes_binarized[i] = ([0] * len(all_types), [0] * len(all_cuisines))
        for id in recipes_dic[i][0]:
            recipes_binarized[i][0][all_types.index(id)] = 1
        recipes_binarized[i][1][all_cuisines.index(recipes_dic[i][1])] = 1

    if save:
        # Écrire les données dans un fichier JSON
        with open("data/binarized_recipes_data_origines.json", "w") as f:
            json.dump(recipes_binarized, f)

    return recipes_binarized


def calculate_scores_tuples(recipes_binarized, save=True):
    scores = {}  # {ID_recipe : {id_recipe : distance }}
    for id in recipes_binarized:
        scores[id] = {}
        for i in recipes_binarized:
            scores[id][i] = sum(
                abs(a - b)
                for a, b in zip(recipes_binarized[id][0], recipes_binarized[str(i)][0])
            )
            # Donner un poids supp ? Trouver un truc de ouf
            # scores[id][i] = sum(abs(a - b) for a, b in zip(recipes_binarized[id][1], recipes_binarized[str(i)][1]))

    if save:
        # Écrire les données dans un fichier JSON
        with open("scores.json", "w") as f:
            json.dump(scores, f)

    return scores


if __name__ == "__main__":
    with open("data/recipes_data_origines.json") as f:
        data = json.load(f)
    binarize_recipes_data_origines(data)

    # with open('recipes_data.json') as f:
    #     data = json.load(f)

    # recipes_binarized = binarize_recipes(data)

    # with open("binarized_recipes.json") as f:
    #     recipes_binarized = json.load(f)

    # print("---------")
    # scores = calculate_scores(recipes_binarized)
