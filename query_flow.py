from jina import Flow, Executor, requests
from docarray import Document, DocumentArray


INDEX_PATH = "./data/index"


class ITPredictor(Executor):
    def __init__(self, index_path: str, **kwargs):
        super().__init__(**kwargs)
        self.index_path = index_path
        self.index = DocumentArray.load(self.index_path)
        self.index = DocumentArray(self.index, copy=True)
        self.index.match(self.index, exclude_self=True)

    @requests(on="/predict")
    def predict(self, docs: DocumentArray, **kwargs):
        # usually documentarray would be sent to this route, but in this app this executor will load docs from documentarray we already have saved at INDEX_PATH location given as parameter when it is defined in Flow (i.e., "uses_with=").
        print("[INFO] at predict route...")

        predictions = []
        for d in self.index:
            if d.matches[0].tags.get("known_label") == 0:
                predictions.append("Benign")
            else:
                predictions.append("Attack")
        
        return DocumentArray(Document(preds=pred) for pred in predictions)
        

f = (
    Flow(port=12345)
    .add(
        uses=ITPredictor,
        name="ITPredictor",
        uses_with={"index_path" : INDEX_PATH}
    )
)    

with f:
    print("[INFO] blocking...")
    f.block()
 