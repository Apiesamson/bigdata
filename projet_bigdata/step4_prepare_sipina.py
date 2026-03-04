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
print("ÉTAPE 4 - PRÉPARATION DES DONNÉES POUR SIPINA")
print("="*70)

print("\n1. CHARGEMENT DU DATASET AVEC VARIABLE CIBLE")
print("-"*70)
df = pd.read_csv("dataset_with_target.csv")
print(f"Dimensions : {df.shape[0]:,} lignes × {df.shape[1]} colonnes")
print(f"Colonnes : {list(df.columns)}")

print("\n2. CONVERSION ET EXTRACTION DES VARIABLES TEMPORELLES")
print("-"*70)
df['dt'] = pd.to_datetime(df['dt'])
df['Year'] = df['dt'].dt.year
df['Month'] = df['dt'].dt.month
print(f"Période : {df['Year'].min()} - {df['Year'].max()}")
print(f"Mois : {df['Month'].min()} - {df['Month'].max()}")

print("\n3. SÉLECTION DES VARIABLES POUR SIPINA")
print("-"*70)
variables_to_keep = ['City', 'Country', 'Latitude', 'Longitude', 'Year', 'Month', 'temperature_class']
df_final = df[variables_to_keep].copy()

print("Variables explicatives :")
for var in variables_to_keep[:-1]:
    print(f"  - {var:15s} : {df_final[var].dtype}")
print(f"\nVariable cible :")
print(f"  - temperature_class : {df_final['temperature_class'].dtype}")

print("\n4. VÉRIFICATION DES VALEURS MANQUANTES")
print("-"*70)
missing = df_final.isnull().sum()
print(missing)
if missing.sum() == 0:
    print("✓ Aucune valeur manquante détectée")
else:
    print("⚠ Attention : Valeurs manquantes détectées")

print("\n5. STATISTIQUES DESCRIPTIVES DES VARIABLES NUMÉRIQUES")
print("-"*70)
print(df_final[['Year', 'Month']].describe())

print("\n6. CARDINALITÉ DES VARIABLES CATÉGORIELLES")
print("-"*70)
print(f"Nombre de villes uniques    : {df_final['City'].nunique()}")
print(f"Nombre de pays uniques      : {df_final['Country'].nunique()}")
print(f"Nombre de classes de temp.  : {df_final['temperature_class'].nunique()}")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

top_cities = df_final['City'].value_counts().head(15)
axes[0, 0].barh(range(len(top_cities)), top_cities.values, color='steelblue', edgecolor='black')
axes[0, 0].set_yticks(range(len(top_cities)))
axes[0, 0].set_yticklabels(top_cities.index, fontsize=9)
axes[0, 0].set_xlabel('Nombre d\'observations')
axes[0, 0].set_title('Top 15 des villes', fontweight='bold')
axes[0, 0].grid(axis='x', alpha=0.3)

top_countries = df_final['Country'].value_counts().head(15)
axes[0, 1].barh(range(len(top_countries)), top_countries.values, color='coral', edgecolor='black')
axes[0, 1].set_yticks(range(len(top_countries)))
axes[0, 1].set_yticklabels(top_countries.index, fontsize=9)
axes[0, 1].set_xlabel('Nombre d\'observations')
axes[0, 1].set_title('Top 15 des pays', fontweight='bold')
axes[0, 1].grid(axis='x', alpha=0.3)

class_counts = df_final['temperature_class'].value_counts()
colors_map = {'Basse': '#3498db', 'Moyenne': '#f39c12', 'Élevée': '#e74c3c'}
colors = [colors_map[c] for c in class_counts.index]
axes[0, 2].bar(class_counts.index, class_counts.values, color=colors, edgecolor='black', linewidth=2)
axes[0, 2].set_ylabel('Nombre d\'observations')
axes[0, 2].set_title('Distribution de la variable cible', fontweight='bold')
axes[0, 2].grid(axis='y', alpha=0.3)
for i, v in enumerate(class_counts.values):
    axes[0, 2].text(i, v + 500, f'{v:,}', ha='center', va='bottom', fontweight='bold')

yearly_counts = df_final['Year'].value_counts().sort_index()
axes[1, 0].plot(yearly_counts.index, yearly_counts.values, color='green', linewidth=2, marker='o', markersize=3)
axes[1, 0].set_xlabel('Année')
axes[1, 0].set_ylabel('Nombre d\'observations')
axes[1, 0].set_title('Distribution par année', fontweight='bold')
axes[1, 0].grid(alpha=0.3)

monthly_counts = df_final['Month'].value_counts().sort_index()
month_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
axes[1, 1].bar(monthly_counts.index, monthly_counts.values, color='purple', alpha=0.7, edgecolor='black')
axes[1, 1].set_xlabel('Mois')
axes[1, 1].set_ylabel('Nombre d\'observations')
axes[1, 1].set_title('Distribution par mois', fontweight='bold')
axes[1, 1].set_xticks(range(1, 13))
axes[1, 1].set_xticklabels(month_labels, rotation=45)
axes[1, 1].grid(axis='y', alpha=0.3)

variables_info = pd.DataFrame({
    'Variable': variables_to_keep,
    'Type': [str(df_final[v].dtype) for v in variables_to_keep],
    'Cardinalité': [df_final[v].nunique() for v in variables_to_keep],
    'Valeurs manquantes': [df_final[v].isnull().sum() for v in variables_to_keep]
})
axes[1, 2].axis('off')
table = axes[1, 2].table(cellText=variables_info.values, 
                         colLabels=variables_info.columns,
                         cellLoc='left', loc='center',
                         colWidths=[0.25, 0.2, 0.2, 0.25])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)
for i in range(len(variables_info.columns)):
    table[(0, i)].set_facecolor('#40466e')
    table[(0, i)].set_text_props(weight='bold', color='white')
axes[1, 2].set_title('Résumé des variables', fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "step4_sipina_preparation.png", dpi=300, bbox_inches='tight')
print(f"\nVisualisations sauvegardées : {OUTPUT_DIR / 'step4_sipina_preparation.png'}")

df_final.to_csv("dataset_final_sipina.csv", index=False)
print(f"Dataset final sauvegardé : dataset_final_sipina.csv")

with open(OUTPUT_DIR / "step4_variables_description.txt", 'w', encoding='utf-8') as f:
    f.write("DESCRIPTION DES VARIABLES POUR SIPINA\n")
    f.write("="*50 + "\n\n")
    f.write("VARIABLES EXPLICATIVES :\n")
    f.write("-"*50 + "\n")
    f.write(f"1. City      : Nom de la ville ({df_final['City'].nunique()} valeurs uniques)\n")
    f.write(f"2. Country   : Pays ({df_final['Country'].nunique()} valeurs uniques)\n")
    f.write(f"3. Latitude  : Position géographique Nord-Sud (format texte)\n")
    f.write(f"4. Longitude : Position géographique Est-Ouest (format texte)\n")
    f.write(f"5. Year      : Année de mesure ({df_final['Year'].min()}-{df_final['Year'].max()})\n")
    f.write(f"6. Month     : Mois de mesure (1-12)\n\n")
    f.write("VARIABLE CIBLE :\n")
    f.write("-"*50 + "\n")
    f.write("temperature_class : Classe de température (Basse/Moyenne/Élevée)\n\n")
    f.write("TRANSFORMATIONS APPLIQUÉES :\n")
    f.write("-"*50 + "\n")
    f.write("- Extraction de Year et Month à partir de la date\n")
    f.write("- Suppression de la colonne 'dt' (date originale)\n")
    f.write("- Suppression de 'AverageTemperature' (éviter data leakage)\n")
    f.write("- Suppression de 'AverageTemperatureUncertainty' (non pertinent)\n\n")
    f.write("QUALITÉ DES DONNÉES :\n")
    f.write("-"*50 + "\n")
    f.write(f"- Nombre total d'observations : {len(df_final):,}\n")
    f.write(f"- Valeurs manquantes : {df_final.isnull().sum().sum()}\n")
    f.write(f"- Fichier prêt pour Sipina : dataset_final_sipina.csv\n")

print(f"Description sauvegardée : {OUTPUT_DIR / 'step4_variables_description.txt'}")
print("\n" + "="*70)
print("PRÉPARATION POUR SIPINA TERMINÉE AVEC SUCCÈS")
print("="*70)
