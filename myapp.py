from docarray import Document, DocumentArray
import pandas as pd
import plotly.express as px
import streamlit as st

from helpers import get_data, set_bg_hack_url, get_data_from_excel

# ---------- Main area
st.set_page_config(page_title="Cybersecurity Dashboard", page_icon=":spider:", layout="wide")
set_bg_hack_url("https://wallpapercave.com/uwp/uwp1259188.gif")
st.title(":spider:  Cybersecurity Dashboard")

# ---- GET DATA
df = get_data("index")
old_df = get_data_from_excel()

# creating a single-element container.
placeholder = st.empty()

with placeholder.container():
    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs 
    kpi1.metric(label="Threat Level 🚨", value=3, delta=2)
    kpi2.metric(label="Attacks/Hr 🕐", value=200, delta=30)
    kpi3.metric(label="Estimated Damage 💰", value=300000, delta=50000)

fig1 = px.histogram(df, x="datetime", y="predicted", histfunc="count", nbins=8, text_auto=True, title='Threat Volume')

fig2 = px.pie(df, values=df["predicted"].value_counts(), names=df["predicted"].unique().tolist(), title='Threat Distribution')

# #NOTE: make one of these a map?
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)


st.dataframe(df[["datetime", "doc_id", "port", "protocol", "known_label", "predicted", "is_wrong", "embedding"]])


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=["New York", "Houston", "San Francisco"],
    default=["San Francisco", "Houston"]
)

customer_type = st.sidebar.multiselect(
    "Select the Attack Type:",
    options=["Benign", "Attack"],
    default=["Attack", "Benign"]
)

gender = st.sidebar.multiselect(
    "Select the Port:",
    options=["44", "80"],
    default=["80"]
)

# ---- HIDE STREAMLIT STYLE ----
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)
