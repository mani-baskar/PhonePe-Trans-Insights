import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Load GeoJSON for India states
state_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
state_geojson_data = requests.get(state_geojson_url).json()

# Example data: Replace this with your real data where "state" matches "properties.ST_NM"
data = pd.DataFrame({
    "state": ["Karnataka", "Maharashtra", "Tamil Nadu", "Delhi", "Kerala"],
    "value": [10, 20, 30, 40, 50]
})

# Create Plotly Express choropleth figure
fig = px.choropleth(
    data_frame=data,
    geojson=state_geojson_data,
    featureidkey="properties.ST_NM",
    locations="state",
    color="value",
    color_continuous_scale="Viridis",
    projection="mercator",
    hover_name="state",
    labels={"value": "Value"},
)

# Configure map view
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, title_text="India States Choropleth Map")

# Show in Streamlit
st.title("India Map Visualization")
st.plotly_chart(fig, use_container_width=True)
