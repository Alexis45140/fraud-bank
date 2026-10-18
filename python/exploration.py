from pathlib import Path
import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
FICHIER = RACINE / "data" / "raw" / "Synthetic_Financial_datasets_log.csv"

df = pd.read_csv(FICHIER)

# 1. Vue d'ensemble
print("Lignes, colonnes :", df.shape)
print(df.dtypes)
print(df.head())

# 2. Combien de fraudes ?
print("\nNombre de fraudes :", df["isFraud"].sum())
print("Taux de fraude :", round(df["isFraud"].mean() * 100, 3), "%")

# 3. Où se trouve la fraude, par type de transaction ?
par_type = df.groupby("type")["isFraud"].agg(
    nb_transactions="size",
    nb_fraudes="sum",
    taux_fraude="mean",
)
print("\n", par_type)

# 4. Que vaut la règle actuelle de la banque ?
print("\nRègle actuelle (isFlaggedFraud) contre fraudes réelles (isFraud) :")
print(pd.crosstab(df["isFlaggedFraud"], df["isFraud"]))