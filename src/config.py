from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"

print("Project:", BASE_DIR)
print("Raw Data:", RAW_DATA)