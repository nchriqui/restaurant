import json
import logging 
import sys

from similarity import (binarize_recipes_data_limited_ingredients,
                        calculate_scores,
                        compute_nearest_neighbors)

logging.basicConfig(level=logging.DEBUG,  # Niveau de journalisation (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(asctime)s - %(levelname)s - %(message)s')  # Format du message de log


def calculate_similarity(k :int = 10):
    with open("data/recipes_data_limited_ingredients.json") as f:
        data = json.load(f)

    recipes_binarized = binarize_recipes_data_limited_ingredients(data)
    logging.info("! Binarization Done")

    scores = calculate_scores(recipes_binarized)
    logging.info("! Scores Calculation done")

    nearest_neighbours = compute_nearest_neighbors(scores, k)
    logging.info("! Nearest N Done")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        argument = sys.argv[1]
        calculate_similarity(argument)
    else:
        print("Aucun argument n'a été fourni.")