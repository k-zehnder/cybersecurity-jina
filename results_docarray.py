from docarray import Document, DocumentArray
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from config import configs


index = DocumentArray.load(configs["INDEX_PATH"])
index.match(index, exclude_self=True)
index.summary()

# filter attacks
attacks_da = index.find({"tags__known_label" : {"$eq" : 1.0}}) # 566
attacks_da.summary()

# filter benign
benigns_da = index.find({"tags__known_label" : {"$eq" : 0.0}}) # 14535
benigns_da.summary()

attack_q = attacks_da[0] # known attack 
attack_q.match(index, exclude_self=True)
attack_q.summary()

benign_q = benigns_da[0] # known benign
benign_q.match(index, exclude_self=True)
benign_q.summary()

y_test = [] # expected
yhat = [] # "predictions" aka nearest neighbor/brute force

for doc in index:
    # known
    if doc.tags.get("known_label") == 0.0:
        y_test.append(0.0)
    else:
        y_test.append(1.0)
    
    # use similarity search to classify by class of nearest neighbor
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

