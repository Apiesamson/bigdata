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
print("ÉTAPE 3 - CRÉATION DE LA VARIABLE CIBLE")
print("="*70)

print("\n1. CHARGEMENT DU DATASET RÉDUIT")
print("-"*70)
df = pd.read_csv("dataset_reduced.csv")
print(f"Dimensions : {df.shape[0]:,} lignes × {df.shape[1]} colonnes")

print("\n2. CALCUL DES QUANTILES")
print("-"*70)
q33 = df['AverageTemperature'].quantile(0.33)
q66 = df['AverageTemperature'].quantile(0.66)
print(f"Quantile 33% : {q33:.2f}°C")
print(f"Quantile 66% : {q66:.2f}°C")

print("\n3. CRÉATION DE LA VARIABLE CIBLE")
print("-"*70)

def classify_temperature(temp, q1, q2):
    """Classifie la température en 3 catégories"""
    if temp <= q1:
        return "Basse"
    elif temp <= q2:
        return "Moyenne"
    else:
        return "Élevée"

df['temperature_class'] = df['AverageTemperature'].apply(
    lambda x: classify_temperature(x, q33, q66)
)

print("\n4. RÉPARTITION DES CLASSES")
print("-"*70)
class_counts = df['temperature_class'].value_counts()
class_proportions = df['temperature_class'].value_counts(normalize=True) * 100

class_summary = pd.DataFrame({
    'Nombre': class_counts,
    'Pourcentage': class_proportions
})
print(class_summary)

print("\n5. STATISTIQUES PAR CLASSE")
print("-"*70)
stats_by_class = df.groupby('temperature_class')['AverageTemperature'].agg([
    ('Minimum', 'min'),
    ('Maximum', 'max'),
    ('Moyenne', 'mean'),
    ('Écart-type', 'std')
])
print(stats_by_class)

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

class_order = ['Basse', 'Moyenne', 'Élevée']
colors_map = {'Basse': '#3498db', 'Moyenne': '#f39c12', 'Élevée': '#e74c3c'}
counts = [class_counts[c] for c in class_order]
colors = [colors_map[c] for c in class_order]

axes[0, 0].bar(class_order, counts, color=colors, edgecolor='black', linewidth=2)
axes[0, 0].set_ylabel('Nombre d\'observations')
axes[0, 0].set_title('Répartition des classes de température', fontweight='bold')
axes[0, 0].grid(axis='y', alpha=0.3)
for i, v in enumerate(counts):
    axes[0, 0].text(i, v + 500, f'{v:,}\n({class_proportions[class_order[i]]:.1f}%)', 
                    ha='center', va='bottom', fontweight='bold')

axes[0, 1].pie(counts, labels=class_order, colors=colors, autopct='%1.1f%%', 
               shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
axes[0, 1].set_title('Proportion des classes', fontweight='bold')

for i, temp_class in enumerate(class_order):
    data = df[df['temperature_class'] == temp_class]['AverageTemperature']
    axes[0, 2].hist(data, bins=30, alpha=0.6, label=temp_class, 
                    color=colors_map[temp_class], edgecolor='black')
axes[0, 2].axvline(q33, color='green', linestyle='--', linewidth=2, label=f'Q33 ({q33:.1f}°C)')
axes[0, 2].axvline(q66, color='red', linestyle='--', linewidth=2, label=f'Q66 ({q66:.1f}°C)')
axes[0, 2].set_xlabel('Température (°C)')
axes[0, 2].set_ylabel('Fréquence')
axes[0, 2].set_title('Distribution des températures par classe', fontweight='bold')
axes[0, 2].legend()
axes[0, 2].grid(axis='y', alpha=0.3)

bp = axes[1, 0].boxplot([df[df['temperature_class'] == c]['AverageTemperature'] for c in class_order],
                        labels=class_order, patch_artist=True, showmeans=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[1, 0].set_ylabel('Température (°C)')
axes[1, 0].set_title('Distribution des températures (Boxplot)', fontweight='bold')
axes[1, 0].grid(axis='y', alpha=0.3)

df['dt'] = pd.to_datetime(df['dt'])
df['Year'] = df['dt'].dt.year
yearly_class = df.groupby(['Year', 'temperature_class']).size().unstack(fill_value=0)
yearly_class_pct = yearly_class.div(yearly_class.sum(axis=1), axis=0) * 100

axes[1, 1].plot(yearly_class_pct.index, yearly_class_pct['Basse'], 
                label='Basse', color=colors_map['Basse'], linewidth=2)
axes[1, 1].plot(yearly_class_pct.index, yearly_class_pct['Moyenne'], 
                label='Moyenne', color=colors_map['Moyenne'], linewidth=2)
axes[1, 1].plot(yearly_class_pct.index, yearly_class_pct['Élevée'], 
                label='Élevée', color=colors_map['Élevée'], linewidth=2)
axes[1, 1].set_xlabel('Année')
axes[1, 1].set_ylabel('Pourcentage (%)')
axes[1, 1].set_title('Évolution temporelle des classes', fontweight='bold')
axes[1, 1].legend()
axes[1, 1].grid(alpha=0.3)

df['Month'] = df['dt'].dt.month
monthly_class = df.groupby(['Month', 'temperature_class']).size().unstack(fill_value=0)
monthly_class.plot(kind='bar', stacked=True, ax=axes[1, 2], 
                   color=[colors_map[c] for c in class_order], edgecolor='black')
axes[1, 2].set_xlabel('Mois')
axes[1, 2].set_ylabel('Nombre d\'observations')
axes[1, 2].set_title('Distribution mensuelle des classes', fontweight='bold')
axes[1, 2].legend(title='Classe')
axes[1, 2].grid(axis='y', alpha=0.3)
axes[1, 2].set_xticklabels(['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
                            'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'], rotation=45)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "step3_target_creation.png", dpi=300, bbox_inches='tight')
print(f"\nVisualisations sauvegardées : {OUTPUT_DIR / 'step3_target_creation.png'}")

df.to_csv("dataset_with_target.csv", index=False)
print(f"Dataset avec variable cible sauvegardé : dataset_with_target.csv")

with open(OUTPUT_DIR / "step3_target_description.txt", 'w', encoding='utf-8') as f:
    f.write("DESCRIPTION DE LA VARIABLE CIBLE\n")
    f.write("="*50 + "\n\n")
    f.write("Variable créée : temperature_class\n\n")
    f.write("Méthode : Classification par quantiles (33% et 66%)\n\n")
    f.write("Seuils calculés :\n")
    f.write(f"- Quantile 33% : {q33:.2f}°C\n")
    f.write(f"- Quantile 66% : {q66:.2f}°C\n\n")
    f.write("Classes définies :\n")
    f.write(f"1. Basse   : Température ≤ {q33:.2f}°C\n")
    f.write(f"2. Moyenne : {q33:.2f}°C < Température ≤ {q66:.2f}°C\n")
    f.write(f"3. Élevée  : Température > {q66:.2f}°C\n\n")
    f.write("Répartition :\n")
    for cls in class_order:
        f.write(f"- {cls:8s} : {class_counts[cls]:6,} observations ({class_proportions[cls]:5.2f}%)\n")
    f.write("\nJustification :\n")
    f.write("L'utilisation des quantiles garantit un équilibrage parfait des classes,\n")
    f.write("évitant ainsi les biais lors de l'apprentissage automatique.\n")

print(f"Description sauvegardée : {OUTPUT_DIR / 'step3_target_description.txt'}")
print("\n" + "="*70)
print("CRÉATION DE LA VARIABLE CIBLE TERMINÉE AVEC SUCCÈS")
print("="*70)
