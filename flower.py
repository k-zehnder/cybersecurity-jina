import os
from jina import Flow, Executor, requests
from jina import DocumentArray, Executor, requests
from docarray import Document, DocumentArray
import pandas as pd
import numpy as np


# DATA_URL_DATASET_1 = "https://github.com/k-zehnder/cybersecurity-jina/blob/main/data/embeddings_df_with_details.csv?raw=true"
DATA_URL_DATASET_2 = "https://github.com/k-zehnder/cybersecurity-jina/blob/main/data/dataset_2_embeddings_df_with_details.csv?raw=true"
INDEX_PATH = "index"


class ITPrepper(Executor):
    def __init__(self, data_url: str, **kwargs):
        super().__init__(**kwargs)
        self.embeddings_df = pd.read_csv(data_url)
        
    @requests
    def preprocess(self, docs: DocumentArray, **kwargs):
        res_da = DocumentArray()
        for i in range(len(self.embeddings_df)):
            d = Document(
                embedding=np.array(self.embeddings_df.iloc[i, :128].tolist()), 
                tags={
                    "dt" : self.embeddings_df.loc[i, "dt"],
                    "known_label" : self.embeddings_df.loc[i, "Label"],
                    "port" : float(self.embeddings_df.loc[i, "Dst Port"]),
                    "protocol" : float(self.embeddings_df.loc[i, "Protocol"]),
                }
            )
            res_da.append(d)
        return res_da


class DocArrayIndexer(Executor):
    def __init__(self, index_path: str, **kwargs):
        super().__init__(**kwargs)
        self.index_path = index_path
        self.index = DocumentArray()

    @requests
    def index(self, docs: DocumentArray, **kwargs):
        print("[INFO] saving index to disk...")
        with self.index:
            self.index.extend(docs)
        self.index.save(self.index_path)
        # return self.index
    
    
class WeaviateExecutor(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.index = DocumentArray(
                    storage='weaviate',
                    config={
                        'host': "localhost",
                        'port': 8080,
                        'name': "Persisted",
                    },
        )

    @requests
    def index(self, docs: DocumentArray, **kwargs):
        print("[INFO] saving weaviate index...")        
        with self.index:
            self.index.extend(docs)
        self.index.summary()
        # return self.index

class DummyExecutor(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    @requests
    def index(self, docs: DocumentArray, **kwargs):
        print("[INFO] at DummyExecutor...")  
        print(docs) # len 15000 as expected b/c goes parallel to each prior executor in flow
        docs.summary()
       
f = (
    Flow()
    .add(
        uses=ITPrepper, 
        name='ITPrepper', 
        uses_with={"data_url" : DATA_URL_DATASET_2}
    ).add(
        uses=DocArrayIndexer, 
        name='DocArrayIndexer',
        needs='ITPrepper', 
        uses_with={"index_path" : INDEX_PATH}
    ).add(
        uses=WeaviateExecutor,
        name='WeaviateExecutor',
        needs='ITPrepper'
    ).add(
        uses=DummyExecutor,
        name="DummyExecutor",
        needs=['DocArrayIndexer', 'WeaviateExecutor']
    )
)

f.plot("flow.svg")

with f:
    f.post(on="/start", show_progress=True)
 
 