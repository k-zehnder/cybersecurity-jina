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
    # return ["Benign" if d.matches[0].tags.get("known_label") == 0.0 else "Attack" for d in da]


if __name__ == '__main__':
    preds = get_preds("index")
    print(f"preds: {preds}")