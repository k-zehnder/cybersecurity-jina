from jina import Flow, Executor,requests
from docarray import Document, DocumentArray
import numpy as np


print("[INFO] sqlite...")
index = DocumentArray.load("index")
index.match(index, exclude_self=True)
index.summary()

print()
print()

print("[INFO] weaviate...")
da =  DocumentArray(
    storage='weaviate', config={'name': 'Persisted', 'host': 'localhost', 'port': 8080}
)
da.match(da, exclude_self=True)
da.summary()

