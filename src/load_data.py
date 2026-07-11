import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW = BASE_DIR / "data" / "raw"

files = {
    "coverage": "coverage-data.xlsx",
    "incidence": "incidence-rate-data.xlsx",
    "cases": "reported-cases-data.xlsx",
    "intro": "vaccine-introduction-data.xlsx",
    "schedule": "vaccine-schedule-data.xlsx",
}

dfs = {}

for name, file in files.items():
    path = RAW / file
    df = pd.read_excel(path)
    dfs[name] = df

    print(f"\n{name.upper()}")
    print(df.head())
    print(df.shape)