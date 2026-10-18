from pathlib import Path
import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
df = pd.read_csv(RACINE / "data" / "raw" / "Synthetic_Financial_datasets_log.csv")

TOTAL_FRAUDES = df["isFraud"].sum()


def evaluer(nom, alerte):
    """Compare les alertes d'une règle aux fraudes réelles."""
    nb_alertes = int(alerte.sum())
    fraudes_detectees = int((alerte & (df["isFraud"] == 1)).sum())
    return {
        "regle": nom,
        "nb_alertes": nb_alertes,
        "fraudes_detectees": fraudes_detectees,
        "fausses_alertes": nb_alertes - fraudes_detectees,
        "taux_detection": fraudes_detectees / TOTAL_FRAUDES,
        "precision": fraudes_detectees / nb_alertes if nb_alertes else 0,
    }


# Les signaux élémentaires
type_risque = df["type"].isin(["TRANSFER", "CASH_OUT"])

compte_vide = (
    (df["oldbalanceOrg"] > 0)
    & (df["newbalanceOrig"] == 0)
    & (df["amount"] >= df["oldbalanceOrg"])
)

destinataire_incoherent = (
    (df["oldbalanceDest"] == 0)
    & (df["newbalanceDest"] == 0)
    & (df["amount"] > 0)
)

gros_montant = df["amount"] > 200_000

# Les règles
regles = {
    "R0 Règle actuelle": df["isFlaggedFraud"] == 1,
    "R1 Type à risque": type_risque,
    "R2 Compte vidé": type_risque & compte_vide,
    "R3 Destinataire incohérent": type_risque & destinataire_incoherent,
    "R4 Montant > 200 000": type_risque & gros_montant,
    "R5 Compte vidé ou destinataire incohérent": type_risque
    & (compte_vide | destinataire_incoherent),
}

regles["R6 Destinataire incohérent ou virement qui vide le compte"] = (
    type_risque & destinataire_incoherent
) | ((df["type"] == "TRANSFER") & compte_vide)

vide_exactement = (df["amount"] == df["oldbalanceOrg"]) & (df["amount"] > 0)

regles["R7 Destinataire incohérent ou retrait qui vide exactement le compte"] = (
    type_risque & destinataire_incoherent
) | ((df["type"] == "CASH_OUT") & vide_exactement)

resultats = pd.DataFrame([evaluer(nom, alerte) for nom, alerte in regles.items()])

pd.set_option("display.width", 200)
pd.set_option("display.float_format", "{:.3f}".format)
print(resultats)

(RACINE / "outputs").mkdir(exist_ok=True)
resultats.to_csv(RACINE / "outputs" / "python_evaluation_regles.csv", index=False)

# --- Analyse des fraudes manquées par R3 ---
r3 = type_risque & destinataire_incoherent
manquees = df[(df["isFraud"] == 1) & ~r3]
honnetes_cash_out = df[(df["isFraud"] == 0) & (df["type"] == "CASH_OUT")]

print("\nFraudes manquées par R3 :", len(manquees))
print(manquees["type"].value_counts())

colonnes = ["amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]

print("\nFraudes manquées (CASH_OUT) :")
print(manquees[manquees["type"] == "CASH_OUT"][colonnes].describe())

print("\nCASH_OUT honnêtes :")
print(honnetes_cash_out[colonnes].describe())

# Part des transactions qui vident exactement le compte émetteur
vide_exact = lambda d: (d["amount"] == d["oldbalanceOrg"]).mean()
print("\nVident exactement le compte :")
print("  fraudes manquées :", round(vide_exact(manquees) * 100, 1), "%")
print("  CASH_OUT honnêtes :", round(vide_exact(honnetes_cash_out) * 100, 1), "%")