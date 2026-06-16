import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# on fixe la seed pour avoir toujours les memes resultats
# (sinon ca change a chaque execution et c'est chiant pour comparer avec le prof)
np.random.seed(42)
n_samples = 1000

# simulation des donnees de capteurs solaires (projet SUNe)
# en gros : plus il y a de lumiere, plus ca produit
# mais quand ca chauffe trop le rendement baisse (effet de surchauffe classique sur les panneaux)
lux = np.random.uniform(500, 100000, n_samples)
temperature = np.random.uniform(15, 45, n_samples)
humidite = np.random.uniform(20, 80, n_samples)

# formule "inventee" pour la puissance de sortie, avec du bruit pour que ce soit pas trop parfait
puissance_sortie = (lux * 0.005) - (temperature * 2.5) - (humidite * 0.1) + np.random.normal(0, 10, n_samples)
puissance_sortie = np.clip(puissance_sortie, 0, None)  # une puissance negative ca veut rien dire

df_solar = pd.DataFrame({
    'Intensite_Lumineuse_Lux': lux,
    'Temperature_C': temperature,
    'Humidite_Pourcentage': humidite,
    'Puissance_Sortie_mW': puissance_sortie
})

print("Apercu du dataset :")
print(df_solar.head())

# separation train/test, 80/20 comme d'habitude
X = df_solar[['Intensite_Lumineuse_Lux', 'Temperature_C', 'Humidite_Pourcentage']]
y = df_solar['Puissance_Sortie_mW']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# (au debut j'avais ecrit test_test_split par erreur, du coup ca plantait direct -> corrige)

# entrainement, RandomForest parce que c'est ce qu'on a fait en TD
print("\nEntrainement du modele...")
model_sune = RandomForestRegressor(n_estimators=100, random_state=42)
model_sune.fit(X_train, y_train)

# evaluation rapide
y_pred = model_sune.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nResultats :")
print("RMSE =", round(rmse, 2), "mW")
print("R2 =", round(r2 * 100, 2), "%")

# petit test avec un cas concret : panneau en plein soleil
nouveau_contexte = pd.DataFrame([[85000, 32, 40]], columns=X.columns)
prediction = model_sune.predict(nouveau_contexte)
print("\nPour 85000 lux, 32 degres et 40% d'humidite, puissance estimee :", round(prediction[0], 2), "mW")