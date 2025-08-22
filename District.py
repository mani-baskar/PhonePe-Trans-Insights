import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
import geopandas as gpd

st.set_page_config(page_title="India Districts Choropleth", layout="wide")
st.title("India Districts Visualization")

# --- 1) Load the districts GeoJSON (or TopoJSON) ---
# Point to your uploaded file path
DISTRICTS_PATH = Path("src/india-districts-2019-734.json")

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

geojson_data, prop_keys = load_geojson_from_any(DISTRICTS_PATH)

# --- 2) Pick the district-name property automatically ---
# Common keys seen in Indian district datasets
CANDIDATES = [
    "DISTRICT", "district", "District", "DT_NAME", "dtname",
    "dt_name", "DIST_NAME", "district_n", "district_na", "NAME_2", "NAME"
]
district_key = next((k for k in CANDIDATES if k in prop_keys), None)

if not district_key:
    st.error(
        "Couldn't find a district name column in the GeoJSON properties.\n\n"
        f"Available keys include: {sorted(list(prop_keys))[:20]} ...\n"
        "Please rename/choose the district column and update the code."
    )
    st.stop()

st.success(f"Using district name column: `{district_key}`")

# --- 3) Example data (replace with your real metrics) ---
# IMPORTANT: 'district' values must match the names in the GeoJSON `properties[district_key]`
example_data = pd.DataFrame({
    "district": [
        # Replace with real district names as they appear in your file
        "Bengaluru Urban", "Pune", "Chennai", "New Delhi", "Ernakulam"
    ],
    "value": [10, 20, 30, 40, 50]
})

# --- 4) Build a mapping table to help you check name matches ---
# (Optionally show a preview so you can copy exact names)
if st.checkbox("Show a sample of available district names in the file"):
    names = sorted({
        feat["properties"].get(district_key, "")
        for feat in geojson_data["features"]
    })
    st.write(pd.DataFrame({district_key: names}).head(50))

# --- 5) Draw the Plotly choropleth ---
fig = px.choropleth(
    data_frame=example_data,
    geojson=geojson_data,
    featureidkey=f"properties.{district_key}",  # <-- must match the property name
    locations="district",                      # <-- your dataframe column with district names
    color="value",
    color_continuous_scale="Viridis",
    hover_name="district",
    labels={"value": "Value"},
    projection="mercator",
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin=dict(r=0, t=50, l=0, b=0),
    title_text="India Districts Choropleth Map"
)

st.plotly_chart(fig, use_container_width=True)
