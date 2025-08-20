import streamlit as st
ss = st.session_state
from StFiles.Layout import EXP_TITLES, FilterTabs
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

