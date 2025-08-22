import streamlit as st
from StFiles.stDBProcess import get_lists, ENGINE
from StFiles.stGraph import wide_bar, bar_line_combo, grouped_bar_line_share_combo, bar_line_dynamic_scale
import pandas as pd
from sqlalchemy import text
import requests
import plotly.express as px
from pathlib import Path
import json
ss = st.session_state
ss.setdefault("summary", "Use buttons below. Multi-Select keeps expanders open and lets you pick many.")
ss.setdefault("tab_locked", None)
EXP_TITLES = ["Year", "Quarterly", "State"]
INSURANCE = get_lists("agg_ins")
TRANSACTION = get_lists("agg_trans")
USER = get_lists("agg_user")

def expander_with_checkboxes(title, key_prefix, options, disabled=False):
    selected_key = f"{key_prefix}_{title}_selected"
    ss.setdefault(selected_key, [])
    with st.expander(title, expanded=False):
        selected = []
        cols = st.columns(4)
        for idx, opt in enumerate(options):
            col = cols[idx % 4]
            label = opt.replace("-", " ").title()
            check_key = f"{key_prefix}_{title}_{opt}"
            with col:
                checked = st.checkbox(label, key=check_key, value=(opt in ss[selected_key]), disabled=disabled)
            if checked:
                selected.append(opt)
        ss[selected_key] = selected

def three_columns(tab: str, lists_3: list[list[str]], disabled=False):
    cols = st.columns([1.4, 1, 3.6])  # Adjust widths as desired
    for i, exp_title in enumerate(EXP_TITLES):
        with cols[i]:
            options = lists_3[i]
            expander_with_checkboxes(exp_title, tab, options, disabled=disabled)

def sql_list(values):
    return ', '.join(f"'{v}'" for v in values)

def run_df(sql: str, **params) -> pd.DataFrame:
    # Uses ENGINE imported at top of Layout.py
    with ENGINE.connect() as conn:  # ENGINE comes from stDBProcess.py
        return pd.read_sql_query(text(sql), conn, params=params)
    
def generate_sql_query(table_name, filters):
    base_query = f"SELECT * FROM {table_name}"
    if filters:
        where_clause = " WHERE " + " AND ".join(filters)
        return base_query + where_clause
    return base_query
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

def FilterTabs():
    tabs = ["Insurance", "Transaction", "User"]
    tabs_objs = st.tabs(tabs)

    # Automatically detect and lock tab if any selections exist
    if ss.tab_locked is None:
        for tab in tabs:
            if any(ss.get(f"{tab}_{exp}_selected") for exp in EXP_TITLES):
                ss.tab_locked = tab
                break

    table_map = {
        "Insurance": (INSURANCE, "agg_ins"),
        "Transaction": (TRANSACTION, "agg_trans"),
        "User": (USER, "agg_user"),
    }

    for idx, tab_name in enumerate(tabs):
        disabled = ss.tab_locked is not None and ss.tab_locked != tab_name
        with tabs_objs[idx]:
            if disabled:
                st.warning(f"The '{tab_name}' tab is disabled. Clear filters in '{ss.tab_locked}' to enable.")

            lists_3, table_name = table_map[tab_name]
            three_columns(tab_name, lists_3, disabled=disabled)

            # Prepare filters for SQL
            filters = []
            for exp_title in EXP_TITLES:
                selected = ss.get(f"{tab_name}_{exp_title}_selected", [])
                if selected:
                    colname = exp_title.lower()  # year, quarterly, state
                    # special fix for Quarterly column name if needed
                    colname = "quarter" if exp_title == "Quarterly" else colname
                    filters.append(f"{colname} IN ({sql_list(selected)})")

            QueryTab = st.columns([5,1])
            with QueryTab[0]:
                st.markdown("**SQL Query:**")
                if ss.tab_locked is not None and ss.tab_locked != tab_name:
                    st.write(f"Clear all filters in '{ss.tab_locked}' tab")
                elif ss.tab_locked is not None:
                    st.write(generate_sql_query(table_name, filters))
                else:
                    st.write("No filters applied.")
            # Clear button
            with QueryTab[1]:
                if st.button(f"Clear {tab_name}"):
                    for exp_title in EXP_TITLES:
                        ss[f"{tab_name}_{exp_title}_selected"] = []
                    if ss.tab_locked == tab_name:
                        ss.tab_locked = None
                    st.success("Selections cleared.")
            
#--------------------------------------------------First Graph--------------------------------------------------#

            if ss.tab_locked is None and table_name == "agg_ins":
                st.markdown("---")
                st.markdown("### PhonePe Insurance - Insights")
                cols = st.columns([1.5, 1.5 ,3])
                with cols[0]:
                    Query = f"Select year, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from {table_name} where state is null  GROUP BY year order by year"
                    df_year = run_df(Query)
                    df_year = df_year.rename(columns={"year": "x"})
                    bar_line_combo(df_year, bar_col="payment_amount", line_col="payment_count", title="Insurance Details by Year", x_title="Year", y1_title="Payment Amount", y2_title="Payment Count")
                    
                with cols[1]:
                    Query = f"Select quarter, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from {table_name} where state is null  GROUP BY quarter order by quarter"
                    df_quarter = run_df(Query)
                    df_quarter = df_quarter.rename(columns={"quarter": "x"})
                    bar_line_combo(df_quarter, bar_col="payment_amount", line_col="payment_count", title="Insurance Details by Quarter", x_title="Quarter", y1_title="Payment Amount", y2_title="Payment Count")
                    
                with cols[2]:
                    Query = f"Select state, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from {table_name} where state is not null GROUP BY state order by (payment_count + payment_amount) DESC LIMIT 18"
                    df_state = run_df(Query)
                    df_state = df_state.sort_values(by=["payment_amount"], ascending=False)
                    df_state = df_state.rename(columns={"state": "x"})
                    bar_line_combo(df_state, bar_col="payment_amount", line_col="payment_count", title="Top 18 Insurance Details by State", x_title="State", y1_title="Payment Amount", y2_title="Payment Count")
                st.markdown("---")
    #-----------------------------------------------------------------------------------------------------------------------                
                st.markdown("### Top 10 Participants Insights")
                cols = st.columns([2, 2 ,2])
                with cols[0]:
                    Query = f"SELECT DISTINCT state_entity, count(*) as Count, SUM(state_metric_count) as Total_Count, SUM(state_metric_amount) as Total_Amount from top_ins WHERE state_entity IS NOT null and state is null GROUP BY state_entity ORDER BY count(*) DESC, (SUM(state_metric_count) + SUM(state_metric_amount)) DESC;"
                    df_year = run_df(Query)
                    grouped_bar_line_share_combo(
                        df=df_year,
                        x_col="state_entity",
                        bar1_col="Total_Count",
                        bar2_col="Total_Amount",
                        line_col="Count",
                        title="State Insights",
                        x_title="State",
                        height=460,   # adjust as you like
                    )

                with cols[1]:
                    Query = f"SELECT DISTINCT district_entity, count(*) as Count, SUM(district_metric_count) as Total_Count, SUM(district_metric_amount) as Total_Amount from top_ins WHERE state_entity IS NOT null and state is null GROUP BY district_entity ORDER BY count(*) DESC, (SUM(district_metric_count) + SUM(district_metric_amount)) DESC;"
                    df_year = run_df(Query)
                    grouped_bar_line_share_combo(
                        df=df_year,
                        x_col="district_entity",
                        bar1_col="Total_Count",
                        bar2_col="Total_Amount",
                        line_col="Count",
                        title="District Insights",
                        x_title="District",
                        height=460,   # adjust as you like
                    )

                with cols[2]:
                    Query = f"SELECT DISTINCT pincode_entity, count(*) as Count, SUM(pincode_metric_count) as Total_Count, SUM(pincode_metric_amount) as Total_Amount from top_ins WHERE state_entity IS NOT null and state is null GROUP BY pincode_entity ORDER BY count(*) DESC, (SUM(pincode_metric_count) + SUM(pincode_metric_amount)) DESC;"
                    df_year = run_df(Query)
                    grouped_bar_line_share_combo(
                        df=df_year,
                        x_col="pincode_entity",
                        bar1_col="Total_Count",
                        bar2_col="Total_Amount",
                        line_col="Count",
                        title="Pincode Insights",
                        x_title="Pincode",
                        height=460,   # adjust as you like
                    )
                st.markdown("---")
    #-----------------------------------------------------------------------------------------------------------------------                
                st.markdown("### Map Insights")
                cols = st.columns([3, 3])
                with cols[0]:
                    state_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                    state_geojson_data = requests.get(state_geojson_url).json()

                    on = st.toggle("Metric Count")
                    if on:
                        st.write("Feature activated!")
                        Query = "SELECT location_name as state, SUM(metric_count) as Count FROM `map_ins_hover` WHERE state is null and location_name is not null GROUP BY location_name"
                        df = run_df(Query)
                        df['state'] = df['state'].str.strip().str.title()
                        fig = px.choropleth(
                            data_frame=df,
                            geojson=state_geojson_data,
                            featureidkey="properties.ST_NM",
                            locations="state",
                            color="Count",  # <- use Count here
                            color_continuous_scale="Viridis",
                            projection="mercator",
                            hover_name="state",
                            labels={"Count": "Count"},
                        )
                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, title_text="India States Choropleth Map")
                        st.title("India Map Visualization")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.write("Feature deactivated!")
                        Query = "SELECT location_name as state, SUM(metric_amount) as Amount FROM `map_ins_hover` WHERE state is null and location_name is not null GROUP BY location_name"
                        df = run_df(Query)
                        df['state'] = df['state'].str.strip().str.title()
                        fig = px.choropleth(
                            data_frame=df,
                            geojson=state_geojson_data,
                            featureidkey="properties.ST_NM",
                            locations="state",
                            color="Amount",  # <- use Amount here
                            color_continuous_scale="Viridis",
                            projection="mercator",
                            hover_name="state",
                            labels={"Amount": "Amount"},
                        )
                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, title_text="India States Choropleth Map")
                        st.title("India Map Visualization")
                        st.plotly_chart(fig, use_container_width=True)
                with cols[1]:
                    DISTRICTS_PATH = Path("src/india-districts-2019-734.json")
                    state_geojson_data = requests.get(state_geojson_url).json()
                    on = st.toggle("Metric Count")

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
                    # --- 5) Draw the Plotly choropleth ---
                    if on:
                        st.write("Feature activated!")
                        Query = "SELECT location_name as state, SUM(metric_count) as Count FROM `map_ins_hover` WHERE state is null and location_name is not null GROUP BY location_name"
                        df = run_df(Query)
                        fig = px.choropleth(
                            data_frame=df,
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
            elif ss.tab_locked is None and table_name == "agg_trans":
                st.markdown("---")
                st.markdown("### PhonePe Transaction - Insights")
                cols = st.columns([1.5, 1.5, 1, 2])
                with cols[0]:
                    Query = f"Select year, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from {table_name} where state is null GROUP BY year order by year"
                    df_year = run_df(Query)
                    df_year = df_year.rename(columns={"year": "x"})
                    bar_line_combo(df_year, bar_col="payment_amount", line_col="payment_count", title="Transaction Details by Year", x_title="Year", y1_title="Payment Amount", y2_title="Payment Count", bar_scale="T", line_scale="B")
                    
                with cols[1]:
                    Query = f"Select quarter, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from {table_name} where state is null GROUP BY quarter order by quarter"
                    df_quarter = run_df(Query)
                    df_quarter = df_quarter.rename(columns={"quarter": "x"})
                    bar_line_combo(df_quarter, bar_col="payment_amount", line_col="payment_count", title="Transaction Details by Quarter", x_title="Quarter", y1_title="Payment Amount", y2_title="Payment Count", bar_scale="T", line_scale="B")
                    
                with cols[2]:
                    Query = f"""
                        SELECT transaction_name,
                            SUM(payment_count) AS payment_count,
                            SUM(payment_amount) AS payment_amount
                        FROM {table_name}
                        WHERE state IS NULL
                        GROUP BY transaction_name
                        ORDER BY SUM(payment_amount) DESC
                    """
                    df_transaction = run_df(Query).rename(columns={"transaction_name": "x"})
                    order = df_transaction["x"].tolist()
                    df_transaction["x"] = pd.Categorical(df_transaction["x"], categories=order, ordered=True)
                    bar_line_combo(
                        df_transaction,
                        bar_col="payment_amount",
                        line_col="payment_count",
                        title="Transaction Details by Transaction Name",
                        x_title="Transaction Name",
                        y1_title="Payment Amount",
                        y2_title="Payment Count",
                        x_order=order,           # <-- pass it in
                        bar_scale="T", line_scale="B"
                    )
                with cols[3]:
                    Query = f"Select state, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from {table_name} where state is not null GROUP BY state order by (payment_count + payment_amount) DESC LIMIT 10"
                    df_state = run_df(Query)
                    df_state = df_state.sort_values(by=["payment_amount"], ascending=False)
                    df_state = df_state.rename(columns={"state": "x"})
                    bar_line_combo(df_state, bar_col="payment_amount", line_col="payment_count", title="Top 10 Transaction Details by State", x_title="State", y1_title="Payment Amount", y2_title="Payment Count", bar_scale="T", line_scale="B")
                st.markdown("---")
    #-----------------------------------------------------------------------------------------------------------------------                
                st.markdown("### Top 10 Participants Insights")
                cols = st.columns([2, 2 ,2])
                with cols[0]:
                    Query = f"SELECT DISTINCT state_entity, count(*) as Count, SUM(state_metric_count) as Total_Count, SUM(state_metric_amount) as Total_Amount from top_trans WHERE state_entity IS NOT null and state is null GROUP BY state_entity ORDER BY count(*) DESC, (SUM(state_metric_count) + SUM(state_metric_amount)) DESC;"
                    df_year = run_df(Query)
                    grouped_bar_line_share_combo(
                        df=df_year,
                        x_col="state_entity",
                        bar1_col="Total_Count",
                        bar2_col="Total_Amount",
                        line_col="Count",
                        title="State Insights",
                        x_title="State",
                        height=460,   # adjust as you like
                    )

                with cols[1]:
                    Query = f"SELECT DISTINCT district_entity, count(*) as Count, SUM(district_metric_count) as Total_Count, SUM(district_metric_amount) as Total_Amount from top_trans WHERE state_entity IS NOT null and state is null GROUP BY district_entity ORDER BY count(*) DESC, (SUM(district_metric_count) + SUM(district_metric_amount)) DESC;"
                    df_year = run_df(Query)
                    grouped_bar_line_share_combo(
                        df=df_year,
                        x_col="district_entity",
                        bar1_col="Total_Count",
                        bar2_col="Total_Amount",
                        line_col="Count",
                        title="District Insights",
                        x_title="District",
                        height=460,   # adjust as you like
                    )

                with cols[2]:
                    Query = f"SELECT DISTINCT pincode_entity, count(*) as Count, SUM(pincode_metric_count) as Total_Count, SUM(pincode_metric_amount) as Total_Amount from top_trans WHERE state_entity IS NOT null and state is null GROUP BY pincode_entity ORDER BY count(*) DESC, (SUM(pincode_metric_count) + SUM(pincode_metric_amount)) DESC;"
                    df_year = run_df(Query)
                    grouped_bar_line_share_combo(
                        df=df_year,
                        x_col="pincode_entity",
                        bar1_col="Total_Count",
                        bar2_col="Total_Amount",
                        line_col="Count",
                        title="Pincode Insights",
                        x_title="Pincode",
                        height=460,   # adjust as you like
                    )
                st.markdown("---")
            elif ss.tab_locked is None and table_name == "agg_user":
                st.markdown("---")
                st.markdown("### PhonePe User - Insights")
                cols = st.columns([1.5, 1.5 ,3])
                with cols[0]:
                    Query = f"Select year, Sum(registered_users) as registered_users, Sum(app_opens) as app_opens from {table_name} where state is null group by year order by year"
                    df_year = run_df(Query)
                    df_year = df_year.rename(columns={"year": "x"})
                    bar_line_combo(df_year, bar_col="app_opens", line_col="registered_users", title="Insurance by Year", x_title="Year", y1_title="Amount", y2_title="Count", bar_scale="M", line_scale="M")
                    
                with cols[1]:
                    Query = f"Select quarter, Sum(registered_users) as registered_users, Sum(app_opens) as app_opens from {table_name} where state is null group by quarter order by quarter"
                    df_quarter = run_df(Query)
                    df_quarter = df_quarter.rename(columns={"quarter": "x"})
                    bar_line_combo(df_quarter, bar_col="app_opens", line_col="registered_users", title="Insurance by Quarter", x_title="Quarter", y1_title="Amount", y2_title="Count", bar_scale="B", line_scale="B")
                    
                with cols[2]:
                    Query = f"Select state, Sum(registered_users) as registered_users, Sum(app_opens) as app_opens from {table_name} where state is not null group by state order by (registered_users + app_opens  ) DESC LIMIT 18"
                    df_state = run_df(Query)
                    df_state = df_state.rename(columns={"state": "x"})
                    order = df_state["x"].tolist()
                    df_state["x"] = pd.Categorical(df_state["x"], categories=order, ordered=True)
                    bar_line_combo(df_state, bar_col="app_opens", line_col="registered_users", title="Top 18 Insurance by State", x_title="State", y1_title="Amount", y2_title="Count", bar_scale="B", line_scale="B")
                st.markdown("---")
    #-----------------------------------------------------------------------------------------------------------------------                
                st.markdown("### Top 10 Participants Insights")
                cols = st.columns([2, 2 ,2])
                with cols[0]:
                    Query = f"SELECT DISTINCT state_name, count(*) as Count, SUM(state_registered_users) as State_Registered_Users from top_user WHERE state_name IS NOT null and state is null GROUP BY state_name ORDER BY count(*) DESC, state_registered_users DESC;"
                    df_year = run_df(Query)
                    bar_line_dynamic_scale(
                        df=df_year,
                        x_col="state_name",
                        bar_col="State_Registered_Users",
                        line_col="Count",
                        title="Total Amount and Count by State",
                        x_title="Total Registered Users by State",
                        bar_title="State Registered Users",
                        line_title="Count",
                    )

                with cols[1]:
                    Query = f"SELECT DISTINCT district_name, count(*) as Count, SUM(state_registered_users) as State_Registered_Users from top_user WHERE district_name IS NOT null and state is null GROUP BY district_name ORDER BY count(*) DESC, state_registered_users DESC;"
                    df_year = run_df(Query)
                    bar_line_dynamic_scale(
                        df=df_year,
                        x_col="district_name",
                        bar_col="State_Registered_Users",
                        line_col="Count",
                        title="Total Amount and Count by District",
                        x_title="Total Registered Users by District",
                        bar_title="District Registered Users",
                        line_title="Count",
                    )
                with cols[2]:
                    Query = f"SELECT DISTINCT pincode, count(*) as Count, SUM(pincode_registered_users) as `Pincode Registered Users` from top_user WHERE pincode IS NOT null and state is null GROUP BY pincode ORDER BY count(*) DESC, pincode_registered_users DESC;"
                    df_year = run_df(Query)
                    bar_line_dynamic_scale(
                        df=df_year,
                        x_col="pincode",
                        bar_col="Pincode Registered Users",
                        line_col="Count",
                        title="Total Amount and Count by Pincode",
                        x_title="Total Registered Users by Pincode",
                        bar_title="Pincode Registered Users",
                        line_title="Count",
                    )
                st.markdown("---")