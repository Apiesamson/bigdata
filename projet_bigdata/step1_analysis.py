import pandas as pd

# Charger le fichier
df = pd.read_csv("GlobalLandTemperaturesByMajorCity.csv")

# 1. Dimensions
print("Nombre de lignes :", df.shape[0])
print("Nombre de colonnes :", df.shape[1])

# 2. Types de variables
print("\nTypes des variables :")
print(df.dtypes)

# 3. Aperçu des données
print("\nPremières lignes :")
print(df.head())

# 4. Valeurs manquantes
print("\nValeurs manquantes :")
print(df.isnull().sum())

# 5. Taille mémoire
print("\nTaille mémoire (MB) :")
print(df.memory_usage(deep=True).sum() / 1024**2)
