import pandas as pd

df = pd.read_excel(
    "Postkarten_Datenbank_Inventar.xlsx",
    sheet_name="Postkarten"
)

for col in df.columns:
    print(col)
