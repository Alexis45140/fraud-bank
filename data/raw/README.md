# Données brutes

Ce dossier contient le jeu de données PaySim. Il n'est pas versionné : le fichier pèse environ 470 Mo, trop pour GitHub.

## Télécharger le fichier

1. Ouvrir la page Kaggle : https://www.kaggle.com/datasets/sriharshaeedala/financial-fraud-detection-dataset
2. Télécharger le jeu de données (un compte Kaggle est nécessaire).
3. Décompresser l'archive et placer le fichier CSV ici, sous ce nom exact :

```
data/raw/Synthetic_Financial_datasets_log.csv
```

Les scripts du dossier `python/` et le workflow KNIME lisent le fichier à cet emplacement.

## Contrôle rapide

Le fichier attendu contient 6 362 620 transactions et 11 colonnes : `step`, `type`, `amount`, `nameOrig`, `oldbalanceOrg`, `newbalanceOrig`, `nameDest`, `oldbalanceDest`, `newbalanceDest`, `isFraud`, `isFlaggedFraud`.

## Origine et licence

PaySim a été créé par Edgar Lopez-Rojas. La copie utilisée ici est celle publiée sur Kaggle au lien ci-dessus. Vérifier la licence sur la page Kaggle avant toute réutilisation.
