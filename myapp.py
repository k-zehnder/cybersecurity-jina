import plotly.express as px
import streamlit as st
from config import configs
from helpers import get_data, set_bg_hack_url


# -------------- Config
st.set_page_config(page_title="Cybersecurity Dashboard", page_icon="🔍", layout="wide")
set_bg_hack_url("https://wallpapercave.com/uwp/uwp1259188.gif")
st.title("🚨  Cybersecurity Dashboard")

# -------------- Get data
df = get_data(configs["INDEX_PATH"])

# -------------- Main area
placeholder = st.empty()
with placeholder.container():
    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(label="Threat Level 🔥", value=3, delta=2)
    kpi2.metric(label="Attacks/Hr 🕐", value=200, delta=-30)
    kpi3.metric(label="Estimated Damage 💰", value=300000, delta=50000)

fig1 = px.histogram(df, x="datetime", y="predicted_da", histfunc="count", nbins=8, text_auto=True, title='Threat Volume')
fig2 = px.pie(df, values=df["predicted_da"].value_counts(), names=df["predicted_da"].unique().tolist(), title='Threat Distribution')

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

st.dataframe(df)

# -------------- Sidebar (simulated)
st.sidebar.header("Please Filter Here:")
region = st.sidebar.multiselect(
    "Select the City:",
    options=["New York", "Houston", "San Francisco"],
    default=["San Francisco", "Houston"]
)

attack_type = st.sidebar.multiselect(
    "Select the Attack Type:",
    options=["Benign", "Attack"],
    default=["Attack", "Benign"]
)

port = st.sidebar.multiselect(
    "Select the Port:",
    options=["44", "80"],
    default=["80"]
)

# -------------- Hide streamlit style
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)
