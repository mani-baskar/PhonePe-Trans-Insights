import streamlit as st
from StFiles.stDBProcess import get_lists, ENGINE, run_df
from StFiles.stGraph import wide_bar, bar_line_combo, grouped_bar_line_share_combo, bar_line_dynamic_scale, get_geojson, plot_choropleth, clean_strings, load_geojson_from_any, get_district_key, normalize_state_name
from pathlib import Path
import pandas as pd
ss = st.session_state
EXP_TITLES = ["Year", "Quarterly", "State"]

st.set_page_config(
    page_title="PhonePe Transaction Insights",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def NonFilterPhonePeInsurance(table_name):
    st.markdown("---")
    st.markdown("### Insurance — National Overview (No Filters)")
    cols = st.columns([1.5, 1.5 ,3])
    with cols[0]:
        Query = f"Select year, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from {table_name} where state is null  GROUP BY year order by year"
        df_year = run_df(Query)
        df_year = df_year.rename(columns={"year": "x"})
        bar_line_combo(
            df_year,
            bar_col="payment_amount",
            line_col="payment_count",
            title="Yearly Insurance: Amount & Transactions",
            x_title="Year",
            y1_title="Total Amount (₹)",
            y2_title="Total Transactions"
        )
        
    with cols[1]:
        Query = f"Select quarter, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from {table_name} where state is null  GROUP BY quarter order by quarter"
        df_quarter = run_df(Query)
        df_quarter = df_quarter.rename(columns={"quarter": "x"})
        bar_line_combo(
            df_quarter,
            bar_col="payment_amount",
            line_col="payment_count",
            title="Quarterly Insurance: Amount & Transactions",
            x_title="Quarter (Q1–Q4)",
            y1_title="Total Amount (₹)",
            y2_title="Total Transactions"
        )
        
    with cols[2]:
        Query = f"Select state, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from {table_name} where state is not null GROUP BY state order by (payment_count + payment_amount) DESC LIMIT 18"
        df_state = run_df(Query)
        df_state = df_state.sort_values(by=["payment_amount"], ascending=False)
        df_state = df_state.rename(columns={"state": "x"})
        bar_line_combo(
            df_state,
            bar_col="payment_amount",
            line_col="payment_count",
            title="Top 18 States by Insurance Activity",
            x_title="State",
            y1_title="Total Amount (₹)",
            y2_title="Total Transactions"
        )
    st.markdown("---")
#-----------------------------------------------------------------------------------------------------------------------                

def NonFilterTop10Insight(table_name):
    st.markdown("### Top 10 Entities — Insurance")
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
            title="Top 10 by State Entity",
            x_title="State",
            bar1_title="Total Transactions",
            bar2_title="Total Amount (₹)",
            line_title="Occurrences",
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
            title="Top 10 by District Entity",
            x_title="District",
            bar1_title="Total Transactions",
            bar2_title="Total Amount (₹)",
            line_title="Occurrences",
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
            title="Top 10 by Pincode",
            x_title="Pincode",
            bar1_title="Total Transactions",
            bar2_title="Total Amount (₹)",
            line_title="Occurrences",
            height=460,   # adjust as you like
        )
    st.markdown("---")
#-----------------------------------------------------------------------------------------------------------------------                

def InsNonFilterTabs(table_name):
    NonFilterPhonePeInsurance(table_name)
    NonFilterTop10Insight(table_name)
    st.markdown("### Insurance Heatmaps")
    cols = st.columns([3, 3])

    with cols[0]:
        # States map
        state_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        state_geojson = get_geojson(state_geojson_url)
        metric_count_on = st.toggle("Show Insurance Count Instead of Amount (States)")
        if metric_count_on:
            query = "SELECT location_name AS state, SUM(metric_count) AS metric FROM `map_ins_hover` WHERE state IS NULL AND location_name IS NOT NULL GROUP BY location_name"
            label_name = "Total Transactions"
            color_col = "metric"
            map_title = "States Heatmap — Insurance (Count)"
        else:
            query = "SELECT location_name AS state, SUM(metric_amount) AS metric FROM `map_ins_hover` WHERE state IS NULL AND location_name IS NOT NULL GROUP BY location_name"
            label_name = "Total Amount (₹)"
            color_col = "metric"
            map_title = "States Heatmap — Insurance (Amount)"

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
        # Assume you have a function called load_geojson_from_any (in your original code)
        geojson_data, prop_keys = load_geojson_from_any(Path(DISTRICTS_PATH))
        district_key = get_district_key(prop_keys)
        if not district_key:
            st.error(f"Couldn't find a district name column in the GeoJSON properties. Available keys: {sorted(list(prop_keys))[:20]}")
            st.stop()
        DistrictMatch = pd.read_csv("Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\District Match.csv")
        district_metric_count_on = st.toggle("Show Insurance Count Instead of Amount (Districts)")
        if district_metric_count_on:
            sql_metric_col = "SUM(metric_count) AS metric"
            label_name = "Total Transactions"
            map_title = "Districts Heatmap — Insurance (Count)"
        else:
            sql_metric_col = "SUM(metric_amount) AS metric"
            label_name = "Total Amount (₹)"
            map_title = "Districts Heatmap — Insurance (Amount)"

        query = f"""
            SELECT state, TRIM(REPLACE(location_name, 'district', '')) AS district, {sql_metric_col}
            FROM `map_ins_hover`
            WHERE state IS NOT NULL AND location_name IS NOT NULL
            GROUP BY state, TRIM(REPLACE(location_name, 'district', ''))
            ORDER BY metric DESC;
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
            color_col="metric",
            featureidkey=f"properties.{district_key}",
            title=map_title,
            label_name=label_name
        )

def FilterPhonePeInsurance(Query):
    if Query and "State IN" in Query:
        StateIsNull = Query
        StateNotNull = Query
    else:
        StateIsNull = Query + " AND state IS NOT NULL"
        StateNotNull = Query + " AND state IS NOT NULL"

    st.markdown("---")
    st.markdown("### Insurance — Filtered Overview")
    cols = st.columns([1.5, 1.5 ,3])
    with cols[0]:
        Query = f"Select year, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from agg_ins {StateIsNull} GROUP BY year order by year"
        df_year = run_df(Query)
        df_year = df_year.rename(columns={"year": "x"})
        st.write(Query)
        bar_line_combo(
            df_year,
            bar_col="payment_amount",
            line_col="payment_count",
            title="Yearly Insurance: Amount & Transactions",
            x_title="Year",
            y1_title="Total Amount (₹)",
            y2_title="Total Transactions"
        )
        
    with cols[1]:
        Query = f"Select quarter, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from agg_ins {StateIsNull} GROUP BY quarter order by quarter"
        df_quarter = run_df(Query)
        df_quarter = df_quarter.rename(columns={"quarter": "x"})
        st.write(Query)
        bar_line_combo(
            df_quarter,
            bar_col="payment_amount",
            line_col="payment_count",
            title="Quarterly Insurance: Amount & Transactions",
            x_title="Quarter (Q1–Q4)",
            y1_title="Total Amount (₹)",
            y2_title="Total Transactions"
        )
        
    with cols[2]:
        Query = f"Select state, Sum(payment_count) as payment_count, Sum(payment_amount) as payment_amount from agg_ins {StateNotNull} GROUP BY state order by (payment_count + payment_amount) DESC LIMIT 18"
        df_state = run_df(Query)
        df_state = df_state.sort_values(by=["payment_amount"], ascending=False)
        df_state = df_state.rename(columns={"state": "x"})
        st.write(Query)
        bar_line_combo(
            df_state,
            bar_col="payment_amount",
            line_col="payment_count",
            title="Top 18 States by Insurance Activity",
            x_title="State",
            y1_title="Total Amount (₹)",
            y2_title="Total Transactions"
        )
        
    st.markdown("---")

def FilterTop10Insight(Query):
    if Query and "state IN" in Query:
        RQuery = Query.replace("-", " ")
        RQuery = RQuery.replace("state IN ", "state_entity IN ")
        StateQuery = f"""
        SELECT  
            state_entity,
            Count(*)                 AS Count,
            Sum(state_metric_count)  AS Total_Count,
            Sum(state_metric_amount) AS Total_Amount
        FROM   top_ins
        {RQuery}       
        GROUP  BY state_entity
        ORDER  BY Count(*) DESC,
                ( Sum(state_metric_count)
                + Sum(state_metric_amount) ) DESC; 
        """
        QuarterQuery = f"""
        SELECT
            district_entity,
            COUNT(*) AS Count,
            Sum(district_metric_count)  AS Total_Count,
            Sum(district_metric_amount) AS Total_Amount
        FROM   top_ins
        {Query}
        GROUP BY state,district_entity
        ORDER BY Count(*) DESC,
                ( Sum(district_metric_count)
                + Sum(district_metric_amount) ) DESC; 
        """
        PincodeQuery = f"""
        SELECT
            pincode_entity,
            COUNT(*) AS Count,
            Sum(district_metric_count)  AS Total_Count,
            Sum(district_metric_amount) AS Total_Amount
        FROM   top_ins
        {Query}
        GROUP BY state,pincode_entity
        ORDER BY Count(*) DESC,
                ( Sum(district_metric_count)
                + Sum(district_metric_amount) ) DESC;
        """
    else:
        StateQuery = f"SELECT DISTINCT state_entity, count(*) as Count, SUM(state_metric_count) as Total_Count, SUM(state_metric_amount) as Total_Amount from top_ins {Query} AND state_entity IS NOT null and state is null GROUP BY state_entity ORDER BY count(*) DESC, (SUM(state_metric_count) + SUM(state_metric_amount)) DESC;"
        QuarterQuery = f"SELECT DISTINCT district_entity, count(*) as Count, SUM(district_metric_count) as Total_Count, SUM(district_metric_amount) as Total_Amount from top_ins {Query} AND state_entity IS NOT null and state is null GROUP BY district_entity ORDER BY count(*) DESC, (SUM(district_metric_count) + SUM(district_metric_amount)) DESC;"
        PincodeQuery = f"SELECT DISTINCT pincode_entity, count(*) as Count, SUM(pincode_metric_count) as Total_Count, SUM(pincode_metric_amount) as Total_Amount from top_ins {Query} AND state_entity IS NOT null and state is null GROUP BY pincode_entity ORDER BY count(*) DESC, (SUM(pincode_metric_count) + SUM(pincode_metric_amount)) DESC;"

    st.markdown("### Top 10 Entities — Filtered")
    cols = st.columns([2, 2 ,2])
    with cols[0]:
        df = run_df(StateQuery)
        st.write(StateQuery)
        grouped_bar_line_share_combo(
            df=df,
            x_col="state_entity",
            bar1_col="Total_Count",
            bar2_col="Total_Amount",
            line_col="Count",
            title="Top 10 by State Entity",
            x_title="State",
            bar1_title="Total Transactions",
            bar2_title="Total Amount (₹)",
            line_title="Occurrences",
            height=460,   # adjust as you like
        )
        
    with cols[1]:
        df = run_df(QuarterQuery)
        st.write(QuarterQuery)
        grouped_bar_line_share_combo(
            df=df,
            x_col="district_entity",
            bar1_col="Total_Count",
            bar2_col="Total_Amount",
            line_col="Count",
            title="Top 10 by District Entity",
            x_title="District",
            bar1_title="Total Transactions",
            bar2_title="Total Amount (₹)",
            line_title="Occurrences",
            height=460,   # adjust as you like
        )
        
    with cols[2]:
        df = run_df(PincodeQuery)
        st.write(PincodeQuery)
        grouped_bar_line_share_combo(
            df=df,
            x_col="pincode_entity",
            bar1_col="Total_Count",
            bar2_col="Total_Amount",
            line_col="Count",
            title="Top 10 by Pincode",
            x_title="Pincode",
            bar1_title="Total Transactions",
            bar2_title="Total Amount (₹)",
            line_title="Occurrences",
            height=460,   # adjust as you like
        )
        
    st.markdown("---")

def FilterMapInsightsAmount(Query):
    if Query and "state IN" in Query:
        StateAmountQuery = f"SELECT state, SUM(metric_amount) AS metric FROM `map_ins_hover` {Query} GROUP BY state"
        DistrictAmountQuery = f"SELECT state, TRIM(REPLACE(location_name, 'district', '')) AS district, SUM(metric_amount) AS metric FROM `map_ins_hover` {Query} GROUP BY state, TRIM(REPLACE(location_name, 'district', '')) ORDER BY metric DESC;"
    else:
        StateAmountQuery = f"SELECT location_name AS state, SUM(metric_amount) AS metric FROM `map_ins_hover` {Query} AND state IS NULL AND location_name IS NOT NULL GROUP BY location_name"
        DistrictAmountQuery = f"SELECT state, TRIM(REPLACE(location_name, 'district', '')) AS district, SUM(metric_amount) AS metric FROM `map_ins_hover` {Query} AND state IS NOT NULL AND location_name IS NOT NULL GROUP BY state, TRIM(REPLACE(location_name, 'district', '')) ORDER BY metric DESC;"
    st.markdown("### Insurance Heatmaps — Filtered (Amount)")
    cols = st.columns([3, 3])

    with cols[0]:
        # States map
        state_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        state_geojson = get_geojson(state_geojson_url)
        query = StateAmountQuery
        label_name = "Total Amount (₹)"
        color_col = "metric"

        df = run_df(query)
        df = clean_strings(df, [('state', 'title')])
        StateMatch = pd.read_csv("Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\State Match.csv")
        StateMatch = clean_strings(StateMatch, [('MYSQLState', 'title')])
        # Merge with mapping file
        df = df.merge(
            StateMatch,
            left_on=["state"],
            right_on=["MYSQLState"],
            how="left"
        )
        # Use mapped name if present
        df["state"] = df["JSON State"].fillna(df["state"])
        df = df.drop(columns=["MYSQLState", "JSON State"])
        st.write(query)
        plot_choropleth(
            df=df,
            geojson_data=state_geojson,
            location_col="state",
            color_col=color_col,
            featureidkey="properties.ST_NM",
            title="States Heatmap — Insurance (Amount)",
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
        label_name = "Total Amount (₹)"
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
        st.write(query)
        plot_choropleth(
            df=df,
            geojson_data=geojson_data,
            location_col="district",
            color_col="metric",
            featureidkey=f"properties.{district_key}",
            title="Districts Heatmap — Insurance (Amount)",
            label_name=label_name
        )

def FilterMapInsightsCount(Query):
    if Query and "state IN" in Query:
        #st.write(Query)
        StateCountQuery = f"SELECT state, SUM(metric_count) AS metric FROM `map_ins_hover` {Query} GROUP BY state"
        DistrictCountQuery = f"SELECT state, TRIM(REPLACE(location_name, 'district', '')) AS district, SUM(metric_count) AS metric FROM `map_ins_hover` {Query} GROUP BY state, TRIM(REPLACE(location_name, 'district', '')) ORDER BY metric DESC;"
    else:
        #st.write(Query)
        StateCountQuery = f"SELECT location_name AS state, SUM(metric_count) AS metric FROM `map_ins_hover` {Query} AND state IS NULL AND location_name IS NOT NULL GROUP BY location_name"
        DistrictCountQuery = f"SELECT state, TRIM(REPLACE(location_name, 'district', '')) AS district, SUM(metric_count) AS metric FROM `map_ins_hover` {Query} AND state IS NOT NULL AND location_name IS NOT NULL GROUP BY state, TRIM(REPLACE(location_name, 'district', '')) ORDER BY metric DESC;"
    st.markdown("### Insurance Heatmaps — Filtered (Count)")
    cols = st.columns([3, 3])

    with cols[0]:
        state_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        state_geojson = get_geojson(state_geojson_url)
        query = StateCountQuery
        label_name = "Total Transactions"
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
            title="States Heatmap — Insurance (Count)",
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
        label_name = "Total Transactions"
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
            title="Districts Heatmap — Insurance (Count)",
            label_name=label_name
        )

def InsFilterTabs(Query):
    FilterPhonePeInsurance(Query)
    FilterTop10Insight(Query)
    FilterMapInsightsAmount(Query)
