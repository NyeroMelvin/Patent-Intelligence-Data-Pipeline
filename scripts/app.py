# =========================
# app.py
# =========================

import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
from analytics import (
    chart_company_share,
    chart_inventor_distribution,
    chart_yoy_growth,
    chart_company_treemap,
    chart_rank_vs_patents,
    chart_cumulative_share,
    chart_inventor_boxplot,
    chart_rolling_trend,
    chart_inventor_bubble,
    chart_decade_summary,
)
import plotly.express as px


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Patent Analytics Dashboard",
    layout="wide",
    page_icon="📊"
)


# =========================
# LOAD CSS
# =========================
def load_css(filepath):
    with open(filepath) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css(Path(__file__).parent / "style.css")


# =========================
# CUSTOM UI FIXES
# =========================
# =========================
# CUSTOM UI FIXES
# =========================
st.markdown("""
<style>

/* Hide sidebar collapse button */
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Hide floating sidebar toggle button */
button[kind="header"] {
    display: none !important;
}

/* Hide toolbar */
[data-testid="stToolbar"] {
    display: none !important;
}

/* Hide decoration */
[data-testid="stDecoration"] {
    display: none !important;
}

/* Hide status widget */
[data-testid="stStatusWidget"] {
    display: none !important;
}

/* Hide main menu */
#MainMenu {
    visibility: hidden;
}

/* Hide footer */
footer {
    visibility: hidden;
}

/* Hide header */
header {
    visibility: hidden;
}

/* Hide accessibility keyboard helper */
[data-testid="stBaseButton-headerNoPadding"] {
    display: none !important;
}

/* Remove extra top spacing */
.block-container {
    padding-top: 1rem;
}

/* Cleaner sidebar */
section[data-testid="stSidebar"] {
    border-right: 1px solid #EEEEEE;
}

</style>
""", unsafe_allow_html=True)



# =========================
# TITLE
# =========================
st.title("Patent Analytics Dashboard")
st.markdown("Interactive insights from large-scale patent data")


# =========================
# DATA LOADER
# =========================
@st.cache_data
def load_data(query):
    db_path = Path(__file__).parent.parent / "data" / "patents.db"

    conn = sqlite3.connect(db_path)

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# =========================
# KPI METRICS
# =========================
stats = load_data("""
    SELECT 
        (SELECT COUNT(*) FROM patents) AS total_patents,
        (SELECT COUNT(*) FROM inventor_summary) AS total_inventors,
        (SELECT COUNT(*) FROM companies) AS total_companies
""")

total_patents = stats["total_patents"][0]
total_inventors = stats["total_inventors"][0]
total_companies = stats["total_companies"][0]

col1, col2, col3 = st.columns(3)

col1.metric("Total Patents", f"{total_patents:,}")
col2.metric("Total Inventors", f"{total_inventors:,}")
col3.metric("Total Companies", f"{total_companies:,}")

st.markdown("---")


# =========================
# SIDEBAR
# =========================
option = st.sidebar.radio(
    "Select Analysis",
    [
        "Top Companies",
        "Top Inventors",
        "Yearly Trends",
        "Company Patent Share",
        "Inventor Distribution",
        "YoY Growth Rate",
        "Company Treemap",
        "Rank vs Patents",
        "Cumulative Share",
        "Decade Summary",
    ]
)


# =========================
# TOP COMPANIES
# =========================
if option == "Top Companies":

    st.subheader("Top Companies by Patent Count")

    limit = st.slider("Number of companies", 5, 20, 10)

    with st.spinner("Loading companies..."):

        df = load_data(f"""
            SELECT name, patents
            FROM company_summary
            ORDER BY patents DESC
            LIMIT {limit}
        """)

    fig = px.bar(
        df,
        x="patents",
        y="name",
        orientation="h",
        text="patents",
        title="Top Patent Holding Companies"
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(
            family="Inter, Segoe UI, sans-serif",
            color="#1a1a1a"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, use_container_width=True)


# =========================
# TOP INVENTORS
# =========================
elif option == "Top Inventors":

    st.subheader("Top Inventors")

    limit = st.slider("Number of inventors", 5, 20, 10)

    with st.spinner("Loading inventors..."):

        df = load_data(f"""
            SELECT name, patents
            FROM inventor_summary
            ORDER BY patents DESC
            LIMIT {limit}
        """)

    fig = px.bar(
        df,
        x="patents",
        y="name",
        orientation="h",
        text="patents",
        title="Top Inventors by Patent Count"
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(
            family="Inter, Segoe UI, sans-serif",
            color="#1a1a1a"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, use_container_width=True)


# =========================
# YEARLY TRENDS
# =========================
elif option == "Yearly Trends":

    st.subheader("Patent Trends Over Time")

    with st.spinner("Loading trends..."):

        df = load_data("""
            SELECT year, patents
            FROM yearly_trends
            WHERE year BETWEEN '1900' AND '2025'
            ORDER BY year
        """)

    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    df = df.dropna(subset=["year"])

    df["year"] = df["year"].astype(int)

    year_range = st.slider(
        "Select Year Range",
        int(df["year"].min()),
        int(df["year"].max()),
        (2000, 2020)
    )

    df_filtered = df[
        (df["year"] >= year_range[0]) &
        (df["year"] <= year_range[1])
    ]

    fig = px.line(
        df_filtered,
        x="year",
        y="patents",
        title="Patent Activity Over Time"
    )

    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(
            family="Inter, Segoe UI, sans-serif",
            color="#1a1a1a"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_filtered, use_container_width=True)


# =========================
# COMPANY SHARE
# =========================
elif option == "Company Patent Share":

    st.subheader("Patent Share by Company")

    top_n = st.slider("Companies to highlight", 5, 20, 10)

    with st.spinner("Loading data..."):

        df = load_data("""
            SELECT name, patents
            FROM company_summary
            ORDER BY patents DESC
        """)

    col_left, col_right = st.columns([2, 1])

    with col_left:

        st.plotly_chart(
            chart_company_share(df, top_n=top_n),
            use_container_width=True
        )

    with col_right:

        st.dataframe(
            df.head(top_n),
            use_container_width=True
        )


# =========================
# INVENTOR DISTRIBUTION
# =========================
elif option == "Inventor Distribution":

    st.subheader("Inventor Productivity Distribution")

    with st.spinner("Loading data..."):

        df = load_data("""
            SELECT name, patents
            FROM inventor_summary
            ORDER BY patents DESC
        """)

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            chart_inventor_distribution(df),
            use_container_width=True
        )

    with col2:

        st.plotly_chart(
            chart_inventor_boxplot(df),
            use_container_width=True
        )

    st.markdown("### Summary Statistics")

    st.dataframe(
        df["patents"].describe().rename("Patents").to_frame(),
        use_container_width=True
    )


# =========================
# YOY GROWTH
# =========================
elif option == "YoY Growth Rate":

    st.subheader("Year-over-Year Patent Growth Rate")

    with st.spinner("Loading data..."):

        df = load_data("""
            SELECT year, patents
            FROM yearly_trends
            WHERE year BETWEEN '1900' AND '2025'
            ORDER BY year
        """)

    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    df = df.dropna(subset=["year"])

    df["year"] = df["year"].astype(int)

    year_range = st.slider(
        "Select Year Range",
        int(df["year"].min()),
        int(df["year"].max()),
        (1980, 2020)
    )

    df_filtered = df[
        (df["year"] >= year_range[0]) &
        (df["year"] <= year_range[1])
    ]

    st.plotly_chart(
        chart_yoy_growth(df_filtered),
        use_container_width=True
    )

    window = st.slider(
        "Rolling average window",
        3,
        10,
        5
    )

    st.plotly_chart(
        chart_rolling_trend(df_filtered, window=window),
        use_container_width=True
    )


# =========================
# COMPANY TREEMAP
# =========================
elif option == "Company Treemap":

    st.subheader("Patent Volume Treemap")

    top_n = st.slider("Number of companies", 10, 50, 20)

    with st.spinner("Loading data..."):

        df = load_data("""
            SELECT name, patents
            FROM company_summary
            ORDER BY patents DESC
        """)

    st.plotly_chart(
        chart_company_treemap(df, top_n=top_n),
        use_container_width=True
    )

    col_a, col_b = st.columns(2)

    with col_a:

        inventor_df = load_data("""
            SELECT name, patents
            FROM inventor_summary
            ORDER BY patents DESC
        """)

        st.plotly_chart(
            chart_inventor_bubble(inventor_df, top_n=30),
            use_container_width=True
        )

    with col_b:

        st.plotly_chart(
            chart_rank_vs_patents(df, entity_label="Company"),
            use_container_width=True
        )


# =========================
# RANK VS PATENTS
# =========================
elif option == "Rank vs Patents":

    st.subheader("Rank vs Patent Count")

    with st.spinner("Loading data..."):

        df_companies = load_data("""
            SELECT name, patents
            FROM company_summary
            ORDER BY patents DESC
        """)

        df_inventors = load_data("""
            SELECT name, patents
            FROM inventor_summary
            ORDER BY patents DESC
        """)

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            chart_rank_vs_patents(
                df_companies,
                entity_label="Company"
            ),
            use_container_width=True
        )

    with col2:

        st.plotly_chart(
            chart_rank_vs_patents(
                df_inventors,
                entity_label="Inventor"
            ),
            use_container_width=True
        )


# =========================
# CUMULATIVE SHARE
# =========================
elif option == "Cumulative Share":

    st.subheader("Cumulative Patent Share")

    with st.spinner("Loading data..."):

        df = load_data("""
            SELECT name, patents
            FROM company_summary
            ORDER BY patents DESC
        """)

    st.plotly_chart(
        chart_cumulative_share(df),
        use_container_width=True
    )


# =========================
# DECADE SUMMARY
# =========================
elif option == "Decade Summary":

    st.subheader("Patent Activity by Decade")

    with st.spinner("Loading data..."):

        df = load_data("""
            SELECT year, patents
            FROM yearly_trends
            WHERE year BETWEEN '1900' AND '2025'
            ORDER BY year
        """)

    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    df = df.dropna(subset=["year"])

    df["year"] = df["year"].astype(int)

    st.plotly_chart(
        chart_decade_summary(df),
        use_container_width=True
    )


# =========================
# FOOTER
# =========================
st.markdown("---")

