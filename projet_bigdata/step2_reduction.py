import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*70)
print("ÉTAPE 2 - RÉDUCTION DU VOLUME DE DONNÉES")
print("="*70)

print("\n1. CHARGEMENT DES DONNÉES")
print("-"*70)
df = pd.read_csv("GlobalLandTemperaturesByMajorCity.csv")
print(f"Dimensions initiales : {df.shape[0]:,} lignes × {df.shape[1]} colonnes")

print("\n2. CONVERSION DE LA DATE")
print("-"*70)
df['dt'] = pd.to_datetime(df['dt'])
df['Year'] = df['dt'].dt.year
print(f"Période couverte : {df['Year'].min()} - {df['Year'].max()}")

print("\n3. SUPPRESSION DES VALEURS MANQUANTES")
print("-"*70)
missing_before = df['AverageTemperature'].isnull().sum()
df_clean = df.dropna(subset=['AverageTemperature'])
missing_after = df_clean['AverageTemperature'].isnull().sum()
print(f"Valeurs manquantes supprimées : {missing_before:,}")
print(f"Lignes restantes : {len(df_clean):,}")

print("\n4. FILTRAGE TEMPOREL (≥ 1950)")
print("-"*70)
YEAR_THRESHOLD = 1950
df_reduced = df_clean[df_clean['Year'] >= YEAR_THRESHOLD].copy()
print(f"Lignes après filtrage : {len(df_reduced):,}")
reduction_pct = ((len(df) - len(df_reduced)) / len(df)) * 100
print(f"Réduction du volume : {reduction_pct:.1f}%")

print("\n5. STATISTIQUES COMPARATIVES")
print("-"*70)
stats_comparison = pd.DataFrame({
    'Dataset original': [
        len(df),
        df['AverageTemperature'].mean(),
        df['AverageTemperature'].std(),
        df['Year'].min(),
        df['Year'].max()
    ],
    'Dataset réduit': [
        len(df_reduced),
        df_reduced['AverageTemperature'].mean(),
        df_reduced['AverageTemperature'].std(),
        df_reduced['Year'].min(),
        df_reduced['Year'].max()
    ]
}, index=['Nombre de lignes', 'Température moyenne', 'Écart-type', 'Année min', 'Année max'])
print(stats_comparison)

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

stages = ['Original', 'Sans NA', 'Filtré\n(≥1950)']
counts = [len(df), len(df_clean), len(df_reduced)]
colors = ['#ff9999', '#ffcc99', '#99ccff']
axes[0, 0].bar(stages, counts, color=colors, edgecolor='black', linewidth=1.5)
axes[0, 0].set_ylabel('Nombre de lignes')
axes[0, 0].set_title('Évolution du volume de données')
axes[0, 0].grid(axis='y', alpha=0.3)
for i, v in enumerate(counts):
    axes[0, 0].text(i, v + 5000, f'{v:,}', ha='center', va='bottom', fontweight='bold')

yearly_counts_original = df.groupby('Year').size()
yearly_counts_reduced = df_reduced.groupby('Year').size()
axes[0, 1].plot(yearly_counts_original.index, yearly_counts_original.values, 
                label='Original', linewidth=2, alpha=0.7, color='red')
axes[0, 1].plot(yearly_counts_reduced.index, yearly_counts_reduced.values, 
                label='Réduit (≥1950)', linewidth=2, color='blue')
axes[0, 1].axvline(x=YEAR_THRESHOLD, color='green', linestyle='--', linewidth=2, label='Seuil 1950')
axes[0, 1].set_xlabel('Année')
axes[0, 1].set_ylabel('Nombre de mesures')
axes[0, 1].set_title('Distribution temporelle des données')
axes[0, 1].legend()
axes[0, 1].grid(alpha=0.3)

axes[1, 0].hist(df['AverageTemperature'].dropna(), bins=50, alpha=0.5, 
                label='Original', color='red', edgecolor='black')
axes[1, 0].hist(df_reduced['AverageTemperature'], bins=50, alpha=0.7, 
                label='Réduit', color='blue', edgecolor='black')
axes[1, 0].set_xlabel('Température (°C)')
axes[1, 0].set_ylabel('Fréquence')
axes[1, 0].set_title('Distribution des températures')
axes[1, 0].legend()
axes[1, 0].grid(axis='y', alpha=0.3)

labels = ['Données\nsupprimées', 'Données\nconservées']
sizes = [len(df) - len(df_reduced), len(df_reduced)]
colors_pie = ['#ff6b6b', '#4ecdc4']
explode = (0.05, 0)
axes[1, 1].pie(sizes, explode=explode, labels=labels, colors=colors_pie, 
               autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
axes[1, 1].set_title('Proportion de données conservées')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "step2_data_reduction.png", dpi=300, bbox_inches='tight')
print(f"\nVisualisations sauvegardées : {OUTPUT_DIR / 'step2_data_reduction.png'}")

df_reduced.to_csv("dataset_reduced.csv", index=False)
print(f"Dataset réduit sauvegardé : dataset_reduced.csv")

with open(OUTPUT_DIR / "step2_justification.txt", 'w', encoding='utf-8') as f:
    f.write("JUSTIFICATION DE LA STRATÉGIE DE RÉDUCTION\n")
    f.write("="*50 + "\n\n")
    f.write("Stratégie choisie : Filtrage temporel (≥ 1950)\n\n")
    f.write("Justifications :\n")
    f.write("1. Qualité des données : Les mesures modernes sont plus fiables\n")
    f.write("2. Pertinence métier : Données récentes plus utiles pour l'analyse\n")
    f.write("3. Volume conservé : 76,407 lignes (suffisant pour l'analyse)\n")
    f.write(f"4. Réduction : {reduction_pct:.1f}% du volume initial\n\n")
    f.write("Résultats :\n")
    f.write(f"- Lignes originales : {len(df):,}\n")
    f.write(f"- Lignes conservées : {len(df_reduced):,}\n")
    f.write(f"- Période : {df_reduced['Year'].min()} - {df_reduced['Year'].max()}\n")

print(f"Justification sauvegardée : {OUTPUT_DIR / 'step2_justification.txt'}")
print("\n" + "="*70)
print("RÉDUCTION DES DONNÉES TERMINÉE AVEC SUCCÈS")
print("="*70)
