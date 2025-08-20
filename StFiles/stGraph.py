# stGraph.py
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

# ====================== x-axis ordering ======================
def _x_order(df: pd.DataFrame) -> list | str:
    s = df["x"].astype(str)
    n = pd.to_numeric(s, errors="coerce")
    if n.notna().all():
        return s.iloc[n.argsort()].tolist()
    q = s.str.extract(r"Q(\d+)", expand=False)
    qn = pd.to_numeric(q, errors="coerce")
    if qn.notna().all():
        return s.iloc[qn.argsort()].tolist()
    return "ascending"

# ====================== Charts ======================
def wide_bar(df: pd.DataFrame, y_col: str, title: str, x_title="X", y_title="Total"):
    if df.empty:
        st.info("No data to plot."); return
    order = _x_order(df)
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("x:N", sort=order, title=x_title),
            y=alt.Y(f"{y_col}:Q", title=y_title, axis=alt.Axis(format=",")),
            tooltip=[
                alt.Tooltip("x:N", title=x_title),
                alt.Tooltip(f"{y_col}:Q", title=y_title, format=","),
            ],
        )
        .properties(title=title, height=360)
    )
    st.altair_chart(chart, use_container_width=True)

def bar_line_combo(
    df: pd.DataFrame,
    bar_col: str,
    line_col: str,
    title: str,
    x_title="X",
    y1_title="Bar",
    y2_title="Line",
):
    if df.empty:
        st.info("No data to plot."); return

    order = _x_order(df)

    # Convert potential Decimal to floats
    bar_vals = pd.to_numeric(df[bar_col], errors="coerce")
    line_vals = pd.to_numeric(df[line_col], errors="coerce")

    # Tooltip fields: millions + avg
    df = df.copy()
    df["bar_m"] = bar_vals / 1_000_000.0
    df["line_m"] = line_vals / 1_000_000.0
    df["avg_amt_per_count"] = (line_vals / bar_vals).replace([np.inf, -np.inf], np.nan)

    bar = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("x:N", sort=order, title=x_title),
            y=alt.Y(f"{bar_col}:Q", title=y1_title, axis=alt.Axis(format=",")),
            tooltip=[
                alt.Tooltip("x:N", title=x_title),
                alt.Tooltip("bar_m:Q", title=f"{y1_title} (M)", format=".2f"),
                alt.Tooltip("line_m:Q", title=f"{y2_title} (M)", format=".2f"),
                alt.Tooltip("avg_amt_per_count:Q", title="Avg Amount / Count", format=",.2f"),
            ],
        )
    )

    line = (
        alt.Chart(df)
        .mark_line(point=alt.OverlayMarkDef(color="red"), color="red")
        .encode(
            x=alt.X("x:N", sort=order, title=x_title),
            y=alt.Y(f"{line_col}:Q", title=y2_title, axis=alt.Axis(format=",", orient="right")),
            tooltip=[
                alt.Tooltip("x:N", title=x_title),
                alt.Tooltip("bar_m:Q", title=f"{y1_title} (M)", format=".2f"),
                alt.Tooltip("line_m:Q", title=f"{y2_title} (M)", format=".2f"),
                alt.Tooltip("avg_amt_per_count:Q", title="Avg Amount / Count", format=",.2f"),
            ],
        )
    )

    st.altair_chart(
        alt.layer(bar, line).resolve_scale(y="independent").properties(title=title, height=360),
        use_container_width=True
    )
