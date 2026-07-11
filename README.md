# 💉 Vaccination Data Analysis and Visualization

> **An End-to-End Data Analytics Project using Python, SQLite, Streamlit, and Power BI to analyze global vaccination coverage, disease incidence, immunization schedules, and vaccination trends.**

LIVE STREAMLIT APP
![Streamlit](https://vaccination-data-analysis-and-visualization-vibxqle853xupnjfto.streamlit.app/)


---

# 📌 Project Overview

Vaccination plays a crucial role in preventing infectious diseases and improving public health worldwide. This project analyzes global vaccination datasets to uncover vaccination trends, disease incidence, immunization coverage, vaccine introductions, and country-wise performance.

The project demonstrates the complete Data Analytics lifecycle:

- Data Collection
- Data Cleaning
- Data Transformation
- SQL Database Creation
- Exploratory Data Analysis (EDA)
- Interactive Streamlit Dashboard
- Interactive Power BI Dashboard
- Business Insights & Recommendations

---

# 🎯 Business Objectives

This project aims to answer questions such as:

- Which countries have the highest vaccination coverage?
- Which vaccines are most widely administered?
- How has vaccination coverage changed over time?
- Which diseases have the highest reported incidence?
- Which countries require vaccination awareness programs?
- What is the relationship between vaccination coverage and disease incidence?

---

# 🗂️ Project Architecture

```
                Raw Datasets
                      │
                      ▼
             Data Cleaning (Python)
                      │
                      ▼
             SQLite Database
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 Streamlit Dashboard         Power BI Dashboard
        ▼                           ▼
 Interactive Insights      Executive Analytics
```

---

# 📁 Project Structure

```
Vaccination-Data-Analysis-and-Visualization
│
├── data
│   ├── raw
│   ├── cleaned
│
├── database
│   └── vaccination.db
│
├── notebooks
│
├── powerbi
│   └── Vaccination Dashboard.pbix
│
├── images
│
├── app.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 📊 Dataset Description

The project uses multiple datasets including:

| Dataset | Description |
|----------|-------------|
| Coverage | Vaccination coverage by country |
| Incidence | Disease incidence statistics |
| Cases | Reported disease cases |
| Vaccine Introduction | Vaccine launch year |
| Immunization Schedule | National immunization schedule |

---

# 🛠️ Technologies Used

### Programming

- Python

### Data Analysis

- Pandas
- NumPy

### Data Visualization

- Plotly
- Matplotlib
- Streamlit
- Power BI

### Database

- SQLite

### IDE

- VS Code

### Version Control

- Git
- GitHub

---

# ⚙️ Features

## 📈 Interactive Dashboard

- Country Selection
- Vaccine Selection
- Year Filter
- KPI Cards
- Dynamic Charts

---

## 📊 Power BI Dashboard

Includes

- Executive Summary
- Vaccination Coverage Analysis
- Disease Incidence Analysis
- Country Comparison
- Vaccine Introduction Timeline
- Drill Through Pages
- Interactive Slicers

---

## 📉 Visualizations

- Vaccination Coverage Trends
- Disease Incidence Trend
- Top Countries by Coverage
- Top Vaccines
- Country Comparison
- Year-wise Growth
- Interactive KPI Cards
- Heatmaps
- Bar Charts
- Line Charts
- Pie Charts

---

# 🧹 Data Cleaning

The following preprocessing steps were performed:

- Removed duplicate records
- Handled missing values
- Standardized country names
- Converted date columns
- Removed invalid entries
- Renamed inconsistent columns
- Optimized data types

---

# 🗄️ Database Design

SQLite database stores all cleaned datasets.

Main tables:

- coverage_cleaned
- incidence_cleaned
- cases_cleaned
- intro_cleaned
- schedule_cleaned

---

# 📊 Key Insights

✔ Countries with consistently high vaccination coverage

✔ Vaccines with maximum global adoption

✔ Regions with lower immunization rates

✔ Disease incidence trends over multiple years

✔ Vaccine introduction timeline across countries

✔ Relationship between vaccination coverage and disease reduction

---

# 📸 Dashboard Preview

> Add screenshots here

```
images/dashboard1.png

images/dashboard2.png

images/dashboard3.png
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/SUMANSANGEET/Vaccination-Data-Analysis-and-Visualization.git
```

Go inside the folder

```bash
cd Vaccination-Data-Analysis-and-Visualization
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Streamlit

```bash
streamlit run app.py
```

---

# 📈 Power BI Dashboard

Open

```
Vaccination Dashboard.pbix
```

in Microsoft Power BI Desktop.

---

# 📊 KPIs

- Total Countries
- Total Vaccines
- Average Vaccination Coverage
- Total Reported Cases
- Disease Incidence
- Vaccine Introduction Count

---

# 💡 Future Improvements

- Machine Learning Prediction
- WHO API Integration
- Live Dashboard
- Cloud Database
- Docker Deployment
- Azure Deployment
- Advanced Forecasting
- Country Recommendation Engine

---

# 📚 Skills Demonstrated

- Data Cleaning
- Data Wrangling
- SQL
- SQLite
- Exploratory Data Analysis
- Dashboard Development
- Power BI
- DAX
- Data Visualization
- Streamlit
- Business Intelligence
- Git & GitHub

---

# 👨‍💻 Author

**P. Suman Sangeet**

PGDM (Big Data Analytics)

GitHub:
https://github.com/SUMANSANGEET



---

# ⭐ If you found this project useful

Please consider giving it a ⭐ on GitHub!

---

# 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- World Health Organization (WHO)
- UNICEF
- Python Community
- Streamlit
- Microsoft Power BI
