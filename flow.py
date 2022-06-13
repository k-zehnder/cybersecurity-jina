from jina import Flow, Executor, requests
from docarray import Document, DocumentArray
import pandas as pd
import numpy as np


DATA_URL = "https://github.com/k-zehnder/cybersecurity-jina/blob/main/data/embeddings_df_with_details.csv?raw=true"
INDEX_PATH = "./index"

class ITPrepper(Executor):
    def __init__(self, data_url: str, **kwargs):
        super().__init__(**kwargs)
        self.data_url = data_url
        self.embeddings_df = pd.read_csv(self.data_url)
        
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

class ITIndexer(Executor):
    def __init__(self, index_path: str, **kwargs):
        super().__init__(**kwargs)
        self.index_path = index_path
        self.index = DocumentArray()

    @requests
    def index(self, docs: DocumentArray, **kwargs):
        with self.index:
            for doc in docs:
                self.index.append(doc)
        
        print("[INFO] saving index to disk...")
        self.index.save(self.index_path)
        return self.index

f = (
    Flow()
    .add(
        uses=ITPrepper,
        name="ITPrepper",
        uses_with={"data_url" : DATA_URL}
    ).add(
        uses=ITIndexer,
        name="ITIndexer",
        uses_with={"index_path" : INDEX_PATH}
    )
)    

with f:
    f.post(on="/start")
 