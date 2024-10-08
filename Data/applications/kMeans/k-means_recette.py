import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# Données d'exemple
data = {
        "1": [1, 1, 1, 0, 0, 0],
        "2": [0, 0, 0, 1, 1, 0],
        "3": [0, 0, 1, 1, 0, 1],
        "4": [0, 0, 0, 0, 0, 1],
        "5": [1, 0, 0, 0, 0, 0],
        "7": [0, 0, 0, 0, 1, 0],
    }

# Extraction des ID de recette et des listes d'ingrédients
recipe_ids = list(data.keys())
ingredient_lists = list(data.values())

# Conversion des listes d'ingrédients en une matrice numpy
X = np.array(ingredient_lists)

# Création de l'objet KMeans avec 2 clusters
kmeans = KMeans(n_clusters=2)

# Entraînement de l'algorithme sur les données
kmeans.fit(X)

# Obtenir les labels des clusters et les centroïdes
cluster_labels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_

# Tracé des points avec couleurs correspondant aux clusters
plt.scatter(X[:, 0], X[:, 1], c=cluster_labels)
plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], marker='x', color='red')

# Étiquetage des points avec les ID de recette
for i, txt in enumerate(recipe_ids):
    plt.annotate(txt, (X[i, 0], X[i, 1]), textcoords="offset points", xytext=(0,10), ha='center')

# Affichage du graphique
plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.title('K-means Clustering')
plt.show()
