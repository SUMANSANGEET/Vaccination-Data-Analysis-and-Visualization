import pandas as pd
from sqlalchemy import create_engine
import os

# ---------------------------------
# Database Connection
# ---------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "database", "vaccination.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

print("Connected Successfully")

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    engine
)

print(tables)

for table in ["coverage", "incidence", "cases", "intro", "schedule"]:

    query = f"SELECT COUNT(*) AS Total_Rows FROM {table}"

    df = pd.read_sql(query, engine)

    print("\n", table.upper())

    print(df)

for table in ["coverage", "incidence", "cases"]:

    print("\n")

    print(table.upper())

    query = f"SELECT * FROM {table} LIMIT 5"

    print(pd.read_sql(query, engine))

for table in ["coverage", "incidence", "cases", "intro", "schedule"]:

    print("\n", "="*50)

    print(table.upper())

    query = f"PRAGMA table_info({table});"

    print(pd.read_sql(query, engine))

query = """
SELECT
    country,
    COUNT(*) AS Total_Records
FROM coverage
GROUP BY country
ORDER BY Total_Records DESC
LIMIT 20;
"""

print(pd.read_sql(query, engine))

query = """
SELECT
    year,
    COUNT(*) AS Records
FROM coverage
GROUP BY year
ORDER BY year;
"""

print(pd.read_sql(query, engine))

query = """
SELECT *
FROM coverage
WHERE year IS NULL;
"""

print(pd.read_sql(query, engine))

query = """
SELECT
    country,
    AVG(coverage) AS Avg_Coverage
FROM coverage
GROUP BY country
ORDER BY Avg_Coverage DESC
LIMIT 10;
"""

print(pd.read_sql(query, engine))

query = """
SELECT *
FROM coverage
LIMIT 100;
"""

df = pd.read_sql(query, engine)

output = os.path.join(BASE_DIR, "reports")

os.makedirs(output, exist_ok=True)

df.to_csv(
    os.path.join(output, "coverage_sample.csv"),
    index=False
)

print("Report Saved")