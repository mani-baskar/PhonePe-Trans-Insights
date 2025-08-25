# stGraph.py
import numpy as np
import pandas as pd
import altair as alt
import requests
import streamlit as st
import plotly.express as px
from pathlib import Path
import json
import geopandas as gpd

def get_geojson(url_or_path):
    if url_or_path.startswith('http'):
        return requests.get(url_or_path).json()
    else:
        import json
        with open(url_or_path, 'r', encoding='utf-8') as f:
            return json.load(f)

def plot_choropleth(df, geojson_data, location_col, color_col, featureidkey, title, label_name):
    fig = px.choropleth(
        data_frame=df,
        geojson=geojson_data,
        featureidkey=featureidkey,
        locations=location_col,
        color=color_col,
        color_continuous_scale="Viridis",
        hover_name=location_col,
        labels={color_col: label_name},
        projection="mercator",
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin=dict(r=0, t=50, l=0, b=0),
        title_text=title
    )
    st.plotly_chart(fig, use_container_width=True)

def clean_strings(df, cols):
    for col, case in cols:
        # Remove leading/trailing spaces
        df[col] = df[col].str.strip()

        # Replace "-" with space
        df[col] = df[col].str.replace("-", " ", regex=False)

        # Apply case formatting
        if case == 'title':
            df[col] = df[col].str.title()
        elif case == 'lower':
            df[col] = df[col].str.lower()
        elif case == 'upper':
            df[col] = df[col].str.upper()
    return df

def load_geojson_from_any(path: Path):
    """
    Reads GeoJSON directly, or uses GeoPandas to read TopoJSON/GeoJSON,
    and returns (geojson_dict, features_properties_keys).
    """
    # Try plain JSON first
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, dict) and raw.get("type") == "FeatureCollection":
        # Already GeoJSON
        gj = raw
    elif isinstance(raw, dict) and raw.get("type") == "Topology":
        # TopoJSON → use GeoPandas/Fiona (GDAL) to read it, then export to GeoJSON
        try:
            gdf = gpd.read_file(path.as_posix())
            # Ensure we have WGS84 for Plotly
            if gdf.crs is not None:
                gdf = gdf.to_crs(epsg=4326)
            gj = json.loads(gdf.to_json())
        except Exception as e:
            st.error(
                "Your file looks like TopoJSON and needs GeoPandas/GDAL to read.\n\n"
                "Please install: `pip install geopandas shapely fiona`\n\n"
                f"Loader error: {e}"
            )
            st.stop()
    else:
        st.error("Unsupported file format. Expecting GeoJSON FeatureCollection or TopoJSON.")
        st.stop()

    # Collect property keys from first feature
    props_keys = set()
    for feat in gj.get("features", [])[:50]:  # sample a few
        props_keys.update(feat.get("properties", {}).keys())
    return gj, props_keys

def get_district_key(prop_keys):
    CANDIDATES = [
        "DISTRICT", "district", "District", "DT_NAME", "dtname",
        "dt_name", "DIST_NAME", "district_n", "district_na", "NAME_2", "NAME"
    ]
    return next((k for k in CANDIDATES if k in prop_keys), None)


STATE_OVERRIDES = {
    # Use Title Case keys after normalization
    "Nct Of Delhi": "Delhi",
    "Andaman And Nicobar Island": "Andaman And Nicobar Islands",
    "Andaman And Nicobar Islands": "Andaman And Nicobar Islands",
    "Pondicherry": "Puducherry",
    "Dadra And Nagar Haveli": "Dadra And Nagar Haveli And Daman And Diu",
    "Daman And Diu": "Dadra And Nagar Haveli And Daman And Diu",
    # Add any DB/GeoJSON quirks you see here
}

def normalize_state_name(s: pd.Series) -> pd.Series:
    out = (
        s.astype(str)
         .str.strip()
         .str.replace(r"[-_]", " ", regex=True)          # hyphen/underscore -> space
         .str.replace("&", "and", regex=False)           # & -> and
         .str.replace(r"\s+", " ", regex=True)           # collapse spaces
         .str.title()
    )
    return out.replace(STATE_OVERRIDES)

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
    x_order=None,
    bar_scale="M",   # Scale for bar values: M, B, or T
    line_scale="M",  # Scale for line values: M, B, or T
):
    if df.empty:
        st.info("No data to plot."); return

    if x_order is None:
        if pd.api.types.is_categorical_dtype(df["x"]):
            x_order = list(df["x"].cat.categories)
        else:
            x_order = df["x"].tolist()

    scale_map = {
        "M": 1_000_000,
        "B": 1_000_000_000,
        "T": 1_000_000_000_000,
    }

    bar_divisor = scale_map.get(bar_scale.upper(), 1_000_000)
    line_divisor = scale_map.get(line_scale.upper(), 1_000_000)

    bar_vals = pd.to_numeric(df[bar_col], errors="coerce")
    line_vals = pd.to_numeric(df[line_col], errors="coerce")

    df = df.copy()
    df["x"] = df["x"].astype(str)
    df["bar_scaled"] = bar_vals / bar_divisor
    df["line_scaled"] = line_vals / line_divisor
    df["avg_amt_per_count"] = (line_vals / bar_vals).replace([np.inf, -np.inf], np.nan)

    bar = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("x:N", sort=x_order, title=x_title),
            y=alt.Y("bar_scaled:Q", title=f"{y1_title} ({bar_scale})", axis=alt.Axis(format=",.0f")),
            tooltip=[
                alt.Tooltip("x:N", title=x_title),
                alt.Tooltip("bar_scaled:Q", title=f"{y1_title} ({bar_scale})", format=",.2f"),
                alt.Tooltip("line_scaled:Q", title=f"{y2_title} ({line_scale})", format=",.2f"),
                alt.Tooltip("avg_amt_per_count:Q", title="Avg Amount / Count", format=",.2f"),
            ],
        )
    )

    line = (
        alt.Chart(df)
        .mark_line(point=alt.OverlayMarkDef(color="red"), color="red")
        .encode(
            x=alt.X("x:N", sort=x_order, title=x_title),
            y=alt.Y("line_scaled:Q", title=f"{y2_title} ({line_scale})", axis=alt.Axis(format=",.0f", orient="right")),
            tooltip=[
                alt.Tooltip("x:N", title=x_title),
                alt.Tooltip("bar_scaled:Q", title=f"{y1_title} ({bar_scale})", format=",.2f"),
                alt.Tooltip("line_scaled:Q", title=f"{y2_title} ({line_scale})", format=",.2f"),
                alt.Tooltip("avg_amt_per_count:Q", title="Avg Amount / Count", format=",.2f"),
            ],
        )
    )

    st.altair_chart(
        alt.layer(bar, line).resolve_scale(y="independent").properties(title=title, height=360),
        use_container_width=True,
    )

def grouped_bar_line_share_combo(
    df: pd.DataFrame,
    x_col: str,
    bar1_col: str,
    bar2_col: str,
    line_col: str,
    title: str,
    x_title: str = "X",
    bar1_title: str | None = None,   # None = auto from bar1_col
    bar2_title: str | None = None,   # None = auto from bar2_col (Proper Case)
    line_title: str = "Line",
    x_order=None,
    bar_colors=("#377eb8", "#4daf4a"),
    line_color="#e41a1c",
    raw_fmt=",.0f",
    pct_fmt=".1%",
    legend_orient: str = "bottom",
    legend_direction: str = "horizontal",
    legend_columns: int = 2,
    height: int = 380,               # <-- ONLY size control you asked for
):
    """
    Grouped bars show each series as share of its own column total (0..1).
    Line stays in raw numbers. Both Y axes are hidden; numbers are in tooltips.
    """

    if df is None or df.empty:
        st.info("No data to plot."); return

    # nicify text helper
    def _nicify(s: str) -> str:
        return str(s).replace("_", " ").strip().title()

    # auto titles (you asked specifically for bar2_col)
    if not bar1_title:
        bar1_title = _nicify(bar1_col)
    if not bar2_title:
        bar2_title = _nicify(bar2_col)

    # clean & types
    work = df.copy()
    for col in [bar1_col, bar2_col, line_col]:
        work[col] = pd.to_numeric(work[col], errors="coerce")\
                        .replace([np.inf, -np.inf], np.nan).fillna(0)
    work[x_col] = work[x_col].astype(str)

    # x order
    if x_order is None:
        x_order = list(work[x_col].cat.categories) if pd.api.types.is_categorical_dtype(work[x_col]) else work[x_col].tolist()

    # totals and shares
    tot1 = float(work[bar1_col].sum())
    tot2 = float(work[bar2_col].sum())
    work["bar1_raw"] = work[bar1_col]
    work["bar2_raw"] = work[bar2_col]
    work["bar1_pct"] = (work[bar1_col] / tot1) if tot1 > 0 else 0.0
    work["bar2_pct"] = (work[bar2_col] / tot2) if tot2 > 0 else 0.0

    # long df for grouped bars
    n = len(work)
    bars_long = pd.DataFrame({
        x_col:       np.concatenate([work[x_col].values, work[x_col].values]),
        "series":    ([bar1_title] * n) + ([bar2_title] * n),
        "value_raw": np.concatenate([work["bar1_raw"].values, work["bar2_raw"].values]),
        "value_pct": np.concatenate([work["bar1_pct"].values, work["bar2_pct"].values]),
    })

    # bars (axis hidden)
    bars = (
        alt.Chart(bars_long)
        .mark_bar()
        .encode(
            x=alt.X(f"{x_col}:N", sort=x_order, title=x_title),
            xOffset=alt.X("series:N", title=None),
            y=alt.Y("value_pct:Q", axis=None),  # hide left axis
            color=alt.Color(
                "series:N",
                scale=alt.Scale(range=list(bar_colors)),
                legend=alt.Legend(
                    title=None, orient=legend_orient,
                    direction=legend_direction, columns=legend_columns,
                    symbolType="square",
                ),
            ),
            tooltip=[
                alt.Tooltip(f"{x_col}:N", title=x_title),
                alt.Tooltip("series:N", title="Series"),
                alt.Tooltip("value_pct:Q", title="Share", format=pct_fmt),
                alt.Tooltip("value_raw:Q", title="Raw value", format=raw_fmt),
            ],
        )
    )

    # line (raw numbers; axis hidden)
    line = (
        alt.Chart(work)
        .mark_line(point=True, color=line_color, strokeWidth=2)
        .encode(
            x=alt.X(f"{x_col}:N", sort=x_order, title=x_title),
            y=alt.Y(f"{line_col}:Q", axis=None),  # hide right axis
            tooltip=[
                alt.Tooltip(f"{x_col}:N", title=x_title),
                alt.Tooltip(f"{line_col}:Q", title=line_title, format=raw_fmt),
            ],
        )
    )

    chart = (
        alt.layer(bars, line)
        .resolve_scale(y="independent")
        .properties(title=title, height=height)   # <-- control height only
    )
    st.altair_chart(chart, use_container_width=True)

def bar_line_dynamic_scale(
    df: pd.DataFrame,
    x_col: str,
    bar_col: str,
    line_col: str,
    title: str,
    x_title: str = "X",
    bar_title: str | None = None,
    line_title: str = "Line",
    x_order=None,
    bar_color="#173cb8",
    line_color="#e41a1c",
    raw_fmt=",.0f",
    height: int = 380,
):
    if df is None or df.empty:
        st.info("No data to plot.")
        return

    def _nicify(s: str) -> str:
        return str(s).replace("_", " ").strip().title()

    if not bar_title:
        bar_title = _nicify(bar_col)

    # Prepare working df and convert to numeric safely
    work = df.copy()
    for col in [bar_col, line_col]:
        work[col] = pd.to_numeric(work[col], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0)
    work[x_col] = work[x_col].astype(str)

    if x_order is None:
        if pd.api.types.is_categorical_dtype(work[x_col]):
            x_order = list(work[x_col].cat.categories)
        else:
            x_order = work[x_col].tolist()

    # Use raw values directly, no scaling
    work["bar_raw"] = work[bar_col]
    work["line_raw"] = work[line_col]

    work["bar_scaled"] = work["bar_raw"]  # No scaling
    work["line_scaled"] = work["line_raw"]  # No scaling

    # Build bar chart (axis hidden)
    bar = (
        alt.Chart(work)
        .mark_bar(color=bar_color)
        .encode(
            x=alt.X(f"{x_col}:N", sort=x_order, title=x_title),
            y=alt.Y("bar_scaled:Q", axis=None, title=bar_title),
            tooltip=[
                alt.Tooltip(f"{x_col}:N", title=x_title),
                alt.Tooltip("bar_raw:Q", title=f"{bar_title}", format=raw_fmt),
            ],
        )
    )

    # Build line chart (axis hidden)
    line = (
        alt.Chart(work)
        .mark_line(point=True, color=line_color, strokeWidth=2)
        .encode(
            x=alt.X(f"{x_col}:N", sort=x_order, title=x_title),
            y=alt.Y("line_scaled:Q", axis=None, title=line_title),
            tooltip=[
                alt.Tooltip(f"{x_col}:N", title=x_title),
                alt.Tooltip("line_raw:Q", title=f"{line_title}", format=raw_fmt),
            ],
        )
    )

    # Combine layer with independent y-axes (both hidden)
    chart = (
        alt.layer(bar, line)
        .resolve_scale(y="independent")
        .properties(title=title, height=height)
    )

    st.altair_chart(chart, use_container_width=True)