import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

# projet perso : essayer de detecter l'etat de concentration a partir de donnees EEG simulees
# idee de base : ondes Beta hautes + temps de reaction court = plutot concentre
np.random.seed(42)
n_sujets = 600

ondes_alpha = np.random.uniform(8, 12, n_sujets)    # ondes alpha (plutot relaxation/distraction)
ondes_beta = np.random.uniform(12, 30, n_sujets)    # ondes beta (plutot concentration)
temps_reaction_ms = np.random.uniform(200, 800, n_sujets)

# score "invente" pour fabriquer le label, juste pour avoir un dataset coherent a tester
score_attention = (ondes_beta * 2) - (ondes_alpha * 1.5) - (temps_reaction_ms * 0.05)
etat_cognitif = (score_attention > np.median(score_attention)).astype(int)  # 0 = distrait, 1 = concentre

df_cog = pd.DataFrame({
    'Ondes_Alpha_Hz': ondes_alpha,
    'Ondes_Beta_Hz': ondes_beta,
    'Temps_Reaction_ms': temps_reaction_ms,
    'Etat_Concentration': etat_cognitif
})

print("Apercu des donnees :")
print(df_cog.head())

# separation + normalisation (important pour le SVM, sinon les echelles differentes faussent les distances)
X = df_cog[['Ondes_Alpha_Hz', 'Ondes_Beta_Hz', 'Temps_Reaction_ms']]
y = df_cog['Etat_Concentration']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # fit que sur le train, sinon ca fuite des infos du test

# SVM lineaire, plus simple a interpreter qu'un kernel rbf pour commencer
model_cog = SVC(kernel='linear', random_state=42)
model_cog.fit(X_train_scaled, y_train)

y_pred = model_cog.predict(X_test_scaled)
print(f"\nPrecision : {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(classification_report(y_test, y_pred, target_names=['Distrait', 'Concentre']))

# petit plus : avec un kernel lineaire on peut regarder les coefficients
# ca montre quelle variable pese le plus dans la decision du modele
poids = pd.Series(model_cog.coef_[0], index=X.columns).sort_values(key=abs, ascending=False)
print("Poids des variables dans la decision :")
print(poids)