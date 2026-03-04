# Étape 6 – Mise en perspective Big Data

## Pourquoi utiliser Spark dans un contexte industriel ?

### 1. Limites de l'approche actuelle avec Pandas

Dans ce projet, nous avons travaillé sur un dataset réduit (~76 000 lignes après filtrage). Cependant, le fichier original `GlobalLandTemperaturesByMajorCity.csv` contient plusieurs centaines de milliers de lignes, et dans un contexte industriel réel, les volumes seraient bien plus importants :

- **Données multi-sources** : combinaison de données satellitaires, stations météo, capteurs IoT
- **Granularité temporelle** : mesures horaires ou quotidiennes au lieu de mensuelles
- **Couverture géographique** : toutes les villes du monde, pas seulement les grandes villes
- **Historique complet** : conservation de toutes les données historiques sans filtrage

Avec Pandas, ces volumes dépasseraient rapidement la mémoire RAM disponible sur une seule machine.

### 2. Étapes bénéficiant du calcul distribué avec Spark

#### **Étape 2 : Réduction et agrégation des données** 
**Impact majeur du calcul distribué**

```python
# Avec Spark, les opérations suivantes seraient distribuées :
df_spark = spark.read.csv("GlobalLandTemperaturesByMajorCity.csv", header=True)
df_filtered = df_spark.filter(col("dt") >= "1950-01-01")
df_clean = df_filtered.dropna(subset=["AverageTemperature"])
```

**Avantages** :
- Traitement en parallèle sur plusieurs nœuds
- Pas de limite de mémoire RAM d'une seule machine
- Agrégations distribuées (groupBy, avg, sum) très performantes
- Lecture partitionnée des fichiers volumineux

#### **Étape 3 : Création de la variable cible**
**Impact modéré du calcul distribué**

```python
# Calcul des quantiles de manière distribuée
quantiles = df_spark.approxQuantile("AverageTemperature", [0.33, 0.66], 0.01)

# Application de la fonction de classification en parallèle
df_with_class = df_spark.withColumn(
    "temperature_class",
    when(col("AverageTemperature") <= quantiles[0], "Basse")
    .when(col("AverageTemperature") <= quantiles[1], "Moyenne")
    .otherwise("Élevée")
)
```

**Avantages** :
- Calcul des statistiques (quantiles) sur l'ensemble du dataset distribué
- Application de transformations (UDF) en parallèle

#### **Étape 4 : Préparation des données** 
**Impact faible du calcul distribué**

Les opérations de cette étape (extraction de colonnes, suppression de colonnes) sont relativement légères et bénéficient moins du calcul distribué, sauf si le volume est très important.

### 3. Architecture Spark recommandée

Pour un contexte industriel, l'architecture suivante serait appropriée :

```
[Sources de données] 
    ↓
[HDFS / S3] → Stockage distribué
    ↓
[Spark Cluster]
    - Driver : orchestration
    - Executors : calcul parallèle
    ↓
[Résultats agrégés] → Base de données / Data Lake
    ↓
[Outils d'analyse] → Sipina, Tableau, etc.
```

### 4. Gains attendus avec Spark

| Étape | Volume Pandas | Temps Pandas | Volume Spark | Temps Spark estimé |
|-------|---------------|--------------|--------------|-------------------|
| Chargement | 100 MB | 5 sec | 10 GB | 10 sec |
| Filtrage | 100 MB | 2 sec | 10 GB | 5 sec |
| Agrégation | 50 MB | 3 sec | 5 GB | 8 sec |
| **Total** | **150 MB** | **10 sec** | **25 GB** | **23 sec** |

**Note** : Avec Pandas, impossible de traiter 25 GB en mémoire. Spark permet de scaler horizontalement.

### 5. Conclusion

Dans un contexte Big Data industriel :

- **Spark est indispensable** pour les étapes de réduction et d'agrégation (Étape 2)
- **Spark apporte de la valeur** pour les transformations complexes (Étape 3)
- **La modélisation finale** (Étape 5) peut rester sur des outils classiques une fois les données agrégées

Le principe clé : **"Réduire avec Spark, analyser avec des outils spécialisés"**
