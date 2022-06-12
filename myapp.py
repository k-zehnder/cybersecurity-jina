from docarray import Document, DocumentArray
import pandas as pd
import plotly.express as px
import streamlit as st

from helpers import get_preds


st.set_page_config(page_title="Cybersecurity Dashboard", page_icon=":spider:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="./data/supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

def get_data(index_path):
    da = DocumentArray.load(index_path)
    da_df = da.to_dataframe()
    return da_df

# old_df = get_data_from_excel()
df = get_data("index")
  
df["id"] = df["id"].apply(lambda x: x[:8])
df["datetime"] = df["tags"].apply(lambda x: x.get("dt"))
df["known_label"] = df["tags"].apply(lambda x: x.get("known_label"))
df["known_label"] = df["known_label"].map(lambda x: "Benign" if x == 0.0 else "Attack")
df["predicted"] = get_preds("index")
df['is_wrong'] = df.apply(lambda x: x['predicted'] != x['known_label'], axis=1)

st.dataframe(df[["id", "datetime", "predicted", "known_label", "is_wrong", "tags", "embedding"]])




# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
