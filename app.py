import streamlit as st
from StFiles.MyProfile import myProfile
from StFiles.stDBProcess import get_lists
from StFiles.Layout import EXP_TITLES, FilterTabs
import matplotlib.pyplot as plt
from StFiles.Insurance import InsNonFilterTabs
from StFiles.Transaction import TransNonFilterTabs # type: ignore
from StFiles.User import UserNonFilterTabs # type: ignore

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
