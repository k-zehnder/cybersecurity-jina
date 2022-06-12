from docarray import Document, DocumentArray
import pandas as pd
import plotly.express as px
import streamlit as st

from helpers import get_data


st.set_page_config(page_title="Cybersecurity Dashboard", page_icon=":spider:", layout="wide")

# ---- GET DATA
# old_df = get_data_from_excel()
df = get_data("index")

fig_line1 = px.line(df, x="datetime", y=df["predicted"], title='Network Intrusion Predictions')

fig_line2 = px.line(df, x="datetime", y=df["predicted"], title='Network Intrusion Predictions')

# #NOTE: make one of these a map?
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_line1, use_container_width=True)
right_column.plotly_chart(fig_line2, use_container_width=True)

st.dataframe(df[["id", "datetime", "known_label", "predicted", "is_wrong", "tags", "embedding"]])

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
