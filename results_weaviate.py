from jina import Flow, Executor,requests
from docarray import Document, DocumentArray
import numpy as np

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

print(q) # docarray with 1 sub document
print(type(q)) # docarray
print(q.summary())


# attacks_da = index.find({"tags__known_label" : {"$eq" : 1.0}}) # 566
# attacks_da.summary()

# benigns_da = index.find({"tags__known_label" : {"$eq" : 0.0}}) # 14535
# benigns_da.summary()


# attack_q = index[-10] # known attack 
# attack_q.match(index, exclude_self=True)
# attack_q.summary()

# benign_q = index[0] # known benign
# benign_q.match(index, exclude_self=True)
# benign_q.summary()

# y_test = [] # expected
# yhat = [] # "predictions" aka nearest neighbor/brute force

# for doc in index:
#     # known
#     if doc.tags.get("known_label") == 0.0:
#         y_test.append(0.0)
#     else:
#         y_test.append(1.0)
    
#     # these are nearest neighbor/brute force which is basically the "prediction" since we have embeddings stored in vector space as opposed to a forward pass through neural network or something
#     if doc.matches[0].tags.get("known_label") == 0.0:
#         yhat.append(0.0)
#     else:
#         yhat.append(1.0)


# # accuracy: (tp + tn) / (p + n)
# accuracy = accuracy_score(y_test, yhat)
# print('Accuracy: %f' % accuracy)
# # precision tp / (tp + fp)
# precision = precision_score(y_test, yhat)
# print('Precision: %f' % precision)
# # recall: tp / (tp + fn)
# recall = recall_score(y_test, yhat)
# print('Recall: %f' % recall)
# # f1: 2 tp / (2 tp + fp + fn)
# f1 = f1_score(y_test, yhat)
# print('F1 score: %f' % f1)

# dataset1--sqlite:
# Accuracy: 0.997748
# Precision: 0.966667
# Recall: 0.973498
# F1 score: 0.970070

# dataset2--sqlite:
# Accuracy: 0.997933
# Precision: 0.955923
# Recall: 0.958564
# F1 score: 0.957241

# dataset1--weaviate:


# dataset2--weaviate:



print()
print()

# for d in index[-900:-400]:
#     known = d.tags.get("known_label")
#     print(f"known label: {known}")
    
#     for m in d.matches[:2]:
#         predicted = m.tags.get("known_label")
#         score =  m.scores['cosine'].value
        
#         print(f"predicted: {predicted} -- score: {score}")
        
#         if known != predicted:
#             print("[INFO] wrong...")

#     print()




