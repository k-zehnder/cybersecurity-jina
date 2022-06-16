from jina import Flow, Executor,requests
from docarray import Document, DocumentArray
import numpy as np


# ---------- Docarray
print("[INFO] sqlite...")
index = DocumentArray.load("index")
index.match(index, exclude_self=True)
index.summary()

print()
print()



# ---------- Weaviate
print("[INFO] weaviate...")
da =  DocumentArray(
    storage='weaviate', config={'name': 'Persisted', 'host': 'localhost', 'port': 8080}
)

with da:
    q = DocumentArray(Document(embedding=da[0].embedding))
    res = da.find(q, limit=2)
    print(f"[INFO] query results...")

print(len(res)
)#1
print(res) # returns len 1 list of docrray with 2 sub docs
print(type(res)) # list
print(res[0][0].tags.get("known_label")) # 0.0

print()
print()



