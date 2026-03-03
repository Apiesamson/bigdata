import pandas as pd

# Charger dataset avec variable cible
df = pd.read_csv("dataset_with_target.csv")

# Conversion date
df['dt'] = pd.to_datetime(df['dt'])

# Extraction année et mois
df['Year'] = df['dt'].dt.year
df['Month'] = df['dt'].dt.month

# Suppression variables inutiles
df_final = df.drop(columns=[
    'dt',
    'AverageTemperature',
    'AverageTemperatureUncertainty'
])

# Vérification valeurs manquantes
print("Valeurs manquantes restantes :")
print(df_final.isnull().sum())

print("\nDimensions finales :")
print(df_final.shape)

# Sauvegarde fichier final
df_final.to_csv("dataset_final_sipina.csv", index=False)

print("\nFichier prêt pour Sipina sauvegardé.")