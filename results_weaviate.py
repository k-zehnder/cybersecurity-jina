from jina import Flow, Executor,requests
from docarray import Document, DocumentArray
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score


print("[INFO] weaviate...")
da =  DocumentArray(
    storage='weaviate', config={'name': 'Persisted', 'host': 'localhost', 'port': 8080}
)

# # simulate; had problems using match with weavaite backend and getting it to persist (even when using as context manager ) so this is workaround
da = DocumentArray(da, copy=True)
da.match(da, exclude_self=True)

y_test = [] # expected
yhat = [] # "predictions" aka nearest neighbor/brute force

for doc in da:
    # known
    if doc.tags.get("known_label") == 0.0:
        y_test.append(0.0)
    else:
        y_test.append(1.0)
    
    # use similarity search to classify depending on class of nearest neighbor
    if doc.matches[0].tags.get("known_label") == 0.0:
        yhat.append(0.0)
    else:
        yhat.append(1.0)
    
    if doc.tags.get("known_label") != doc.matches[0].tags.get("known_label"):
        print("[INFO] wrong!...")


# accuracy: (tp + tn) / (p + n)
accuracy = accuracy_score(y_test, yhat)
print('Accuracy: %f' % accuracy)
# precision tp / (tp + fp)
precision = precision_score(y_test, yhat)
print('Precision: %f' % precision)
# recall: tp / (tp + fn)
recall = recall_score(y_test, yhat)
print('Recall: %f' % recall)
# f1: 2 tp / (2 tp + fp + fn)
f1 = f1_score(y_test, yhat)
print('F1 score: %f' % f1)

# dataset1--weaviate:


# dataset2--weaviate:
# Accuracy: 0.997933
# Precision: 0.955923
# Recall: 0.958564
# F1 score: 0.957241





