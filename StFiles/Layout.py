import streamlit as st
# from stDBProcess import get_lists, ENGINE, run_df
# from stGraph import bar_line_combo, grouped_bar_line_share_combo, bar_line_dynamic_scale, get_geojson, plot_choropleth, clean_strings, load_geojson_from_any, get_district_key
from StFiles.stDBProcess import get_lists, ENGINE, run_df
from StFiles.stGraph import bar_line_combo, grouped_bar_line_share_combo, bar_line_dynamic_scale, get_geojson, plot_choropleth, clean_strings, load_geojson_from_any, get_district_key
from StFiles.Insurance import InsNonFilterTabs, InsFilterTabs, FilterMapInsightsAmount, FilterMapInsightsCount
from StFiles.Transaction import TransNonFilterTabs, TransFilterTabs
from StFiles.User import UserNonFilterTabs, UserFilterTabs
import pandas as pd
from sqlalchemy import text
import requests
import plotly.express as px
from pathlib import Path
import json
import geopandas as gpd
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

def generate_sql_query(table_name, filters):
    base_query = f"SELECT * FROM {table_name}"
    if filters:
        where_clause = " WHERE " + " AND ".join(filters)
        return base_query + where_clause
    return base_query

def conditionQuery(filters):
    if filters:
        where_clause = " WHERE " + " AND ".join(filters)
        return  where_clause
    return "No Query"

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
                    if exp_title == "Quarterly":
                        selected = [s.replace("Q", "") for s in selected]
                    filters.append(f"{colname} IN ({sql_list(selected)})")

            QueryTab = st.columns([5, 1])  # Now three columns

            with QueryTab[0]:
                st.markdown("**SQL Query:**")
                if ss.tab_locked is not None and ss.tab_locked != tab_name:
                    st.write(f"Clear all filters in '{ss.tab_locked}' tab")
                elif ss.tab_locked is not None:
                    Query = generate_sql_query(table_name, filters)
                    st.write(Query)
                else:
                    st.write("No filters applied.")

            with QueryTab[1]:
                if st.button(f"Clear {tab_name}"):
                    for exp_title in EXP_TITLES:
                        ss[f"{tab_name}_{exp_title}_selected"] = []
                    if ss.tab_locked == tab_name:
                        ss.tab_locked = None
                    st.success("Selections cleared.")
                    st.rerun()

            # with QueryTab[2]:
            #     if st.button(f"{tab_name} Process"):
            #         if tab_name == ss.tab_locked:
            #             st.write(f"Processing {tab_name} with current filters.")
            #             Query = conditionQuery(filters)
            #             st.write(Query)
            #InsFilterTabs(Query)
                        #st.rerun()

            
#--------------------------------------------------First Graph--------------------------------------------------#

            if st.button(f"{tab_name} Process"):
                if tab_name == ss.tab_locked:
                    st.write(f"Processing {tab_name} with current filters.")
                    Query = conditionQuery(filters)
                    if Query != "No Query" and table_name == "agg_ins":
                        InsFilterTabs(Query)
                    elif Query != "No Query" and table_name == "agg_trans":
                        TransFilterTabs(Query)
                    elif Query != "No Query" and table_name == "agg_user":
                        UserFilterTabs(Query)

            if ss.tab_locked is None and table_name == "agg_ins":
                InsNonFilterTabs(table_name)
            elif ss.tab_locked is None and table_name == "agg_trans":
                TransNonFilterTabs(table_name)
            elif ss.tab_locked is None and table_name == "agg_user":
                UserNonFilterTabs(table_name)

            # if ss.tab_locked is not None and ss.tab_locked == "Insurance":
            #     st.markdown("**Insurance Tab is Locked**")
            #     Query = conditionQuery(filters)
            #     if Query != "No Query":
            #         InsFilterTabs(Query)
            #     else:
            #         Query = "No filters applied."
            #     #st.markdown(Query)
            # elif ss.tab_locked is not None and ss.tab_locked == "Transaction":
            #     st.markdown("**Transaction Tab is Locked**")
            #     st.write(Query)
            # elif ss.tab_locked is not None and ss.tab_locked == "User":
            #     st.markdown("**User Tab is Locked**")
            #     st.markdown(Query)