import pandas as pd

# Charger le dataset réduit
df = pd.read_csv("dataset_reduced.csv")

# Calcul des quantiles
q1 = df['AverageTemperature'].quantile(0.33)
q2 = df['AverageTemperature'].quantile(0.66)

print("Seuil 33% :", q1)
print("Seuil 66% :", q2)

# Création de la variable cible
def classify_temp(temp):
    if temp <= q1:
        return "Basse"
    elif temp <= q2:
        return "Moyenne"
    else:
        return "Élevée"

df['temperature_class'] = df['AverageTemperature'].apply(classify_temp)

# Vérification de la répartition des classes
print("\nRépartition des classes :")
print(df['temperature_class'].value_counts())

# Sauvegarde
df.to_csv("dataset_with_target.csv", index=False)

print("\nDataset avec variable cible sauvegardé.")