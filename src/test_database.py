from sqlalchemy import create_engine
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = os.path.join(BASE_DIR, "database", "vaccination.db")

engine = create_engine(f"sqlite:///{DATABASE_PATH}")

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    engine
)

print(tables)

coverage = pd.read_sql("SELECT * FROM coverage LIMIT 5;", engine)

print(coverage)