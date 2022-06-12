from docarray import Document, DocumentArray
import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache
def get_preds(index_path):
    da = DocumentArray.load(index_path)
    da.match(da, exclude_self=True)
    
    preds =[]
    for d in da:
        if d.matches[0].tags.get("known_label") == 0:
            preds.append("Benign")
        else:
            preds.append("Attack")
    return preds

def get_data(index_path):
    da = DocumentArray.load(index_path)
    df = da.to_dataframe()

    df["id"] = df["id"].apply(lambda x: x[:8])
    df["datetime"] = df["tags"].apply(lambda x: x.get("dt"))
    df["known_label"] = df["tags"].apply(lambda x: x.get("known_label"))
    df["known_label"] = df["known_label"].map(lambda x: "Benign" if x == 0.0 else "Attack")
    df["predicted"] = get_preds(index_path)
    df['is_wrong'] = df.apply(lambda x: x['predicted'] != x['known_label'], axis=1)
    
    return df

if __name__ == '__main__':
    preds = get_preds("index")
    print(f"preds: {preds}")