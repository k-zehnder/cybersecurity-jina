from jina import Flow, Executor, requests
from docarray import Document, DocumentArray
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score


index = DocumentArray.load("index")

index.match(index, exclude_self=True)
index.summary()

attacks_da = index.find({"tags__known_label" : {"$eq" : 1.0}}) # 566
attacks_da.summary()

benigns_da = index.find({"tags__known_label" : {"$eq" : 0.0}}) #14535
benigns_da.summary()


attack_q = index[-10] # known attack 
attack_q.match(index, exclude_self=True)
attack_q.summary()

benign_q = index[0] # known benign
benign_q.match(index, exclude_self=True)
benign_q.summary()

yhat = [] # "predictions" aka nearest neigh.
y_test = [] # expected

for doc in index:
    # known
    if doc.tags.get("known_label") == 0.0:
        y_test.append(0.0)
    else:
        y_test.append(1.0)
    
    # these are nearest neighbor which is basically the "prediction" since we have embeddings stored in vector space as opposed to a forward pass through neural network or something
    if doc.matches[0].tags.get("known_label") == 0.0:
        yhat.append(0.0)
    else:
        yhat.append(1.0)


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


print()
print()

for d in index[-900:-400]:
    known = d.tags.get("known_label")
    print(f"known label: {known}")
    
    for m in d.matches[:2]:
        predicted = m.tags.get("known_label")
        score =  m.scores['cosine'].value
        
        print(f"predicted: {predicted} -- score: {score}")
        
        if known != predicted:
            print("[INFO] wrong...")

    print()
