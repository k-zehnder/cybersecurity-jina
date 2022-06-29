from jina import Flow, Executor, requests
from docarray import Document, DocumentArray
from config import configs


INDEX_PATH = configs["INDEX_PATH"]


class ITPredictor(Executor):
    def __init__(self, index_path: str, **kwargs):
        super().__init__(**kwargs)
        
        self.index_path = index_path
        self.docarray_index = DocumentArray.load(self.index_path)
        self.docarray_index = DocumentArray(self.docarray_index, copy=True)
        self.docarray_index.match(self.docarray_index, exclude_self=True)

        self.weaviate_index = DocumentArray(
                    storage='weaviate',
                    config={
                        'host': "localhost",
                        'port': 8080,
                        'name': "Persisted",
                    },
        )
        self.weaviate_index = DocumentArray(self.weaviate_index, copy=True)
        self.weaviate_index.match(self.weaviate_index, exclude_self=True)

        self.indexes = {
            "docarray" : self.docarray_index,
            "weaviate" : self.weaviate_index
        }

    @requests(on="/predict")
    def predict(self, docs: DocumentArray, **kwargs):
        # usually documentarray would be sent to this route, but in this app this executor will load docs from documentarray we already have saved at INDEX_PATH.
        # INDEX_PATH location is given as parameter when it is defined in Flow (i.e., "uses_with=").
        print("[INFO] at predict route...")

        da_predictions = []
        for d in self.indexes["docarray"]:
            if d.matches[0].tags.get("known_label") == 0:
                da_predictions.append("Benign")
            else:
                da_predictions.append("Attack")
        
        weav_predictions = []
        for d in self.indexes["weaviate"]:
            if d.matches[0].tags.get("known_label") == 0:
                weav_predictions.append("Benign")
            else:
                weav_predictions.append("Attack")
        
        return DocumentArray(Document(pred_da=p_da, pred_weav=p_weav) for p_da, p_weav in zip(da_predictions, weav_predictions))


f = (
    Flow(port=12345)
    .add(
        uses=ITPredictor,
        name="ITPredictor",
        uses_with={"index_path" : INDEX_PATH}

    )
)    

if __name__ == "__main__":
    with f:
        print("[INFO] blocking...")
        f.block()
        
 