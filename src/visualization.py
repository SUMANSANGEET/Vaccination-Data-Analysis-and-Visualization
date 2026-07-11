import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine

# Connect to SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "database", "vaccination.db")

VIS_PATH = os.path.join(BASE_DIR, "visualizations")

os.makedirs(VIS_PATH, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}")

# Load tables
coverage = pd.read_sql("SELECT * FROM coverage", engine)

incidence = pd.read_sql("SELECT * FROM incidence", engine)

cases = pd.read_sql("SELECT * FROM cases", engine)

intro = pd.read_sql("SELECT * FROM intro", engine)

schedule = pd.read_sql("SELECT * FROM schedule", engine)

# KPI Metrics
print("="*50)
print("KPI METRICS")
print("="*50)

print("Total Records :", len(coverage))

if "country" in coverage.columns:
    print("Countries :", coverage["country"].nunique())

if "year" in coverage.columns:
    print("Years :", coverage["year"].nunique())

if "vaccine" in coverage.columns:
    print("Vaccines :", coverage["vaccine"].nunique())

# Coverage Trend (Line Chart)
trend = (
    coverage
    .groupby("year")["coverage"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(10,5))
plt.plot(trend["year"], trend["coverage"], marker="o")
plt.title("Average Vaccination Coverage Over Time")
plt.xlabel("Year")
plt.ylabel("Coverage")
plt.grid(True)

plt.savefig(os.path.join(VIS_PATH,"line_chart.png"))

plt.show()

# Top 10 Countries
top = (
    coverage
    .groupby("name")["coverage"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))

top.plot(kind="bar")

plt.title("Top Countries by Vaccination Coverage")

plt.savefig(os.path.join(VIS_PATH,"bar_chart.png"))

plt.show()

# Bottom 10 Countries
print("\nCoverage Columns:")
print(coverage.columns.tolist())

print("\nFirst 5 Rows:")
print(coverage.head())
bottom = (
    coverage
    .groupby("name")["coverage"]
    .mean()
    .sort_values()
    .head(10)
)
plt.figure(figsize=(10,6))

bottom.plot(kind="bar")

plt.title("Bottom Countries by Vaccination Coverage")

plt.show()

# Histogram
plt.figure(figsize=(8,5))

coverage["coverage"].hist(bins=25)

plt.title("Coverage Distribution")

plt.savefig(os.path.join(VIS_PATH,"histogram.png"))

plt.show()

# Box Plot
plt.figure(figsize=(6,5))

plt.boxplot(coverage["coverage"])

plt.title("Coverage Boxplot")

plt.savefig(os.path.join(VIS_PATH,"boxplot.png"))

plt.show()

# Scatter Plot
plt.figure(figsize=(8,5))

plt.scatter(
    coverage["year"],
    coverage["coverage"]
)

plt.xlabel("Year")

plt.ylabel("Coverage")

plt.title("Coverage vs Year")

plt.savefig(os.path.join(VIS_PATH,"scatter.png"))

plt.show()

# Correlation Matrix
numeric = coverage.select_dtypes(include="number")

corr = numeric.corr()

plt.figure(figsize=(8,6))

plt.imshow(corr)

plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)

plt.yticks(range(len(corr.columns)), corr.columns)

plt.colorbar()

plt.title("Correlation Matrix")

plt.savefig(os.path.join(VIS_PATH,"correlation_heatmap.png"))

plt.show()

# Disease Incidence Trend
trend = (
    incidence
    .groupby("year")
    .mean(numeric_only=True)
    .reset_index()
)

print(trend.head())

# Line Chart for Disease Incidence
import matplotlib.pyplot as plt

trend = (
    incidence
    .groupby("year")["incidence_rate"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(10,5))

plt.plot(
    trend["year"],
    trend["incidence_rate"],
    marker="o"
)

plt.title("Disease Incidence Trend")

plt.xlabel("Year")

plt.ylabel("Average Incidence Rate")

plt.grid(True)

plt.tight_layout()

plt.savefig(os.path.join(VIS_PATH, "incidence_trend.png"))

plt.show()

trend = (
    incidence
    .groupby("year")["incidence_rate"]
    .mean()
    .reset_index()
)
numeric_cols = incidence.select_dtypes(include="number").columns.tolist()

print("Numeric Columns:", numeric_cols)

metric = numeric_cols[1]

trend = (
    incidence
    .groupby("year")[metric]
    .mean()
    .reset_index()
)

plt.figure(figsize=(10,5))

plt.plot(
    trend["year"],
    trend[metric],
    marker="o"
)

plt.title("Disease Incidence Trend")
plt.xlabel("Year")
plt.ylabel(metric)

plt.grid(True)
plt.show()

# Reported Cases Trend
cases.groupby("year").sum(numeric_only=True)
import matplotlib.pyplot as plt
import os

trend = (
    cases.groupby("year")["cases"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(10,5))

plt.plot(
    trend["year"],
    trend["cases"],
    marker="o"
)

plt.title("Reported Cases by Year")
plt.xlabel("Year")
plt.ylabel("Reported Cases")
plt.grid(True)
plt.tight_layout()

plt.savefig(os.path.join(VIS_PATH, "reported_cases_trend.png"))

plt.show()

print(cases.select_dtypes(include="number").columns.tolist())

metric = "cases"

trend = (
    cases.groupby("year")[metric]
    .sum()
    .reset_index()
)

plt.figure(figsize=(10,5))

plt.plot(
    trend["year"],
    trend[metric],
    marker="o"
)

plt.title("Reported Cases by Year")
plt.xlabel("Year")
plt.ylabel("Reported Cases")
plt.grid(True)
plt.tight_layout()

plt.savefig(os.path.join(VIS_PATH, "reported_cases_trend.png"))

plt.show()

# Vaccine Introduction Timeline
intro.groupby("year").size()

# Line Chart for Vaccine Introduction Timeline
import matplotlib.pyplot as plt
import os

timeline = (
    intro.groupby("year")
    .size()
    .reset_index(name="introductions")
)

plt.figure(figsize=(10,5))

plt.plot(
    timeline["year"],
    timeline["introductions"],
    marker="o"
)

plt.title("Vaccine Introduction Timeline")
plt.xlabel("Year")
plt.ylabel("Number of Vaccine Introductions")
plt.grid(True)
plt.tight_layout()

plt.savefig(os.path.join(VIS_PATH, "vaccine_introduction_timeline.png"))

plt.show()

# Bar Chart for Vaccine Introduction Timeline
timeline = (
    intro.groupby("year")
    .size()
    .reset_index(name="introductions")
)

plt.figure(figsize=(12,6))

plt.bar(
    timeline["year"],
    timeline["introductions"]
)

plt.title("Vaccine Introductions by Year")
plt.xlabel("Year")
plt.ylabel("Number of Introductions")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(os.path.join(VIS_PATH, "vaccine_introduction_bar.png"))

plt.show()

# Choropleth World Map (Interactive)
world = (
    coverage
    .groupby(["code", "name"], as_index=False)["coverage"]
    .mean()
)

fig = px.choropleth(
    world,
    locations="code",
    locationmode="ISO-3",
    color="coverage",
    hover_name="name",
    title="Global Vaccination Coverage",
    color_continuous_scale="Viridis"
)

fig.write_html(
    os.path.join(VIS_PATH, "choropleth.html")
)

fig.show()

