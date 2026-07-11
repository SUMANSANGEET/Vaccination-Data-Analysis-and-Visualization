import sqlite3
import os

# Get project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database path
DB_PATH = os.path.join(BASE_DIR, "database", "vaccination.db")

print("Database Path:")
print(DB_PATH)

# Connect
conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

# Show all tables
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

tables = cursor.fetchall()

print("\nTables Found:")

for table in tables:
    print(table[0])

conn.close()