from pathlib import Path
import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
df = pd.read_csv(RACINE / "data" / "raw" / "Synthetic_Financial_datasets_log.csv")
knime = pd.read_csv(RACINE / "outputs" / "knime_alertes_R7.csv")

# 1. Recalculer R7 en Python, avec exactement les mêmes conditions
type_risque = df["type"].isin(["TRANSFER", "CASH_OUT"])
destinataire_incoherent = (
    (df["oldbalanceDest"] == 0) & (df["newbalanceDest"] == 0) & (df["amount"] > 0)
)
vide_exactement = (df["amount"] == df["oldbalanceOrg"]) & (df["amount"] > 0)
r7 = (type_risque & destinataire_incoherent) | (
    (df["type"] == "CASH_OUT") & vide_exactement
)
python = df[r7].copy()

# 2. Comparer les totaux
print("Alertes  - Python :", len(python), "| KNIME :", len(knime))
print("Fraudes  - Python :", python["isFraud"].sum(), "| KNIME :", knime["isFraud"].sum())

# 3. Comparer transaction par transaction
cle = ["step", "nameOrig", "nameDest", "amount"]
for table in (python, knime):
    table["amount"] = table["amount"].round(2)

print("\nDoublons de clé - Python :", python.duplicated(cle).sum(),
      "| KNIME :", knime.duplicated(cle).sum())

comparaison = python[cle].merge(knime[cle], on=cle, how="outer", indicator=True)
print("\nRésultat de la comparaison :")
print(comparaison["_merge"].value_counts())