import numpy as np
import pandas as pd
from jina import Flow, Executor, requests
from docarray import Document, DocumentArray
from config import configs


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
    
    
class WeaviateIndexer(Executor):
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
        print(docs) 
        docs.summary()
       
f = (
    Flow()
    .add(
        uses=ITPrepper, 
        name="ITPrepper", 
        uses_with={"data_url" : configs["DATA_URL_DATASET_2"]}
    ).add(
        uses=DocArrayIndexer, 
        name="DocArrayIndexer",
        needs="ITPrepper", 
        uses_with={"index_path" : configs["INDEX_PATH"]}
    ).add(
        uses=WeaviateIndexer,
        name="WeaviateIndexer",
        needs="ITPrepper"
    ).add(
        uses=DummyExecutor,
        name="DummyExecutor",
        needs=["DocArrayIndexer", "WeaviateIndexer"]
    )
)

# f.plot(configs["FLOW_SAVE_PATH"])

with f:
    f.post(on="/start", show_progress=True)
 
 