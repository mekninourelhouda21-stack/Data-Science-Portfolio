import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ============================================================
# Projet perso : segmentation d'articles d'une friperie en ligne
# But : regrouper automatiquement les annonces en "profils"
# (genre : "bon plan qui part vite", "ca dort", "premium"...)
# pour pouvoir analyser un catalogue sans tout regarder a la main
# ============================================================

np.random.seed(24)
n_articles = 500

# -- 1. donnees fictives (a remplacer un jour par un vrai export Vinted/eBay) --
prix = np.random.uniform(5, 80, n_articles)             # prix de l'article en euros
nombre_vues = np.random.randint(10, 1500, n_articles)   # nb de vues sur l'annonce
jours_en_ligne = np.random.randint(1, 45, n_articles)   # depuis combien de temps c'est en ligne

df_fashion = pd.DataFrame({
    'Prix_Euros': prix,
    'Nombre_Vues': nombre_vues,
    'Jours_En_Ligne': jours_en_ligne
})

# feature en plus que j'ai ajoutee : les vues ne veulent pas dire grand chose seules,
# ce qui est interessant c'est la vitesse a laquelle l'annonce est vue (vues / jour)
# -> ca permet de distinguer un article populaire d'un article juste vieux
df_fashion['Vues_Par_Jour'] = df_fashion['Nombre_Vues'] / df_fashion['Jours_En_Ligne']

print("Apercu des articles :")
print(df_fashion.head())

# -- 2. normalisation --
# rappel pour moi : le KMeans calcule des distances entre points,
# si une colonne va jusqu'a 1500 et une autre jusqu'a 80, la premiere "ecrase" l'autre
# le StandardScaler met tout a la meme echelle (moyenne 0, ecart-type 1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_fashion)

# -- 3. methode du coude pour choisir k au lieu de le deviner --
# principe : on teste plusieurs k, on regarde l'inertie (= a quel point les points
# sont proches du centre de leur groupe), et on cherche le "coude" sur la courbe
# (le point ou ca arrete de beaucoup s'ameliorer)
inerties = []
valeurs_k = range(1, 9)
for i in valeurs_k:
    kmeans_test = KMeans(n_clusters=i, random_state=42, n_init=10)
    kmeans_test.fit(X_scaled)
    inerties.append(kmeans_test.inertia_)

plt.figure(figsize=(6, 4))
plt.plot(valeurs_k, inerties, marker='o')
plt.xlabel("Nombre de clusters (k)")
plt.ylabel("Inertie")
plt.title("Methode du coude")
plt.tight_layout()
plt.savefig("figs/elbow.png")
plt.close()
print("\n-> graphique du coude enregistre dans figs/elbow.png")

# d'apres mon graphique le coude est autour de k=3, donc je garde ca
k = 3
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df_fashion['Segment_Article'] = kmeans.fit_predict(X_scaled)

print("\nProfil moyen par segment :")
profil_clusters = df_fashion.groupby('Segment_Article').mean()
print(profil_clusters)

# -- 4. visualisation des clusters --
# je projette sur 2 dimensions (prix vs vues/jour) qui sont les plus parlantes
plt.figure(figsize=(6, 5))
scatter = plt.scatter(
    df_fashion['Prix_Euros'],
    df_fashion['Vues_Par_Jour'],
    c=df_fashion['Segment_Article'],
    cmap='viridis',
    alpha=0.6
)
plt.xlabel("Prix (euros)")
plt.ylabel("Vues par jour")
plt.title("Segments d'articles")
plt.colorbar(scatter, label="Segment")
plt.tight_layout()
plt.savefig("figs/clusters.png")
plt.close()
print("-> graphique des clusters enregistre dans figs/clusters.png")

# -- 5. nommage automatique des segments --
# plutot que de juste dire "Segment 0, 1, 2" je donne un nom qui a du sens
# en comparant chaque segment a la moyenne globale
def nommer_segment(ligne, moyennes_globales):
    nom = []
    nom.append("cher" if ligne['Prix_Euros'] > moyennes_globales['Prix_Euros'] else "abordable")
    nom.append("populaire" if ligne['Vues_Par_Jour'] > moyennes_globales['Vues_Par_Jour'] else "discret")
    return " / ".join(nom)

moyennes_globales = df_fashion[['Prix_Euros', 'Vues_Par_Jour']].mean()

print("\nInterpretation des segments :")
for cluster_id in range(k):
    sub_cluster = df_fashion[df_fashion['Segment_Article'] == cluster_id]
    nom_segment = nommer_segment(sub_cluster.mean(), moyennes_globales)
    print(f"\nSegment {cluster_id} ({nom_segment}) :")
    print(f" - prix moyen : {sub_cluster['Prix_Euros'].mean():.2f} euros")
    print(f" - vues/jour moyennes : {sub_cluster['Vues_Par_Jour'].mean():.1f}")
    print(f" - temps en ligne moyen : {sub_cluster['Jours_En_Ligne'].mean():.1f} jours")
    print(f" - nb d'articles dans ce segment : {len(sub_cluster)}")