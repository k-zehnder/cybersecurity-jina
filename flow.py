import os
from jina import Flow, Executor, requests
from docarray import Document, DocumentArray
import pandas as pd
import numpy as np
import pinecone
from helpers import chunks
from typing import Dict, Optional


PATH = "/Users/peppermint/Desktop/codes/python/NetworkIntrusionDetection/embeddings_df.csv"


class ITPrepper(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.embeddings_df = pd.read_csv(PATH).iloc[:, :-1]
        self.label_df = pd.read_csv(PATH).iloc[:, -1]

    @requests
    def preprocess(self, docs: DocumentArray, **kwargs):
        res_da = DocumentArray()
        for i in range(len(self.embeddings_df)):
            d = Document(embedding=np.array(self.embeddings_df.iloc[i, :].tolist()), known_label=self.label_df[i])
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
    ).add(
        uses=ITIndexer,
        name="ITIndexer",
    )
)    

with f:
    f.post(on="/start")
 