import json
import random
from functools import partial
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from RecoWindow import Ui_RecoPage
from reco_appli import *

class RecoUI(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.ui = Ui_RecoPage()
        self.ui.setupUi(self)

        self.ui.spinBox.setValue(5)
        self.ui.spinBox.setMinimum(1)
        self.ui.spinBox.setMaximum(5)
        self.go_2_counter = 0  # Compteur initialisé à 0

        # Masquer les éléments restants
        for i in range(5):
            getattr(self.ui, f"reco_sim_{i+1}").setVisible(False)
            getattr(self.ui, f"origine_{i+1}").setVisible(False)
            getattr(self.ui, f"like_sim_{i+1}").setVisible(False)

        generate_knn_categories()

        all_ingredient_cats, all_users_ids = get_data()
        # Opening JSON file
        with open('Data/applications/knn_recommendation/data/user_data_cat.json') as f:  
            all_data = json.load(f)
        
        if len(all_data[str(user_id)]) == 0:
            res = all_recipes()
            print("Recettes aléatoires car pas de préférences")
        else:
            user_vectors = create_vectors(all_data, all_users_ids, all_ingredient_cats)
            user_similarity = compute_scores(user_vectors, all_users_ids)
            k = 5
            compute_nearest_neighbors_u2u(user_similarity, k, all_users_ids)

            # Opening JSON file
            with open('Data/applications/knn_recommendation/data/user_nn_cat.json') as f:  
                data = json.load(f)

            res = recipes_colaboratif(user_id, data)

        if res == -1:
            res = all_recipes()

        indices = random.sample(range(len(res["name"])), 5)

        for i, index in enumerate(indices, start=1):
            getattr(self.ui, f"user_reco_{i}").setText(res["name"][index])
            getattr(self.ui, f"lcdNumber_{i}").display(res["price"][index])

            recipe_id = res["recipe_id"][index]
            checkbox = getattr(self.ui, f"like_user_{i}")
            checkbox.setChecked(check_favorite(recipe_id, user_id))
            checkbox.clicked.connect(partial(self.handle_checkbox_clicked, recipe_id, user_id))

        button_clicked_callback_sim = partial(self.similarity_recommandation, user_id=user_id)
        self.ui.go.clicked.connect(button_clicked_callback_sim)

        button_clicked_callback = partial(self.user_2_user_recommandation, user_id=user_id)
        self.ui.go_2.clicked.connect(button_clicked_callback)

    def handle_checkbox_clicked(self, recipe_id, user_id):
        checkbox = self.sender()
        if checkbox.isChecked():
            add_favorite(recipe_id, user_id)
        else:
            remove_favorite(recipe_id, user_id)


    def similarity_recommandation(self, user_id):
        recipe_name = self.ui.recipe_name.text().strip()
        k = self.ui.spinBox.value()

        for i in range(5):
            getattr(self.ui, f"reco_sim_{i+1}").setVisible(False)
            getattr(self.ui, f"origine_{i+1}").setVisible(False)
            getattr(self.ui, f"like_sim_{i+1}").setVisible(False)

        id = str(get_recipe_id(recipe_name))
        if id == "-1":
            QMessageBox.critical(self, "Nom de recette invalide", "Pas de recettes avec ce nom disponible")
            print("Pas de recettes avec ce nom disponible")
            return -1

        with open("Data/applications/similarity_recommendation/data/recipes_binarized.json") as f:
            recipes_binarized = json.load(f)

        scores = compute_one_knn(id, recipes_binarized)
        knn = compute_nearest_neighbors(scores, k, False)
        res = get_recipes_from_id(id, knn)

        k = min(k, len(res["name"]), len(res["origine"]))

        for i in range(k):
            getattr(self.ui, f"reco_sim_{i+1}").setVisible(True)
            getattr(self.ui, f"reco_sim_{i+1}").setText(res["name"][i])

            getattr(self.ui, f"origine_{i+1}").setVisible(True)
            getattr(self.ui, f"origine_{i+1}").setText(res["origine"][i])

            getattr(self.ui, f"like_sim_{i+1}").setVisible(True)
            recipe_id = res["recipe_id"][i]
            checkbox = getattr(self.ui, f"like_sim_{i+1}")
            checkbox.setChecked(check_favorite(recipe_id, user_id))
            checkbox.clicked.connect(partial(self.handle_checkbox_clicked, recipe_id, user_id))


    def user_2_user_recommandation(self, user_id):
        self.go_2_counter += 1  # Incrémenter le compteur à chaque clic

        if self.go_2_counter % 3 == 0:
            generate_knn_categories()

            all_ingredient_cats, all_users_ids = get_data()
            # Opening JSON file
            with open('Data/applications/knn_recommendation/data/user_data_cat.json') as f:  
                all_data = json.load(f)

            if len(all_data[str(user_id)]) == 0:
                print("Recettes aléatoires car pas de préférences")
            else:
                user_vectors = create_vectors(all_data, all_users_ids, all_ingredient_cats)
                user_similarity = compute_scores(user_vectors, all_users_ids)
                k = 5
                compute_nearest_neighbors_u2u(user_similarity, k, all_users_ids)

            print("Résultats actualisés")



        with open('Data/applications/knn_recommendation/data/user_data_cat.json') as f:  
            all_data = json.load(f)
        
        if len(all_data[str(user_id)]) == 0:
            res = all_recipes()
        else:
            # Opening JSON file
            with open('Data/applications/knn_recommendation/data/user_nn_cat.json') as f:  
                data = json.load(f)

            res = recipes_colaboratif(user_id, data)

        if res == -1:
            res = all_recipes()
        
        indices = random.sample(range(len(res["name"])), 5)

        for i, index in enumerate(indices, start=1):
            getattr(self.ui, f"user_reco_{i}").setText(res["name"][index])
            getattr(self.ui, f"lcdNumber_{i}").display(res["price"][index])

            recipe_id = res["recipe_id"][index]
            checkbox = getattr(self.ui, f"like_user_{i}")
            checkbox.setChecked(check_favorite(recipe_id, user_id))
            checkbox.clicked.connect(partial(self.handle_checkbox_clicked, recipe_id, user_id))

if __name__ == '__main__':
    app = QApplication([])
    reco_page = RecoUI("304")
    reco_page.show()
    app.exec()