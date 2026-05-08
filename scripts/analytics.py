# =========================
# analytics.py
# =========================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ORANGE = "#FF6B00"
ORANGE_LIGHT = "#FF9A45"
ORANGE_PALE = "#FFD4A8"
BLACK = "#000000"
WHITE = "#FFFFFF"
GRID = "#E8E8E8"

ORANGE_SCALE = [
    [0.0, "#FFFFFF"],
    [0.25, "#FFD4A8"],
    [0.5, "#FF9A45"],
    [0.75, "#FF6B00"],
    [1.0, "#000000"],
]

QUAL_PALETTE = [
    "#FF6B00",
    "#000000",
    "#FF9A45",
    "#333333",
    "#FFD4A8",
    "#555555",
]

AXIS = dict(
    showgrid=True,
    gridcolor=GRID,
    zeroline=False,
    tickfont=dict(size=13, color=BLACK),
    title_font=dict(size=14, color=BLACK),
)

BASE_LAYOUT = dict(
    paper_bgcolor=WHITE,
    plot_bgcolor=WHITE,
    font=dict(size=13, color=BLACK),
    margin=dict(l=50, r=50, t=70, b=50),
)


def apply_theme(fig, title=""):

    fig.update_layout(
        **BASE_LAYOUT,
        title=dict(
            text=f"<b>{title}</b>",
            x=0,
            xanchor="left"
        )
    )

    return fig


# =========================
# COMPANY SHARE
# =========================
def chart_company_share(df, top_n=10):

    df_top = df.nlargest(top_n, "patents").copy()

    others = df["patents"].sum() - df_top["patents"].sum()

    if others > 0:
        df_top = pd.concat([
            df_top,
            pd.DataFrame([{
                "name": "Others",
                "patents": others
            }])
        ])

    fig = go.Figure(go.Pie(
        labels=df_top["name"],
        values=df_top["patents"],
        hole=0.5,
        marker=dict(
            colors=QUAL_PALETTE
        ),
        textinfo="label+percent"
    ))

    return apply_theme(fig, "Patent Share by Company")


# =========================
# INVENTOR DISTRIBUTION
# =========================
def chart_inventor_distribution(df):

    fig = go.Figure(go.Histogram(
        x=df["patents"],
        nbinsx=30,
        marker=dict(color=ORANGE)
    ))

    fig.update_layout(
        xaxis=dict(**AXIS, title="Patents"),
        yaxis=dict(**AXIS, title="Inventors")
    )

    return apply_theme(fig, "Inventor Productivity Distribution")


# =========================
# YOY GROWTH
# =========================
def chart_yoy_growth(df):

    df = df.sort_values("year").copy()

    df["growth"] = df["patents"].pct_change() * 100

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["year"],
        y=df["patents"],
        name="Patents",
        marker=dict(color=ORANGE_PALE)
    ))

    fig.add_trace(go.Scatter(
        x=df["year"],
        y=df["growth"],
        name="Growth %",
        mode="lines+markers",
        yaxis="y2",
        line=dict(color=BLACK)
    ))

    fig.update_layout(
        xaxis=dict(**AXIS, title="Year"),
        yaxis=dict(**AXIS, title="Patents"),
        yaxis2=dict(
            title="Growth %",
            overlaying="y",
            side="right"
        )
    )

    return apply_theme(fig, "Year-over-Year Growth")


# =========================
# COMPANY TREEMAP
# =========================
def chart_company_treemap(df, top_n=20):

    df_top = df.nlargest(top_n, "patents")

    fig = px.treemap(
        df_top,
        path=["name"],
        values="patents",
        color="patents",
        color_continuous_scale=ORANGE_SCALE
    )

    return apply_theme(fig, "Company Patent Treemap")


# =========================
# RANK VS PATENTS
# =========================
def chart_rank_vs_patents(df, entity_label="Company"):

    df = df.sort_values("patents", ascending=False).copy()

    df["rank"] = range(1, len(df) + 1)

    fig = go.Figure(go.Scatter(
        x=df["rank"],
        y=df["patents"],
        mode="markers",
        text=df["name"],
        marker=dict(
            color=ORANGE,
            size=8
        )
    ))

    fig.update_layout(
        xaxis=dict(**AXIS, type="log", title="Rank"),
        yaxis=dict(**AXIS, type="log", title="Patents")
    )

    return apply_theme(fig, f"{entity_label} Rank vs Patents")


# =========================
# CUMULATIVE SHARE
# =========================
def chart_cumulative_share(df):

    df = df.sort_values("patents", ascending=False).copy()

    df["cum_share"] = (
        df["patents"].cumsum()
        / df["patents"].sum()
    ) * 100

    df["rank"] = range(1, len(df) + 1)

    fig = go.Figure(go.Scatter(
        x=df["rank"],
        y=df["cum_share"],
        fill="tozeroy",
        line=dict(color=ORANGE)
    ))

    fig.update_layout(
        xaxis=dict(**AXIS, title="Company Rank"),
        yaxis=dict(**AXIS, title="Cumulative Share %")
    )

    return apply_theme(fig, "Cumulative Patent Share")


# =========================
# INVENTOR BOXPLOT
# =========================
def chart_inventor_boxplot(df):

    fig = go.Figure(go.Box(
        y=df["patents"],
        name="Inventors",
        boxpoints="outliers",
        marker=dict(color=ORANGE),
        line=dict(color=BLACK),
        fillcolor=ORANGE_PALE
    ))

    fig.update_layout(
        yaxis=dict(**AXIS, title="Patents")
    )

    return apply_theme(fig, "Inventor Patent Distribution")


# =========================
# ROLLING TREND
# =========================
def chart_rolling_trend(df, window=5):

    df = df.sort_values("year").copy()

    df["rolling"] = df["patents"].rolling(window).mean()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["year"],
        y=df["patents"],
        name="Actual",
        line=dict(color=ORANGE_LIGHT)
    ))

    fig.add_trace(go.Scatter(
        x=df["year"],
        y=df["rolling"],
        name="Rolling Average",
        line=dict(color=BLACK, width=3)
    ))

    fig.update_layout(
        xaxis=dict(**AXIS, title="Year"),
        yaxis=dict(**AXIS, title="Patents")
    )

    return apply_theme(fig, "Rolling Patent Trend")


# =========================
# INVENTOR BUBBLE
# =========================
def chart_inventor_bubble(df, top_n=30):

    df_top = df.nlargest(top_n, "patents").copy()

    df_top["rank"] = range(1, len(df_top) + 1)

    fig = go.Figure(go.Scatter(
        x=df_top["rank"],
        y=df_top["patents"],
        mode="markers",
        text=df_top["name"],
        marker=dict(
            size=df_top["patents"] / df_top["patents"].max() * 50 + 10,
            color=df_top["patents"],
            colorscale=ORANGE_SCALE,
            showscale=True
        )
    ))

    fig.update_layout(
        xaxis=dict(**AXIS, title="Rank"),
        yaxis=dict(**AXIS, title="Patents")
    )

    return apply_theme(fig, "Top Inventors Bubble Chart")


# =========================
# DECADE SUMMARY
# =========================
def chart_decade_summary(df):

    df = df.copy()

    df["decade"] = (
        df["year"] // 10 * 10
    ).astype(str) + "s"

    df_decade = (
        df.groupby("decade", as_index=False)["patents"]
        .sum()
    )

    fig = go.Figure(go.Bar(
        x=df_decade["decade"],
        y=df_decade["patents"],
        marker=dict(color=ORANGE)
    ))

    fig.update_layout(
        xaxis=dict(**AXIS, title="Decade"),
        yaxis=dict(**AXIS, title="Patents")
    )

    return apply_theme(fig, "Patent Activity by Decade")

