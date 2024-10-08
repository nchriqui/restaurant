import json
import logging 
import sys 
import os
from generate_dataset_similarity import generate_recipes_data

from similarity import (binarize_recipes,
                        calculate_scores,
                        compute_nearest_neighbors,
                        compute_one_knn)

logging.basicConfig(level=logging.DEBUG,  # Niveau de journalisation (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(asctime)s - %(levelname)s - %(message)s')  # Format du message de log


def calculate_similarity(recipe_id, k :int = 5):
    file_path = "./data/recipes_data.json"
    if not os.path.exists(file_path):
        recipes_data = generate_recipes_data()
    else:
        with open(file_path) as f:
            recipes_data = json.load(f)

    recipes_binarized = binarize_recipes(recipes_data)
    logging.info("! Binarization Done")
    
    scores = compute_one_knn(str(recipe_id), recipes_binarized, k)
    logging.info("! Nearest N Done")

    knn = compute_nearest_neighbors(scores, k, False, "one_knn_out.json")
    logging.info("! {k} NN calculated")

    print(knn)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        k = sys.argv[1]
        recipe_id = sys.argv[2]
        calculate_similarity(recipe_id, k)
    else:
        print("Aucun argument n'a été fourni.")