from sklearn import *
import os
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

list_file = [(root, files) for root, dirs, files in os.walk("/home/maxbubblegum/Big_Data/TextAnalytics/Lyrics_Not_Processed/Rock/") if files] #set here the path of the directory of all your songs (if it contains other subdir no problem)

documents = []
canzoni_train = list()
for path, files in list_file:
    for canzoni in files:
        canzoni_train.append(canzoni)
        
X_train = canzoni_train
y_train = canzoni_train

list_file = [(root, files) for root, dirs, files in os.walk("/home/maxbubblegum/Big_Data/TextAnalytics/Lyrics_Not_Processed/Hard Rock/") if files] #set here the path of the directory of all your songs (if it contains other subdir no problem)
canzoni_test = list()
for path, files in list_file:
    for canzoni in files:
        canzoni_test.append(canzoni)

X_test = canzoni_test
y_test = canzoni_test

vectorizer = TfidfVectorizer()
train_vectors = vectorizer.fit_transform(X_train)
test_vectors = vectorizer.transform(X_test)

print(train_vectors.shape, test_vectors.shape)

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(train_vectors, y_train)

from  sklearn.metrics  import accuracy_score
predicted = clf.predict(test_vectors)
print(accuracy_score(y_test,predicted))
