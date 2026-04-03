import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(BASE_DIR, "../data/raw/processed_bp_snapshot.csv"))

def assign_label(row):
    sbp, dbp, hr = row["SBP"], row["DBP"], row["HR"]
    if sbp >= 180 or dbp >= 120 or hr > 150:
        return "Emergency"
    elif sbp >= 160 or dbp >= 100 or hr >= 130:
        return "Warning"
    elif sbp >= 140 or dbp >= 90 or hr >= 110:
        return "Alert"
    else:
        return "Normal"

df["bp_label"] = df.apply(assign_label, axis=1)
df.to_csv(os.path.join(BASE_DIR, "../data/raw/processed_bp_snapshot.csv"), index=False)
print("Preprocessing done")
