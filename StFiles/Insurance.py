import streamlit as st
ss = st.session_state
from StFiles.Layout import EXP_TITLES, FilterTabs

def Test():
    for exp_title in EXP_TITLES:
        selected_key = f"Insurance_{exp_title}_selected" if ss.tab_locked else f"Insurance_{exp_title}_selected"
        selected = ss.get(selected_key, [])
        if selected:
            st.markdown(f"**{exp_title} Selected:** {', '.join(selected)}")