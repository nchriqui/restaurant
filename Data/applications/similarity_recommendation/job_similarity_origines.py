import json
import logging 
import sys
from generate_dataset_similarity import generate_recipes_origines 

from similarity import (binarize_recipes,
                        calculate_scores_tuples,
                        compute_nearest_neighbors)

logging.basicConfig(level=logging.DEBUG,  # Niveau de journalisation (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(asctime)s - %(levelname)s - %(message)s')  # Format du message de log


def calculate_similarity_origines(k :int = 10):
    #with open("data/recipes_data_origines.json") as f:
    #   data = json.load(f)

    data = generate_recipes_origines()

    recipes_binarized = binarize_recipes(data, 44059, 21 )
    logging.info("! Binarization Done")

    scores = calculate_scores_tuples(recipes_binarized, )
    logging.info("! Scores Calculation done")

    nearest_neighbours = compute_nearest_neighbors(scores, k)
    logging.info("! Nearest N Done")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        k = sys.argv[1]
        calculate_similarity_origines(k)
    else:
        print("Aucun argument n'a été fourni.")