import streamlit as st
# from stDBProcess import get_lists, ENGINE, run_df
# from stGraph import wide_bar, bar_line_combo, grouped_bar_line_share_combo, bar_line_dynamic_scale, get_geojson, plot_choropleth, clean_strings, load_geojson_from_any, get_district_key
# from Layout import EXP_TITLES, FilterTabs
from StFiles.stDBProcess import get_lists, ENGINE, run_df
from StFiles.stGraph import wide_bar, bar_line_combo, grouped_bar_line_share_combo, bar_line_dynamic_scale, get_geojson, plot_choropleth, clean_strings, load_geojson_from_any, get_district_key
# from StFiles.Layout import EXP_TITLES, FilterTabs
from pathlib import Path
import json
import geopandas as gpd
import pandas as pd

ss = st.session_state
st.set_page_config(
    page_title="PhonePe Transaction Insights",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def Test():
    for exp_title in EXP_TITLES:
        selected_key = f"Insurance_{exp_title}_selected" if ss.tab_locked else f"Insurance_{exp_title}_selected"
        selected = ss.get(selected_key, [])
        if selected:
            st.markdown(f"**{exp_title} Selected:** {', '.join(selected)}")

def UserMain():
    Col1, Col2, Col3 = st.columns(3)
    with Col1:
        st.markdown("**Insurance Tab is Locked**")
    with Col2:
        st.markdown("**User Tab is Locked**")
    with Col3:
        st.markdown("**Transaction Tab is Locked**")

def NonFilterPhonePeUser(table_name):
    st.markdown("---")
    st.markdown("### Users — National Overview (No Filters)")
    cols = st.columns([1.5, 1.5 ,3])

    with cols[0]:
        Query = f"Select year, Sum(registered_users) as registered_users, Sum(app_opens) as app_opens from {table_name} where state is null group by year order by year"
        df_year = run_df(Query)
        df_year = df_year.rename(columns={"year": "x"})
        bar_line_combo(
            df_year,
            bar_col="app_opens",
            line_col="registered_users",
            title="Yearly Users: App Opens & Registered Users",
            x_title="Year",
            y1_title="App Opens",
            y2_title="Registered Users",
            bar_scale="M",
            line_scale="M"
        )
        
    with cols[1]:
        Query = f"Select quarter, Sum(registered_users) as registered_users, Sum(app_opens) as app_opens from {table_name} where state is null group by quarter order by quarter"
        df_quarter = run_df(Query)
        df_quarter = df_quarter.rename(columns={"quarter": "x"})
        bar_line_combo(
            df_quarter,
            bar_col="app_opens",
            line_col="registered_users",
            title="Quarterly Users: App Opens & Registered Users",
            x_title="Quarter (Q1–Q4)",
            y1_title="App Opens",
            y2_title="Registered Users",
            bar_scale="B",
            line_scale="B"
        )
        
    with cols[2]:
        Query = f"Select state, Sum(registered_users) as registered_users, Sum(app_opens) as app_opens from {table_name} where state is not null group by state order by (registered_users + app_opens  ) DESC LIMIT 18"
        df_state = run_df(Query)
        df_state = df_state.rename(columns={"state": "x"})
        order = df_state["x"].tolist()
        df_state["x"] = pd.Categorical(df_state["x"], categories=order, ordered=True)
        bar_line_combo(
            df_state,
            bar_col="app_opens",
            line_col="registered_users",
            title="Top 18 States by Users",
            x_title="State",
            y1_title="App Opens",
            y2_title="Registered Users",
            bar_scale="B",
            line_scale="B"
        )
    st.markdown("---")

#----------------------------------------------------------------------------------------------------------------------- 
def NonFilterTop10Insight():
    st.markdown("### Top 10 Entities — Users")
    cols = st.columns([2, 2 ,2])

    with cols[0]:
        Query = f"SELECT DISTINCT state_name, count(*) as Count, SUM(state_registered_users) as State_Registered_Users from top_user WHERE state_name IS NOT null and state is null GROUP BY state_name ORDER BY count(*) DESC, state_registered_users DESC;"
        df_year = run_df(Query)
        bar_line_dynamic_scale(
            df=df_year,
            x_col="state_name",
            bar_col="State_Registered_Users",
            line_col="Count",
            title="Top 10 by State: Registered Users & Records",
            x_title="State",
            bar_title="Registered Users",
            line_title="Records (Count)",
        )

    with cols[1]:
        Query = f"SELECT DISTINCT district_name, count(*) as Count, SUM(state_registered_users) as State_Registered_Users from top_user WHERE district_name IS NOT null and state is null GROUP BY district_name ORDER BY count(*) DESC, state_registered_users DESC;"
        df_year = run_df(Query)
        bar_line_dynamic_scale(
            df=df_year,
            x_col="district_name",
            bar_col="State_Registered_Users",
            line_col="Count",
            title="Top 10 by District: Registered Users & Records",
            x_title="District",
            bar_title="Registered Users",
            line_title="Records (Count)",
        )

    with cols[2]:
        Query = f"SELECT DISTINCT pincode, count(*) as Count, SUM(pincode_registered_users) as `Pincode Registered Users` from top_user WHERE pincode IS NOT null and state is null GROUP BY pincode ORDER BY count(*) DESC, pincode_registered_users DESC;"
        df_year = run_df(Query)
        bar_line_dynamic_scale(
            df=df_year,
            x_col="pincode",
            bar_col="Pincode Registered Users",
            line_col="Count",
            title="Top 10 by Pincode: Registered Users & Records",
            x_title="Pincode",
            bar_title="Registered Users",
            line_title="Records (Count)",
        )
    st.markdown("---")

#-----------------------------------------------------------------------------------------------------------------------  
def UserNonFilterTabs(table_name):
    NonFilterPhonePeUser(table_name)
    NonFilterTop10Insight()
    st.markdown("### User Heatmaps")
    cols = st.columns([3, 3])

    with cols[0]:
        # States map
        state_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        state_geojson = get_geojson(state_geojson_url)

        # Toggle between App Opens and Registered Users
        metric_count_on = st.toggle("Show App Opens Instead of Registered Users (States)")
        if metric_count_on:
            query = "SELECT hover_state AS state, SUM(app_opens) AS `App Opens` FROM `map_user` WHERE state IS NULL AND hover_state IS NOT NULL GROUP BY hover_state"
            label_name = "App Opens"
            color_col = "App Opens"
            map_title = "States Heatmap — Users (App Opens)"
        else:
            query = "SELECT hover_state AS state, SUM(registered_users) AS `Registered Users` FROM `map_user` WHERE state IS NULL AND hover_state IS NOT NULL GROUP BY hover_state"
            label_name = "Registered Users"
            color_col = "Registered Users"
            map_title = "States Heatmap — Users (Registered Users)"

        df = run_df(query)
        df = clean_strings(df, [('state', 'title')])
        plot_choropleth(
            df=df,
            geojson_data=state_geojson,
            location_col="state",
            color_col=color_col,
            featureidkey="properties.ST_NM",
            title=map_title,
            label_name=label_name
        )

    with cols[1]:
        # Districts map
        DISTRICTS_PATH = "Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\india-districts-2019-734.json"   
        geojson_data, prop_keys = load_geojson_from_any(Path(DISTRICTS_PATH))
        district_key = get_district_key(prop_keys)
        if not district_key:
            st.error(f"Couldn't find a district name column in the GeoJSON properties. Available keys: {sorted(list(prop_keys))[:20]}")
            st.stop()
        DistrictMatch = pd.read_csv("Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\District Match.csv")

        district_metric_count_on = st.toggle("Show App Opens Instead of Registered Users (Districts)")
        if district_metric_count_on:
            sql_metric_col = "SUM(app_opens) AS `App Opens`"
            label_name = "App Opens"
            color_col = "App Opens"
            map_title = "Districts Heatmap — Users (App Opens)"
        else:
            sql_metric_col = "SUM(registered_users) AS `Registered Users`"
            label_name = "Registered Users"
            color_col = "Registered Users"
            map_title = "Districts Heatmap — Users (Registered Users)"

        query = f"""
            SELECT state, TRIM(REPLACE(hover_state, 'district', '')) AS district, {sql_metric_col}
            FROM `map_user`
            WHERE state IS NOT NULL AND hover_state IS NOT NULL
            GROUP BY state, TRIM(REPLACE(hover_state, 'district', ''))
            ORDER BY SUM(registered_users) DESC;
        """
        df = run_df(query)
        df = clean_strings(df, [('district', 'title'), ('state', 'lower')])
        DistrictMatch = clean_strings(DistrictMatch, [('MySQL_District', 'title'), ('District State', 'lower')])

        # Merge with mapping file
        df = df.merge(
            DistrictMatch,
            left_on=["state", "district"],
            right_on=["District State", "MySQL_District"],
            how="left"
        )
        # Use mapped name if present
        df["district"] = df["GEOJson_District"].fillna(df["district"])
        df = df.drop(columns=["MySQL_District", "GEOJson_District", "District State"])
        df.to_excel("district_data.xlsx", index=False)
        plot_choropleth(
            df=df,
            geojson_data=geojson_data,
            location_col="district",
            color_col=label_name,
            featureidkey=f"properties.{district_key}",
            title=map_title,
            label_name=label_name
        )

def FilterPhonePeUser(Query):
    if Query and "State IN" in Query:
        StateIsNull = Query
        StateNotNull = Query
    else:
        StateIsNull = Query + " AND state IS NOT NULL"
        StateNotNull = Query + " AND state IS NOT NULL"

    st.markdown("---")
    st.markdown("### Users — Filtered Overview")
    cols = st.columns([1.5, 1.5 ,3])

    with cols[0]:
        Query = f"Select year, Sum(registered_users) as registered_users, Sum(app_opens) as app_opens from agg_user {StateIsNull} GROUP BY year order by year"
        df_year = run_df(Query)
        df_year = df_year.rename(columns={"year": "x"})
        st.write(Query)
        bar_line_combo(
            df_year,
            bar_col="app_opens",
            line_col="registered_users",
            title="Yearly Users: App Opens & Registered Users",
            x_title="Year",
            y1_title="App Opens",
            y2_title="Registered Users"
        )
        

    with cols[1]:
        Query = f"Select quarter, Sum(registered_users) as registered_users, Sum(app_opens) as app_opens from agg_user {StateIsNull} GROUP BY quarter order by quarter"
        df_quarter = run_df(Query)
        df_quarter = df_quarter.rename(columns={"quarter": "x"})
        st.write(Query)
        bar_line_combo(
            df_quarter,
            bar_col="app_opens",
            line_col="registered_users",
            title="Quarterly Users: App Opens & Registered Users",
            x_title="Quarter (Q1–Q4)",
            y1_title="App Opens",
            y2_title="Registered Users"
        )
        

    with cols[2]:
        Query = f"Select state, Sum(registered_users) as registered_users, Sum(app_opens) as app_opens from agg_user {StateNotNull} GROUP BY state order by (registered_users + app_opens) DESC LIMIT 18"
        df_state = run_df(Query)
        df_state = df_state.sort_values(by=["app_opens"], ascending=False)
        df_state = df_state.rename(columns={"state": "x"})
        st.write(Query)
        bar_line_combo(
            df_state,
            bar_col="app_opens",
            line_col="registered_users",
            title="Top 18 States by Users",
            x_title="State",
            y1_title="App Opens",
            y2_title="Registered Users"
        )
        

    st.markdown("---")

def FilterTop10Insight(Query):
    if Query and "state IN" in Query:
        RQuery = Query.replace("-", " ")
        RQuery = RQuery.replace("state IN ", "state_name IN ")
        StateQuery = f"""
        SELECT  
            state_name,
            Count(*)                 AS Count,
            Sum(state_registered_users)  AS State_Registered_Users
        FROM   top_user
        {RQuery}       
        GROUP  BY state_name
        ORDER  BY Count(*) DESC,
                state_registered_users DESC; 
        """
        QuarterQuery = f"""
        SELECT
            district_name,
            COUNT(*) AS Count,
            Sum(district_registered_users)  AS District_Registered_Users
        FROM   top_user
        {Query}
        GROUP BY district_name
        ORDER BY Count(*) DESC,
                district_registered_users DESC; 
        """
        PincodeQuery = f"""
        SELECT  
            pincode as Pincode,
            Count(*) AS Count,
            Sum(pincode_registered_users) AS Pincode_Registered_Users
        FROM   top_user
        {Query}
        GROUP BY pincode
        ORDER BY Count(*) DESC,
                Pincode_Registered_Users DESC; 
        """
    else:
        StateQuery = f"SELECT state_name, count(*) as Count, SUM(state_registered_users) as State_Registered_Users from top_user {Query} AND state_name IS NOT null and state is null GROUP BY state_name ORDER BY count(*) DESC, state_registered_users DESC;"
        QuarterQuery = f"SELECT district_name, count(*) as Count, SUM(district_registered_users) as District_Registered_Users from top_user {Query} AND state_name IS NOT null and state is null GROUP BY district_name ORDER BY count(*) DESC, district_registered_users DESC;"
        PincodeQuery = f"SELECT pincode as Pincode, count(*) as Count, SUM(pincode_registered_users) as Pincode_Registered_Users from top_user {Query} AND state_name IS NOT null and state is null GROUP BY pincode ORDER BY count(*) DESC, Pincode_Registered_Users DESC;"

    st.markdown("### Top 10 Entities — Filtered (Users)")
    cols = st.columns([2, 2 ,2])

    with cols[0]:
        st.write(StateQuery)
        df = run_df(StateQuery)
        bar_line_dynamic_scale(
            df=df,
            x_col="state_name",
            bar_col="State_Registered_Users",
            line_col="Count",
            title="Top 10 by State: Registered Users & Records",
            x_title="State",
            bar_title="Registered Users",
            line_title="Records (Count)",
        )
        
    with cols[1]:
        st.write(QuarterQuery)
        df = run_df(QuarterQuery)
        bar_line_dynamic_scale(
            df=df,
            x_col="district_name",
            bar_col="District_Registered_Users",
            line_col="Count",
            title="Top 10 by District: Registered Users & Records",
            x_title="District",
            bar_title="Registered Users",
            line_title="Records (Count)",
        )

    with cols[2]:
        st.write(PincodeQuery)
        df = run_df(PincodeQuery)
        bar_line_dynamic_scale(
            df=df,
            x_col="Pincode",
            bar_col="Pincode_Registered_Users",
            line_col="Count",
            title="Top 10 by Pincode: Registered Users & Records",
            x_title="Pincode",
            bar_title="Registered Users",
            line_title="Records (Count)",
        )

def FilterMapInsightsRegister(Query):
    if Query and "state IN" in Query:
        StateAmountQuery = f"SELECT state, SUM(app_opens) AS 'metric' FROM `map_user` {Query} GROUP BY state"
        DistrictAmountQuery = f"SELECT state, TRIM(REPLACE(hover_state, 'district', '')) AS district, SUM(app_opens) AS 'metric' FROM `map_user` {Query} GROUP BY hover_state"
    else:
        StateAmountQuery = f"SELECT hover_state AS state, SUM(app_opens) AS 'metric' FROM `map_user` {Query} AND state IS NULL AND hover_state IS NOT NULL GROUP BY hover_state"
        DistrictAmountQuery = f"SELECT state, TRIM(REPLACE(hover_state, 'district', '')) AS district, SUM(app_opens) AS 'metric' FROM `map_user` {Query} AND state IS NOT NULL AND hover_state IS NOT NULL GROUP BY hover_state"

    st.markdown("### User Heatmaps — Filtered (App Opens)")
    cols = st.columns([3, 3])

    with cols[0]:
        state_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        state_geojson = get_geojson(state_geojson_url)
        query = StateAmountQuery
        label_name = "App Opens"
        color_col = "metric"
        df = run_df(query)
        st.write(query)
        df = clean_strings(df, [('state', 'title')])
        StateMatch = pd.read_csv("Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\State Match.csv")
        StateMatch = clean_strings(StateMatch, [("MYSQLState", "title")])
        df = df.merge(
            StateMatch,
            left_on=["state"],
            right_on=["MYSQLState"],
            how="left"
        )
        df["state"] = df["JSON State"].fillna(df["state"])
        df = df.drop(columns=["MYSQLState", "JSON State"])
        plot_choropleth(
            df=df,
            geojson_data=state_geojson,
            location_col="state",
            color_col=color_col,
            featureidkey="properties.ST_NM",
            title="States Heatmap — Users (App Opens)",
            label_name=label_name
        )

    with cols[1]:
        # Districts map
        DISTRICTS_PATH = "Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\india-districts-2019-734.json"   
        geojson_data, prop_keys = load_geojson_from_any(Path(DISTRICTS_PATH))
        district_key = get_district_key(prop_keys)
        if not district_key:
            st.error(f"Couldn't find a district name column in the GeoJSON properties. Available keys: {sorted(list(prop_keys))[:20]}")
            st.stop()
        DistrictMatch = pd.read_csv("Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\District Match.csv")

        query = DistrictAmountQuery
        label_name = "App Opens"
        df = run_df(query)
        st.write(query)
        df = clean_strings(df, [('district', 'title'), ('state', 'lower')])
        DistrictMatch = clean_strings(DistrictMatch, [('MySQL_District', 'title'), ('District State', 'lower')])
        df = df.merge(
            DistrictMatch,
            left_on=["state", "district"],
            right_on=["District State", "MySQL_District"],
            how="left"
        )
        df["district"] = df["GEOJson_District"].fillna(df["district"])
        df = df.drop(columns=["MySQL_District", "GEOJson_District", "District State"])
        #df.to_excel("district_data.xlsx", index=False)
        plot_choropleth(
            df=df,
            geojson_data=geojson_data,
            location_col="district",
            color_col="metric",
            featureidkey=f"properties.{district_key}",
            title="Districts Heatmap — Users (App Opens)",
            label_name=label_name
        )

def FilterMapInsightsCount(Query):
    # (Kept as-is per your code; this section uses map_trans and “Count”)
    if Query and "state IN" in Query:
        #st.write(Query)
        StateCountQuery = f"SELECT state, SUM(metric_count) AS metric FROM `map_trans` {Query} GROUP BY state"
        DistrictCountQuery = f"SELECT state, TRIM(REPLACE(location_name, 'district', '')) AS district, SUM(metric_count) AS metric FROM `map_trans` {Query} GROUP BY state, TRIM(REPLACE(location_name, 'district', '')) ORDER BY metric DESC;"
    else:
        #st.write(Query)
        StateCountQuery = f"SELECT location_name AS state, SUM(metric_count) AS metric FROM `map_trans` {Query} AND state IS NULL AND location_name IS NOT NULL GROUP BY location_name"
        DistrictCountQuery = f"SELECT state, TRIM(REPLACE(location_name, 'district', '')) AS district, SUM(metric_count) AS metric FROM `map_trans` {Query} AND state IS NOT NULL AND location_name IS NOT NULL GROUP BY state, TRIM(REPLACE(location_name, 'district', '')) ORDER BY metric DESC;"

    st.markdown("### Map Insights")
    cols = st.columns([3, 3])

    with cols[0]:
        state_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        state_geojson = get_geojson(state_geojson_url)
        query = StateCountQuery
        label_name = "Count"
        color_col = "metric"
        df = run_df(query)
        df = clean_strings(df, [('state', 'title')])
        StateMatch = pd.read_csv("Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\State Match.csv")
        StateMatch = clean_strings(StateMatch, [('MYSQLState', 'title')])
        df = df.merge(
            StateMatch,
            left_on=["state"],
            right_on=["MYSQLState"],
            how="left"
        )
        df["state"] = df["JSON State"].fillna(df["state"])
        df = df.drop(columns=["MYSQLState", "JSON State"])
        plot_choropleth(
            df=df,
            geojson_data=state_geojson,
            location_col="state",
            color_col=color_col,
            featureidkey="properties.ST_NM",
            title="India States Choropleth Map",
            label_name=label_name
        )

    with cols[1]:
        DISTRICTS_PATH = "Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\india-districts-2019-734.json"   
        geojson_data, prop_keys = load_geojson_from_any(Path(DISTRICTS_PATH))
        district_key = get_district_key(prop_keys)
        if not district_key:
            st.error(f"Couldn't find a district name column in the GeoJSON properties. Available keys: {sorted(list(prop_keys))[:20]}")
            st.stop()
        DistrictMatch = pd.read_csv("Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\District Match.csv")
        query = DistrictCountQuery
        label_name = "Count"
        df = run_df(query)
        df = clean_strings(df, [('district', 'title'), ('state', 'lower')])
        DistrictMatch = clean_strings(DistrictMatch, [('MySQL_District', 'title'), ('District State', 'lower')])
        df = df.merge(
            DistrictMatch,
            left_on=["state", "district"],
            right_on=["District State", "MySQL_District"],
            how="left"
        )
        df["district"] = df["GEOJson_District"].fillna(df["district"])
        df = df.drop(columns=["MySQL_District", "GEOJson_District", "District State"])
        df.to_excel("district_data.xlsx", index=False)
        plot_choropleth(
            df=df,
            geojson_data=geojson_data,
            location_col="district",
            color_col="metric",
            featureidkey=f"properties.{district_key}",
            title="India Districts Choropleth Map",
            label_name=label_name
        )

def UserFilterTabs(Query):
    FilterPhonePeUser(Query)
    FilterTop10Insight(Query)
    FilterMapInsightsRegister(Query)
