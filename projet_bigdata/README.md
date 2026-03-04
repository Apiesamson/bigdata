# Big Data – Projet d’intégration : Analyse de données climatiques

## Objectif

Ce dépôt contient un projet d’intégration (Master 2 – Big Data) réalisé en Python à partir du fichier **`GlobalLandTemperaturesByMajorCity.csv`**.

Le but est de démontrer la capacité à :

- **Manipuler un volume de données conséquent**
- **Structurer un pipeline de préparation** (réduction, nettoyage, feature engineering)
- **Produire une analyse exploitable** (variable cible + règles d’un arbre de décision)

## Données

- **Source** : `projet_bigdata/GlobalLandTemperaturesByMajorCity.csv`
- **Contenu** : mesures mensuelles de température, grandes villes, longue période historique, valeurs manquantes.

## Résultats (synthèse)

- **Volume initial** : 239 177 lignes
- **Réduction** : filtrage temporel (≥ 1950) + suppression des NA sur `AverageTemperature`
- **Volume final** : 76 407 lignes
- **Cible** : `temperature_class` (3 classes)
  - Basse : ≤ 16.95°C
  - Moyenne : (16.95°C, 25.04°C]
  - Élevée : > 25.04°C
- **Jeu final Sipina** : `dataset_final_sipina.csv` (0 valeur manquante)

## Structure du dépôt

```
.
├── README.md
└── projet_bigdata
    ├── GlobalLandTemperaturesByMajorCity.csv
    ├── dataset_reduced.csv
    ├── dataset_with_target.csv
    ├── dataset_final_sipina.csv
    ├── outputs/                         # graphiques + fichiers .txt générés
    ├── step1_analysis.py
    ├── step2_reduction.py
    ├── step3_target_creation.py
    ├── step4_prepare_sipina.py
    ├── step5_analysis_sipina.py
    ├── main.py
    ├── rapport_latex.tex
    ├── rapport_latex_compact.tex
    ├── compile_rapport.bat
    ├── compile_rapport_compact.bat
    ├── requirements.txt
    └── .gitignore
```

## Prérequis

- Python 3.9+
- Dépendances Python : voir `projet_bigdata/requirements.txt`


## Installation

Depuis la racine du dépôt :

```bash
python -m venv venv
# Windows
venv\Scripts\activate

pip install -r projet_bigdata/requirements.txt
```

## Exécution du pipeline (recommandé)

Le pipeline complet (steps optimisées, génération des outputs) :

```bash
python projet_bigdata/main.py
```

Les artefacts sont produits dans :

- `projet_bigdata/outputs/` (images + fichiers `.txt`)
- `projet_bigdata/dataset_*.csv`


## Utilisation dans Sipina (Étape 5)

Importer :

- `projet_bigdata/dataset_final_sipina.csv`

Configurer :

- Variable cible : `temperature_class`
- Variables explicatives : `City`, `Country`, `Latitude`, `Longitude`, `Year`, `Month`

## Notes

- Le dossier `projet_bigdata/outputs/` est volontairement **ignoré** par git (voir `.gitignore`) car il contient des artefacts générés.
- Si vous souhaitez versionner les figures du rapport, retirez `outputs/*.png` du `.gitignore`.
