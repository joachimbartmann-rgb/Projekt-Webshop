from pathlib import Path
import pandas as pd

project_root = Path(__file__).parent.parent

excel_file = (
    project_root /
    "Postkarten_Datenbank_Inventar.xlsx"
)

df = pd.read_excel(
    excel_file,
    sheet_name="Postkarten"
)

# Leere Spalten entfernen
df = df.dropna(
    axis=1,
    how="all"
)

print()
print("Verbleibende Spalten:")
print()

for col in df.columns:
    print(col)

print()
print("=" * 60)
print(df.head())