import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# 1. SIMULATION DE DONNÉES PSYCHOLINGUISTIQUES (Modélisation cognitive)
np.random.seed(101)
n_mots = 400
longueur_mot = np.random.randint(3, 15, n_mots)        # Nombre de lettres du mot
frequence_langue = np.random.uniform(1, 100, n_mots)   # Plus le score est haut, plus le mot est courant

# Nombre de syllabes : corrélé à la longueur mais PAS purement déterministe.
# On ajoute une variation indépendante pour éviter une colinéarité parfaite
# avec Longueur_Lettres (deux mots de même longueur n'ont pas forcément
# le même nombre de syllabes en réalité).
bruit_syllabes = np.random.normal(0, 0.6, n_mots)
nb_syllabes = np.clip(np.round(longueur_mot / 2.5 + bruit_syllabes), 1, None).astype(int)

# Le temps de fixation oculaire (en ms) augmente avec la complexité et diminue avec la familiarité
temps_fixation = 150 + (longueur_mot * 15) - (frequence_langue * 0.8) + np.random.normal(0, 15, n_mots)
temps_fixation = np.clip(temps_fixation, 120, None)    # Temps de fixation minimum réaliste

df_ling = pd.DataFrame({
    'Longueur_Lettres': longueur_mot,
    'Nombre_Syllabes': nb_syllabes,
    'Frequence_Usage': frequence_langue,
    'Temps_Fixation_ms': temps_fixation
})

print("--- Base de Données Psycholinguistique (LexiMind) ---")
print(df_ling.head(), "\n")

# Vérification rapide de la colinéarité entre les variables explicatives
print("--- Matrice de corrélation des variables explicatives ---")
print(df_ling[['Longueur_Lettres', 'Nombre_Syllabes', 'Frequence_Usage']].corr(), "\n")

# 2. MODÉLISATION PRÉDICTIVE (Régression Linéaire Multiple)
X = df_ling[['Longueur_Lettres', 'Nombre_Syllabes', 'Frequence_Usage']]
y = df_ling['Temps_Fixation_ms']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Entraînement du modèle de régression linéaire...")
model_ling = LinearRegression()
model_ling.fit(X_train, y_train)

# Affichage des coefficients, désormais plus interprétables individuellement
print("\n--- Coefficients du modèle ---")
for nom_variable, coef in zip(X.columns, model_ling.coef_):
    print(f"{nom_variable} : {coef:.3f}")
print(f"Intercept : {model_ling.intercept_:.3f}")

# 3. ÉVALUATION DES PERFORMANCES DU MODÈLE
y_pred = model_ling.predict(X_test)
print("\n--- Performance du modèle LexiMind ---")
print(f"Erreur moyenne absolue (MAE) : {mean_absolute_error(y_test, y_pred):.2f} ms")
print(f"Score de corrélation R² : {r2_score(y_test, y_pred) * 100:.2f}%")
