import pandas as pd
from sqlalchemy import create_engine
import os

# ------------------------------------
# Project Paths
# ------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")
DATABASE_PATH = os.path.join(BASE_DIR, "database", "vaccination.db")

# Create database folder
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# ------------------------------------
# SQLite Connection
# ------------------------------------
engine = create_engine(f"sqlite:///{DATABASE_PATH}")

print("Connected to SQLite Database")

# ------------------------------------
# Cleaned CSV Files
# ------------------------------------
files = {
    "coverage": "coverage_cleaned.csv",
    "incidence": "incidence_cleaned.csv",
    "cases": "cases_cleaned.csv",
    "intro": "intro_cleaned.csv",
    "schedule": "schedule_cleaned.csv"
}

# ------------------------------------
# Load Data into SQLite
# ------------------------------------
for table_name, file_name in files.items():

    csv_path = os.path.join(PROCESSED_PATH, file_name)

    print(f"\nLoading {table_name}...")

    df = pd.read_csv(csv_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"SUCCESS: {table_name} table created ({len(df)} rows)")

print("\nAll tables created successfully!")
print(f"Database saved at:\n{DATABASE_PATH}")