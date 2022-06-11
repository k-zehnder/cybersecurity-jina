from jina import Flow, Executor, requests
from docarray import Document, DocumentArray
import pandas as pd
import numpy as np


PATH = "/Users/peppermint/Desktop/codes/python/cybersecurity-jina/data/embeddings_df_with_details.csv"


class ITPrepper(Executor):
    def __init__(self, path: str, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.embeddings_df = pd.read_csv(self.path)
        
    @requests
    def preprocess(self, docs: DocumentArray, **kwargs):
        res_da = DocumentArray()
        for i in range(len(self.embeddings_df)):
            d = Document(
                embedding=np.array(self.embeddings_df.iloc[i, :128].tolist()), 
                dt=self.embeddings_df.loc[i, "dt"],
                known_label=self.embeddings_df.loc[i, "Label"],
            )
            res_da.append(d)
        return res_da

class ITIndexer(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index = DocumentArray()

    @requests
    def index(self, docs: DocumentArray, **kwargs):
        with self.index:
            for doc in docs:
                self.index.append(doc)
        print("[INFO] saving index to disk...")
        self.index.save("index")
        self.index.summary()
        return self.index

f = (
    Flow()
    .add(
        uses=ITPrepper,
        name="ITPrepper",
        uses_with={"path" : PATH}
    ).add(
        uses=ITIndexer,
        name="ITIndexer",
    )
)    

with f:
    f.post(on="/start")
 