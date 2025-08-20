import streamlit as st
from StFiles.MyProfile import myProfile
from StFiles.stDBProcess import get_lists
from StFiles.Layout import EXP_TITLES, FilterTabs
import matplotlib.pyplot as plt
from StFiles.Insurance import Test

st.set_page_config(
    page_title="PhonePe Transaction Insights",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def plot_bar_line(df, x_col, bar_y_col, line_y_col, title=""):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # Bar chart
    ax1.bar(df[x_col], df[bar_y_col], color='skyblue', label=bar_y_col)
    # Line chart
    ax2.plot(df[x_col], df[line_y_col], color='red', marker='o', label=line_y_col)
    
    ax1.set_xlabel(x_col)
    ax1.set_ylabel(bar_y_col, color='skyblue')
    ax2.set_ylabel(line_y_col, color='red')

    plt.title(title)
    fig.tight_layout()
    st.pyplot(fig)

def basic_summary(df, x_col, bar_y_col, line_y_col):
    x_max_value = df[x_col].iloc[df[bar_y_col].idxmax()]
    bar_max = df[bar_y_col].max()
    line_mean = df[line_y_col].mean()
    bar_var = df[bar_y_col].var()
    mean_of_variance = bar_var # Usually "mean of variance" isn't meaningful; just showing variance.

    summary = (f"- **{x_col}** with max `{bar_y_col}`: `{x_max_value}` (**{bar_max:.2f}**)\n"
               f"- Mean of `{line_y_col}`: **{line_mean:.2f}**\n"
               f"- Variance of `{bar_y_col}`: **{bar_var:.2f}**")
    return summary

with st.sidebar:
    myProfile()
    st.markdown("---")
ss = st.session_state
st.title("Simple Streamlit Layout Demo")
st.markdown(ss.summary)
FilterTabs()

if ss.tab_locked =="Insurance":
    st.markdown("**Insurance Tab is Locked**")
    Test()

# for exp_title in EXP_TITLES:
#     selected_key = f"{ss.tab_locked}_{exp_title}_selected" if ss.tab_locked else f"{LockedTab}_{exp_title}_selected"
#     selected = ss.get(selected_key, [])
#     if selected:
#         st.markdown(f"**{exp_title} Selected:** {', '.join(selected)}")


# YEAR, QUARTER, STATE  = st.columns(3)
# # For demo, suppose df1, df2, df3 and axis names already exist
# with YEAR:
#     if ss.tab_locked is not None and ss.tab_locked == tab_name:
#         selected = ss.get(f"{tab_name}_Year_selected", [])
#         if selected:
#             colname = "year"
#         st.write("Select * from Ins_Agg")

#     plot_bar_line(df1, 'x', 'bar_y', 'line_y', "Plot 1")
#     st.markdown(basic_summary(df1, 'x', 'bar_y', 'line_y'))

# with QUARTER:
#     plot_bar_line(df2, 'x', 'bar_y', 'line_y', "Plot 2")
#     st.markdown(basic_summary(df2, 'x', 'bar_y', 'line_y'))

# with STATE:
#     plot_bar_line(df3, 'x', 'bar_y', 'line_y', "Plot 3")
#     st.markdown(basic_summary(df3, 'x', 'bar_y', 'line_y'))