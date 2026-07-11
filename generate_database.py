import pandas as pd
import sqlite3
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "vaccination.db"
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(exist_ok=True)

# 1. Load Coverage Data
# (Assuming columns: Country, Year, Vaccine, Coverage)
df_coverage = pd.read_excel(RAW_DIR / "coverage-data.xlsx") 

# Convert column names to lowercase
df_coverage.columns = df_coverage.columns.str.strip().str.lower()

# 2. Load Incidence Data 
# (Assuming columns: Country, Year, Disease/Vaccine, Incidence Cases/Rate)
df_incidence = pd.read_excel(RAW_DIR / "incidence-rate-data.xlsx")

# Convert column names to lowercase
df_incidence.columns = df_incidence.columns.str.strip().str.lower()

# Normalize columns for merging (e.g., lowering case, standardizing country names)
# ... standard cleaning steps ...

# 3. Merge the datasets on common keys
# Usually merged on Country, Year, and matching the Vaccine to its target Disease

print("=" * 60)
print("Coverage Columns")
print("=" * 60)
print(df_coverage.columns.tolist())

print("\n")

print("=" * 60)
print("Incidence Columns")
print("=" * 60)
print(df_incidence.columns.tolist())

# Stop here
exit()
# Fill missing incidence rates with 0 or NaN if necessary
df_combined["incidence_rate"] = df_combined["incidence_rate"].fillna(0)

# 4. Write to SQLite
conn = sqlite3.connect(DB_PATH)
df_combined.to_sql("coverage", conn, if_exists="replace", index=False)
conn.close()
print("Coverage columns:", df_coverage.columns.tolist())
print("Incidence columns:", df_incidence.columns.tolist())
print("Combined columns:", df_combined.columns.tolist())
print("Database rebuilt successfully with incidence_rate column!")