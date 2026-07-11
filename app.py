"""
WHO Vaccination Data Analysis & Visualization Dashboard
INNOVEXIS | HealthTech-adjacent Data Science Capstone
Author: P Suman Sangeet

Run locally:
    python generate_database.py   # builds who_vaccination.db (once)
    streamlit run app.py

Deploy on Streamlit Community Cloud:
    - Push this folder to GitHub (include who_vaccination.db, or let the app
      auto-generate synthetic data on first boot -- see load_data() below)
    - Set Python version via runtime.txt, pin versions via requirements.txt
"""

import sqlite3
from pathlib import Path
from io import BytesIO

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# PATHS (pathlib -> robust regardless of working directory)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "vaccination.db"
TABLE_NAME = "coverage"


# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="WHO Vaccination Analytics",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CUSTOM CSS -- recruiter-friendly polish
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .kpi-card {
        background: linear-gradient(135deg, #1c2333 0%, #232b3d 100%);
        border: 1px solid #2d3548;
        border-radius: 12px;
        padding: 18px 16px;
        text-align: center;
    }
    .kpi-value { font-size: 28px; font-weight: 700; color: #4fd1c5; }
    .kpi-label { font-size: 13px; color: #9aa4b2; text-transform: uppercase; letter-spacing: 0.06em; }
    .section-header {
        font-size: 22px; font-weight: 700; margin-top: 8px; margin-bottom: 4px;
        border-left: 4px solid #4fd1c5; padding-left: 10px;
    }
    div[data-testid="stMetricValue"] { color: #4fd1c5; }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# DATA LAYER -- SQL integration with caching
# ---------------------------------------------------------------------------
@st.cache_resource
def get_connection():
    if not DB_PATH.exists():
        st.error(f"Database not found:\n{DB_PATH}")
        st.stop()

    return sqlite3.connect(DB_PATH, check_same_thread=False)


@st.cache_data(ttl=3600)
def run_query(query: str, params: tuple = ()) -> pd.DataFrame:
    conn = get_connection()
    return pd.read_sql_query(query, conn, params=params)


@st.cache_data(ttl=3600)
def load_full_data():
    df = run_query(f"SELECT * FROM {TABLE_NAME}")

    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Rename database columns
    df.rename(columns={
        "name": "country",
        "antigen": "vaccine"
    }, inplace=True)

    # Create region column
    if "group" in df.columns:
        df["region"] = df["group"]
    
    # Ensure year is numeric
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    # Remove invalid years like 0
    df = df[df["year"] > 1900]

    # Ensure incidence numeric casting if it exists
    if "incidence_rate" in df.columns:
        df["incidence_rate"] = pd.to_numeric(df["incidence_rate"], errors="coerce")

    return df

@st.cache_data(ttl=3600)
def get_filter_options():
    df = load_full_data()

    countries = sorted(df["country"].dropna().unique())
    vaccines = sorted(df["vaccine"].dropna().unique())
    regions = sorted(df["region"].dropna().unique())
    years = sorted(df["year"].dropna().unique())

    return countries, vaccines, regions, years


def apply_filters(df, countries, vaccines, regions, year_range):
    out = df.copy()
    if countries:
        out = out[out["country"].isin(countries)]
    if vaccines:
        out = out[out["vaccine"].isin(vaccines)]
    if regions:
        out = out[out["region"].isin(regions)]
    out = out[(out["year"] >= year_range[0]) & (out["year"] <= year_range[1])]
    return out


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="data")
    return buf.getvalue()


def kpi_card(col, label, value):
    with col:
        st.markdown(
            f"""<div class="kpi-card">
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-label">{label}</div>
                </div>""",
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# LOAD DATA + FILTER STATE
# ---------------------------------------------------------------------------
df_all = load_full_data()
all_countries, all_vaccines, all_regions, all_years = get_filter_options()
min_year, max_year = int(min(all_years)), int(max(all_years))

# ---------------------------------------------------------------------------
# SIDEBAR -- navigation + global filters
# ---------------------------------------------------------------------------
st.sidebar.markdown("## 💉 WHO Vaccination Analytics")
st.sidebar.caption("P Suman Sangeet · INNOVEIS")
st.sidebar.divider()

PAGES = [
    "🏠 Home",
    "📊 Global Overview",
    "🌍 Country Analysis",
    "💉 Vaccine Analysis",
    "📈 Trends",
    "🗺️ World Map",
    "🔍 Compare Countries",
    "📄 Download Reports",
]
page = st.sidebar.radio("Navigate", PAGES, label_visibility="collapsed")

st.sidebar.divider()
st.sidebar.markdown("### 🔧 Global Filters")

f_regions = st.sidebar.multiselect("Region", all_regions, default=[])
f_countries = st.sidebar.multiselect("Country", all_countries, default=[])
f_vaccines = st.sidebar.multiselect("Vaccine", all_vaccines, default=[])
f_years = st.sidebar.slider("Year Range", min_year, max_year, (min_year, max_year))

st.sidebar.divider()
st.sidebar.caption("Data source: WHO Vaccination Datasets (5 files, ~716K rows) · SQLite-backed")

df = apply_filters(df_all, f_countries, f_vaccines, f_regions, f_years)

if df.empty:
    st.warning("No data matches the current filter selection. Adjust filters in the sidebar.")
    st.stop()

# ---------------------------------------------------------------------------
# SHARED KPI COMPUTATION
# ---------------------------------------------------------------------------
def compute_kpis(data: pd.DataFrame) -> dict:
    return {
        "Total Records": f"{len(data):,}",
        "Total Countries": f"{data['country'].nunique():,}",
        "Total Vaccines": f"{data['vaccine'].nunique():,}",
        "Total Years": f"{data['year'].nunique():,}",
        "Average Coverage": f"{data['coverage'].mean():.1f}%",
        "Maximum Coverage": f"{data['coverage'].max():.1f}%",
        "Minimum Coverage": f"{data['coverage'].min():.1f}%",
    }


# ===========================================================================
# PAGE: HOME
# ===========================================================================
if page == "🏠 Home":
    st.markdown("# 💉 WHO Vaccination Data Analysis & Visualization")
    st.caption("End-to-end analytics pipeline: Python cleaning → SQLite → Streamlit dashboard")
    st.divider()

    kpis = compute_kpis(df)
    cols = st.columns(4)
    for c, (label, value) in zip(cols, list(kpis.items())[:4]):
        kpi_card(c, label, value)
    cols2 = st.columns(3)
    for c, (label, value) in zip(cols2, list(kpis.items())[4:]):
        kpi_card(c, label, value)

    st.write("")
    st.markdown('<div class="section-header">Project Summary</div>', unsafe_allow_html=True)
    left, right = st.columns([2, 1])
    with left:
        st.markdown("""
        This dashboard analyzes global vaccination coverage across countries, regions,
        vaccine types, and years using WHO vaccination datasets.

        **Pipeline:**
        - 5 raw WHO Excel datasets cleaned and standardized with pandas
        - Consolidated into a single SQLite database for efficient SQL-backed querying
        - Interactive Plotly visualizations for exploratory data analysis
        - Filterable, cached Streamlit dashboard for deployment

        Use the sidebar to navigate between pages and apply filters — all pages respond
        to the same global Region / Country / Vaccine / Year filters.
        """)
    with right:
        top_vax = df.groupby("vaccine")["coverage"].mean().sort_values(ascending=False).head(5)
        fig = px.bar(top_vax, orientation="h", title="Top 5 Vaccines by Avg Coverage",
                     labels={"value": "Avg Coverage (%)", "vaccine": ""}, color=top_vax.values,
                     color_continuous_scale="Teal")
        fig.update_layout(showlegend=False, coloraxis_showscale=False, height=280,
                           margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Quick Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(20), use_container_width=True, height=300)


# ===========================================================================
# PAGE: GLOBAL OVERVIEW
# ===========================================================================
elif page == "📊 Global Overview":
    st.markdown("# 📊 Global Overview")
    kpis = compute_kpis(df)
    cols = st.columns(5)
    for c, (label, value) in zip(cols, list(kpis.items())[:5]):
        kpi_card(c, label, value)
    st.write("")

    # ---------- ROW 2 : COVERAGE & INCIDENCE ----------
    trend = df.groupby("year")["coverage"].mean().reset_index()

    fig_trend = px.line(
        trend,
        x="year",
        y="coverage",
        markers=True,
        title="Coverage Trend Over Time",
        labels={"coverage": "Avg Coverage (%)"},
    )
    fig_trend.update_traces(line_color="#4fd1c5")

    if "incidence_rate" in df.columns:
        r2c1, r2c2 = st.columns(2)
        with r2c1:
            st.plotly_chart(fig_trend, use_container_width=True)
        with r2c2:
            inc = df.groupby("year")["incidence_rate"].mean().reset_index()
            fig_inc = px.line(
                inc,
                x="year",
                y="incidence_rate",
                markers=True,
                title="Disease Incidence Trend",
                labels={"incidence_rate": "Avg Incidence Rate"},
            )
            fig_inc.update_traces(line_color="#f56565")
            st.plotly_chart(fig_inc, use_container_width=True)
    else:
        st.plotly_chart(fig_trend, use_container_width=True)

    # ---------- ROW 3 : TOP / BOTTOM COUNTRIES ----------
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        top10 = df.groupby("country")["coverage"].mean().sort_values(ascending=False).head(10)
        fig = px.bar(top10[::-1], orientation="h", title="Top 10 Countries by Avg Coverage",
                     labels={"value": "Avg Coverage (%)", "country": ""})
        fig.update_traces(marker_color="#4fd1c5")
        st.plotly_chart(fig, use_container_width=True)
    with r3c2:
        bottom10 = df.groupby("country")["coverage"].mean().sort_values().head(10)
        fig = px.bar(bottom10[::-1], orientation="h", title="Bottom 10 Countries by Avg Coverage",
                     labels={"value": "Avg Coverage (%)", "country": ""})
        fig.update_traces(marker_color="#f56565")
        st.plotly_chart(fig, use_container_width=True)

    # ---------- ROW 4 : DISTRIBUTION & SPREAD ----------
    r4c1, r4c2 = st.columns(2)
    with r4c1:
        fig = px.histogram(df, x="coverage", nbins=30, title="Coverage Distribution (Histogram)")
        fig.update_traces(marker_color="#4fd1c5")
        st.plotly_chart(fig, use_container_width=True)
    with r4c2:
        fig = px.box(df, x="region", y="coverage", title="Coverage Spread by Region (Box Plot)",
                     color="region")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ---------- ROW 5 : SCATTER & CORRELATION ----------
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in ["year", "id"]]

    if "incidence_rate" in df.columns and len(numeric_cols) >= 2:
        r5c1, r5c2 = st.columns(2)
        with r5c1:
            fig_scatter = px.scatter(
                df,
                x="coverage",
                y="incidence_rate",
                color="region",
                opacity=0.5,
                title="Coverage vs Incidence Rate (Scatter)",
                labels={
                    "coverage": "Coverage (%)",
                    "incidence_rate": "Incidence Rate",
                },
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        with r5c2:
            corr = df[numeric_cols].corr()
            fig_corr = px.imshow(
                corr,
                text_auto=".2f",
                title="Correlation Matrix",
                color_continuous_scale="Teal",
                aspect="auto",
            )
            st.plotly_chart(fig_corr, use_container_width=True)
    else:
        if len(numeric_cols) >= 2:
            corr = df[numeric_cols].corr()
            fig_corr = px.imshow(
                corr,
                text_auto=".2f",
                title="Correlation Matrix",
                color_continuous_scale="Teal",
                aspect="auto",
            )
            st.plotly_chart(fig_corr, use_container_width=True)

# ===========================================================================
# PAGE: COUNTRY ANALYSIS
# ===========================================================================
elif page == "🌍 Country Analysis":
    st.markdown("# 🌍 Country Analysis")
    country_choice = st.selectbox("Select a country to drill down", sorted(df["country"].unique()))
    cdf = df[df["country"] == country_choice]

    kpis = compute_kpis(cdf)
    cols = st.columns(5)
    for c, (label, value) in zip(cols, list(kpis.items())[:5]):
        kpi_card(c, label, value)
    st.write("")

    c1, c2 = st.columns(2)
    with c1:
        trend = cdf.groupby("year")["coverage"].mean().reset_index()
        fig = px.area(trend, x="year", y="coverage", title=f"{country_choice}: Coverage Over Time",
                       labels={"coverage": "Avg Coverage (%)"})
        fig.update_traces(line_color="#4fd1c5", fillcolor="rgba(79,209,197,0.25)")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        vax_avg = cdf.groupby("vaccine")["coverage"].mean().sort_values(ascending=False)
        fig = px.bar(vax_avg, title=f"{country_choice}: Avg Coverage by Vaccine",
                     labels={"value": "Avg Coverage (%)", "vaccine": ""})
        fig.update_traces(marker_color="#4fd1c5")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Detailed Records</div>', unsafe_allow_html=True)
    st.dataframe(cdf.sort_values("year", ascending=False), use_container_width=True, height=300)


# ===========================================================================
# PAGE: VACCINE ANALYSIS
# ===========================================================================
elif page == "💉 Vaccine Analysis":
    st.markdown("# 💉 Vaccine Analysis")
    vaccine_choice = st.selectbox("Select a vaccine to drill down", sorted(df["vaccine"].unique()))
    vdf = df[df["vaccine"] == vaccine_choice]

    kpis = compute_kpis(vdf)
    cols = st.columns(5)
    for c, (label, value) in zip(cols, list(kpis.items())[:5]):
        kpi_card(c, label, value)
    st.write("")

    c1, c2 = st.columns(2)
    with c1:
        trend = vdf.groupby("year")["coverage"].mean().reset_index()
        fig = px.line(trend, x="year", y="coverage", markers=True,
                       title=f"{vaccine_choice}: Global Coverage Trend")
        fig.update_traces(line_color="#4fd1c5")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        region_avg = vdf.groupby("region")["coverage"].mean().sort_values(ascending=False)
        fig = px.bar(region_avg, title=f"{vaccine_choice}: Avg Coverage by Region",
                     labels={"value": "Avg Coverage (%)", "region": ""}, color=region_avg.values,
                     color_continuous_scale="Teal")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Top / Bottom Performing Countries</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        top = vdf.groupby("country")["coverage"].mean().sort_values(ascending=False).head(10)
        st.dataframe(top.reset_index().rename(columns={"coverage": "Avg Coverage (%)"}),
                     use_container_width=True, hide_index=True)
    with c4:
        bottom = vdf.groupby("country")["coverage"].mean().sort_values().head(10)
        st.dataframe(bottom.reset_index().rename(columns={"coverage": "Avg Coverage (%)"}),
                     use_container_width=True, hide_index=True)

# ===========================================================================
# PAGE: TRENDS
# ===========================================================================
elif page == "📈 Trends":
    st.markdown("# 📈 Trends")
    st.caption("Coverage trends over time, sliced by region and vaccine.")

    kpis = compute_kpis(df)
    cols = st.columns(5)
    for c, (label, value) in zip(cols, list(kpis.items())[:5]):
        kpi_card(c, label, value)
    st.write("")

    c1, c2 = st.columns(2)
    with c1:
        trend_region = df.groupby(["year", "region"])["coverage"].mean().reset_index()
        fig = px.line(trend_region, x="year", y="coverage", color="region", markers=True,
                       title="Coverage Trend by Region",
                       labels={"coverage": "Avg Coverage (%)"})
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        top_vaccines = df.groupby("vaccine")["coverage"].mean().sort_values(ascending=False).head(6).index
        trend_vax = df[df["vaccine"].isin(top_vaccines)].groupby(["year", "vaccine"])["coverage"].mean().reset_index()
        fig = px.line(trend_vax, x="year", y="coverage", color="vaccine", markers=True,
                       title="Coverage Trend — Top 6 Vaccines",
                       labels={"coverage": "Avg Coverage (%)"})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Year-over-Year Change</div>', unsafe_allow_html=True)
    yoy = df.groupby("year")["coverage"].mean().diff().reset_index()
    yoy.columns = ["year", "change"]
    yoy = yoy.dropna()
    fig = px.bar(yoy, x="year", y="change", title="Year-over-Year Change in Avg Coverage (pp)",
                 labels={"change": "Change (percentage points)"},
                 color="change", color_continuous_scale="Teal")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Cumulative Coverage Growth</div>', unsafe_allow_html=True)
    cum = df.groupby("year")["coverage"].mean().reset_index()
    cum["cumulative_avg"] = cum["coverage"].expanding().mean()
    fig = px.area(cum, x="year", y="cumulative_avg", title="Running Average Coverage",
                   labels={"cumulative_avg": "Running Avg Coverage (%)"})
    fig.update_traces(line_color="#4fd1c5")
    st.plotly_chart(fig, use_container_width=True)


# ===========================================================================
# PAGE: WORLD MAP
# ===========================================================================
elif page == "🗺️ World Map":
    st.markdown("# 🗺️ World Map")
    st.caption("Geographic distribution of vaccination coverage. Uses the year range and "
               "vaccine filters set in the sidebar (country/region filters are ignored here "
               "so the whole map stays visible).")

    map_year = st.slider("Select year for map snapshot", min_year, max_year, max_year, key="map_year")

    map_df = df_all.copy()
    if f_vaccines:
        map_df = map_df[map_df["vaccine"].isin(f_vaccines)]
    if f_regions:
        map_df = map_df[map_df["region"].isin(f_regions)]
    map_df = map_df[map_df["year"] == map_year]

    if map_df.empty:
        st.warning("No data available for that year with the current vaccine/region filters.")
    else:
        geo = map_df.groupby("country", as_index=False)["coverage"].mean()
        fig = px.choropleth(
            geo,
            locations="country",
            locationmode="country names",
            color="coverage",
            hover_name="country",
            color_continuous_scale="Teal",
            range_color=(0, 100),
            title=f"Avg Vaccination Coverage by Country — {map_year}",
            labels={"coverage": "Avg Coverage (%)"},
        )
        fig.update_layout(
            geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False),
            margin=dict(l=0, r=0, t=40, b=0),
            height=520,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-header">Highest & Lowest Coverage Countries</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.dataframe(
                geo.sort_values("coverage", ascending=False).head(10)
                   .rename(columns={"coverage": "Avg Coverage (%)"}),
                use_container_width=True, hide_index=True,
            )
        with c2:
            st.dataframe(
                geo.sort_values("coverage").head(10)
                   .rename(columns={"coverage": "Avg Coverage (%)"}),
                use_container_width=True, hide_index=True,
            )


# ===========================================================================
# PAGE: COMPARE COUNTRIES
# ===========================================================================
elif page == "🔍 Compare Countries":
    st.markdown("# 🔍 Compare Countries")
    st.caption("Side-by-side comparison across countries, using the global filters in the sidebar.")

    compare_choices = st.multiselect(
        "Select countries to compare (2-6 recommended)",
        all_countries,
        default=sorted(df["country"].unique())[:3] if not df.empty else [],
    )

    if len(compare_choices) < 2:
        st.info("Select at least two countries above to compare.")
    else:
        cdf = df[df["country"].isin(compare_choices)]

        st.markdown('<div class="section-header">Coverage Over Time</div>', unsafe_allow_html=True)
        trend = cdf.groupby(["year", "country"])["coverage"].mean().reset_index()
        fig = px.line(trend, x="year", y="coverage", color="country", markers=True,
                       labels={"coverage": "Avg Coverage (%)"})
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-header">Avg Coverage by Country</div>', unsafe_allow_html=True)
            avg = cdf.groupby("country")["coverage"].mean().sort_values(ascending=False)
            fig = px.bar(avg, title="Average Coverage", labels={"value": "Avg Coverage (%)", "country": ""},
                         color=avg.values, color_continuous_scale="Teal")
            fig.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown('<div class="section-header">Coverage by Vaccine (Grouped Bar)</div>', unsafe_allow_html=True)
            vax_comp = cdf.groupby(["country", "vaccine"])["coverage"].mean().reset_index()
            top_vax_for_compare = cdf.groupby("vaccine")["coverage"].mean().sort_values(ascending=False).head(8).index
            vax_comp = vax_comp[vax_comp["vaccine"].isin(top_vax_for_compare)]
            fig = px.bar(vax_comp, x="vaccine", y="coverage", color="country", barmode="group",
                         labels={"coverage": "Avg Coverage (%)"})
            fig.update_xaxes(tickangle=-35)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-header">Summary Table</div>', unsafe_allow_html=True)
        summary = cdf.groupby("country").agg(
            avg_coverage=("coverage", "mean"),
            max_coverage=("coverage", "max"),
            min_coverage=("coverage", "min"),
            vaccines_tracked=("vaccine", "nunique"),
            years_tracked=("year", "nunique"),
        ).round(1).sort_values("avg_coverage", ascending=False)
        st.dataframe(summary, use_container_width=True)


# ===========================================================================
# PAGE: DOWNLOAD REPORTS
# ===========================================================================
elif page == "📄 Download Reports":
    st.markdown("# 📄 Download Reports")
    st.caption("Export the currently filtered dataset and summary tables.")

    st.markdown('<div class="section-header">Filtered Raw Data</div>', unsafe_allow_html=True)
    st.write(f"Current selection: **{len(df):,}** rows across "
             f"**{df['country'].nunique()}** countries, **{df['vaccine'].nunique()}** vaccines, "
             f"**{df['year'].nunique()}** years.")
    st.dataframe(df.head(50), use_container_width=True, height=300)

    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "⬇️ Download Filtered Data (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="who_vaccination_filtered.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "⬇️ Download Filtered Data (Excel)",
            data=to_excel_bytes(df),
            file_name="who_vaccination_filtered.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    st.markdown('<div class="section-header">Country Summary Report</div>', unsafe_allow_html=True)
    country_summary = df.groupby("country").agg(
        avg_coverage=("coverage", "mean"),
        max_coverage=("coverage", "max"),
        min_coverage=("coverage", "min"),
        vaccines_tracked=("vaccine", "nunique"),
        years_tracked=("year", "nunique"),
        records=("coverage", "count"),
    ).round(1).sort_values("avg_coverage", ascending=False).reset_index()
    st.dataframe(country_summary, use_container_width=True, height=300)

    c3, c4 = st.columns(2)
    with c3:
        st.download_button(
            "⬇️ Download Country Summary (CSV)",
            data=country_summary.to_csv(index=False).encode("utf-8"),
            file_name="who_vaccination_country_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c4:
        st.download_button(
            "⬇️ Download Country Summary (Excel)",
            data=to_excel_bytes(country_summary),
            file_name="who_vaccination_country_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )