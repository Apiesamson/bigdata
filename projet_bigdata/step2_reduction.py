import pandas as pd

# 1. Chargement des données
df = pd.read_csv("GlobalLandTemperaturesByMajorCity.csv")

# 2. Conversion de la colonne date en datetime
df['dt'] = pd.to_datetime(df['dt'])

# 3. Suppression des valeurs manquantes sur la température
df = df.dropna(subset=['AverageTemperature'])

# 4. Filtrage des données à partir de 1950
df_reduced = df[df['dt'].dt.year >= 1950]

# 5. Vérification du nouveau volume
print("Dimensions du dataset réduit :", df_reduced.shape)

# 6. Sauvegarde du nouveau dataset
df_reduced.to_csv("dataset_reduced.csv", index=False)

print("Dataset réduit sauvegardé avec succès.")