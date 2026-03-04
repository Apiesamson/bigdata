"""Étape 1 - Analyse exploratoire des données climatiques.

Ce script charge le fichier source et produit :
- des statistiques descriptives et un diagnostic des valeurs manquantes
- des agrégations simples (par année, pays)
- une figure récapitulative enregistrée dans le dossier outputs/
- un fichier texte de synthèse
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Dossier de sortie contenant les figures et les fichiers texte.
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# En-tête console (suivi de l'exécution).
print("="*70)
print("ÉTAPE 1 - ANALYSE EXPLORATOIRE DES DONNÉES CLIMATIQUES")
print("="*70)

# Chargement des données brutes.
df = pd.read_csv("GlobalLandTemperaturesByMajorCity.csv")

print("\n1. DIMENSIONS DU DATASET")
print("-"*70)
print(f"Nombre de lignes    : {df.shape[0]:,}")
print(f"Nombre de colonnes  : {df.shape[1]}")
print(f"Taille mémoire      : {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

print("\n2. TYPES DES VARIABLES")
print("-"*70)
print(df.dtypes)

print("\n3. APERÇU DES DONNÉES")
print("-"*70)
print(df.head(10))

print("\n4. STATISTIQUES DESCRIPTIVES")
print("-"*70)
print(df.describe())

print("\n5. VALEURS MANQUANTES")
print("-"*70)
# Calcul du nombre de NA par colonne et du pourcentage associé.
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Colonne': missing.index,
    'Valeurs manquantes': missing.values,
    'Pourcentage': missing_pct.values
})
print(missing_df)

print("\n6. NOMBRE DE VILLES ET PAYS UNIQUES")
print("-"*70)
print(f"Nombre de villes uniques : {df['City'].nunique()}")
print(f"Nombre de pays uniques   : {df['Country'].nunique()}")

# Figure récapitulative en 2x2.
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Sous-figure (0,0) : barres horizontales des NA par variable.
missing_data = df.isnull().sum()
missing_data = missing_data[missing_data > 0]
axes[0, 0].barh(missing_data.index, missing_data.values, color='coral')
axes[0, 0].set_xlabel('Nombre de valeurs manquantes')
axes[0, 0].set_title('Valeurs manquantes par variable')
axes[0, 0].grid(axis='x', alpha=0.3)

# Sous-figure (0,1) : histogramme de la distribution de température.
# On retire les lignes sans température pour éviter les valeurs invalides.
df_clean = df.dropna(subset=['AverageTemperature'])
axes[0, 1].hist(df_clean['AverageTemperature'], bins=50, color='skyblue', edgecolor='black')
axes[0, 1].set_xlabel('Température (°C)')
axes[0, 1].set_ylabel('Fréquence')
axes[0, 1].set_title('Distribution des températures moyennes')
axes[0, 1].grid(axis='y', alpha=0.3)

# Sous-figure (1,0) : évolution du nombre de mesures par année.
# Conversion de la date et extraction de l'année.
df['dt'] = pd.to_datetime(df['dt'])
df['Year'] = df['dt'].dt.year
yearly_data = df.groupby('Year').size()
axes[1, 0].plot(yearly_data.index, yearly_data.values, color='green', linewidth=2)
axes[1, 0].set_xlabel('Année')
axes[1, 0].set_ylabel('Nombre de mesures')
axes[1, 0].set_title('Nombre de mesures par année')
axes[1, 0].grid(alpha=0.3)

# Sous-figure (1,1) : top 10 pays en nombre d'observations.
top_countries = df['Country'].value_counts().head(10)
axes[1, 1].barh(range(len(top_countries)), top_countries.values, color='purple', alpha=0.7)
axes[1, 1].set_yticks(range(len(top_countries)))
axes[1, 1].set_yticklabels(top_countries.index)
axes[1, 1].set_xlabel('Nombre de mesures')
axes[1, 1].set_title('Top 10 des pays avec le plus de mesures')
axes[1, 1].grid(axis='x', alpha=0.3)

plt.tight_layout()
# Sauvegarde de la figure principale de l'étape 1.
plt.savefig(OUTPUT_DIR / "step1_exploratory_analysis.png", dpi=300, bbox_inches='tight')
print(f"\nVisualisations sauvegardées : {OUTPUT_DIR / 'step1_exploratory_analysis.png'}")

summary = {
    'total_lignes': df.shape[0],
    'total_colonnes': df.shape[1],
    'villes_uniques': df['City'].nunique(),
    'pays_uniques': df['Country'].nunique(),
    'valeurs_manquantes': int(df['AverageTemperature'].isnull().sum()),
    'taille_mb': df.memory_usage(deep=True).sum() / 1024**2,
    'periode_debut': df['Year'].min(),
    'periode_fin': df['Year'].max()
}

# Export d'un résumé textuel (utile pour le rapport).
with open(OUTPUT_DIR / "step1_summary.txt", 'w', encoding='utf-8') as f:
    f.write("RÉSUMÉ DE L'ANALYSE EXPLORATOIRE\n")
    f.write("="*50 + "\n\n")
    for key, value in summary.items():
        f.write(f"{key.replace('_', ' ').title()}: {value}\n")

print(f" Résumé sauvegardé : {OUTPUT_DIR / 'step1_summary.txt'}")
print("\n" + "="*70)
print("ANALYSE EXPLORATOIRE TERMINÉE AVEC SUCCÈS")
print("="*70)
