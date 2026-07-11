import pandas as pd
from pathlib import Path

# -------------------------------
# Folder Paths
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_PATH = BASE_DIR / "data" / "raw"
PROCESSED_PATH = BASE_DIR / "data" / "processed"

# Create processed folder if it doesn't exist
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

# -------------------------------
# Dataset Files
# -------------------------------
files = {
    "coverage": "coverage-data.xlsx",
    "incidence": "incidence-rate-data.xlsx",
    "cases": "reported-cases-data.xlsx",
    "intro": "vaccine-introduction-data.xlsx",
    "schedule": "vaccine-schedule-data.xlsx",
}

# -------------------------------
# Clean Each Dataset
# -------------------------------
for name, file in files.items():

    print(f"\nProcessing {file}...")

    # Read Excel file
    df = pd.read_excel(RAW_PATH / file)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Handle missing values
    # Fill numeric columns with 0
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Fill text columns with "Unknown"
    object_cols = df.select_dtypes(include="object").columns
    df[object_cols] = df[object_cols].fillna("Unknown")

    # Convert year column to integer if it exists
    if "year" in df.columns:
        df["year"] = (
            pd.to_numeric(df["year"], errors="coerce")
            .fillna(0)
            .astype(int)
        )

    # Save cleaned file
    output_file = PROCESSED_PATH / f"{name}_cleaned.csv"
    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\nAll datasets cleaned successfully!")