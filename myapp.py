from docarray import Document, DocumentArray
import pandas as pd
import plotly.express as px
import streamlit as st

from helpers import get_data


st.set_page_config(page_title="Cybersecurity Dashboard", page_icon=":spider:", layout="wide")

# ---- GET DATA
# old_df = get_data_from_excel()
df = get_data("index")

fig1 = px.histogram(df, x="datetime", y="predicted", histfunc="count", nbins=8, text_auto=True, title='Threat Volume')

fig2 = px.pie(df, values=df["predicted"].value_counts(), names=df["predicted"].unique().tolist(), title='Threat Distribution')

# #NOTE: make one of these a map?
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

st.dataframe(df[["datetime", "doc_id", "port", "protocol", "known_label", "predicted", "is_wrong", "embedding"]])
# tags

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
