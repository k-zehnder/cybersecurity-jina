from jina import Flow, Executor, requests
from docarray import Document, DocumentArray


INDEX_PATH = "./index"


class ITPredictor(Executor):
    def __init__(self, index_path: str, **kwargs):
        super().__init__(**kwargs)
        self.index_path = index_path
        self.index = DocumentArray.load(self.index_path)
        self.index = DocumentArray(self.index, copy=True)
        self.index.match(self.index, exclude_self=True)

    @requests(on="/predict")
    def predict(self, docs: DocumentArray, **kwargs):
        # usually documentarray would be sent to this route, but in this app tis executor executor will load docs from documentarray we already have saved at INDEX_PATH location.
        print("[INFO] at predict route...")

        predictions = []
        for d in self.index:
            if d.matches[0].tags.get("known_label") == 0:
                predictions.append("Benign")
            else:
                predictions.append("Attack")
        
        return DocumentArray(Document(preds=predictions[i]) for i in range(len(predictions)))
        

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
 