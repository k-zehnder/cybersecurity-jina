from jina import Document, DocumentArray, Client
import pandas as pd
import streamlit as st


def get_data(index_path):
    da = DocumentArray.load(index_path)
    df = da.to_dataframe()
    return clean_data(df)

def clean_data(df):
    attack_benign_docarray = get_docarray_predictions()
    attack_benign_weaviate = get_weaviate_predictions()

    
    df["doc_id"] = df["id"].apply(lambda x: x[:8])
    df["datetime"] = df["tags"].apply(lambda x: x.get("dt"))
    df["known_label"] = df["tags"].apply(lambda x: x.get("known_label"))
    df["port"] = df["tags"].apply(lambda x: int(x.get("port")))
    df["protocol"] = df["tags"].apply(lambda x: int(x.get("protocol")))
    df["known_label"] = df["known_label"].map(lambda x: "Benign" if x == 0.0 else "Attack")
    df["predicted_da"] = attack_benign_docarray
    df["predicted_weav"] = attack_benign_weaviate
    df['is_wrong'] = df.apply(lambda x: (x['predicted_da'] != x['known_label']) or (x['predicted_weav'] != x['known_label']), axis=1)
    return df[["datetime", "doc_id", "port", "protocol", "known_label", "predicted_da", "predicted_weav", "is_wrong", "embedding"]]

def get_client():
    return Client(port="12345")

def get_docarray_predictions():
    """
    NOTE: Need to have query_flow.py running in seperate terminal tab for this function to work.
    """
    client = get_client()
    results = client.post("/predict", return_results=True)
    return [doc.tags.get("pred_da") for doc in results]


def get_weaviate_predictions():
    """
    NOTE: Need to have query_flow.py running in seperate terminal tab for this function to work.
    """
    client = get_client()
    results = client.post("/predict", return_results=True)
    return [doc.tags.get("pred_weav") for doc in results]


def set_bg_hack_url(url: str) -> None:
    """
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    """
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url({url});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )