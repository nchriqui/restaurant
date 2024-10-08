import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# Données d'exemple
X = np.array([[1, 2, 3, 4, 5], [1.5, 1.8, 2.2, 4.1, 4.9], [5, 8, 2.5, 3.2, 6.5],
              [8, 8, 9, 1, 2], [1, 0.6, 1.2, 3.7, 2.5], [9, 11, 7.5, 6, 5]])
recipe_ids = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']

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
