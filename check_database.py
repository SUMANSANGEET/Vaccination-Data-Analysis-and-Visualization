import sqlite3
import pandas as pd

conn = sqlite3.connect("database/vaccination.db")

# Show tables
tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)
print("\n=== TABLES ===")
print(tables)

# Show columns of coverage table
schema = pd.read_sql("PRAGMA table_info(coverage);", conn)
print("\n=== COVERAGE SCHEMA ===")
print(schema)

# Show sample data
df = pd.read_sql("SELECT * FROM coverage LIMIT 5;", conn)
print("\n=== COLUMNS ===")
print(df.columns.tolist())

print("\n=== FIRST 5 ROWS ===")
print(df)

conn.close()