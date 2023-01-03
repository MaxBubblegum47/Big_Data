import os
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer

# IDEA: FARE UN CONFRONTO CON SCILEARN RIGUARDO LE SIMILITUDINE TRA BRANI, QUINDI PRIMA DI TUTTO DIVIDO I BRANI E LI ORGANIZZO E POI FACCIO LE SIMILITUDINI
# ANOTHER PROBLEM: DIVIDERE E ORGANIZZARE I BRANI IN BASE AL GENERE MUSICALE DI APPARTENENZA

# questo path non esiste piu' perche' e' stato tutto quanto spostato all'interno dei generi musicali
list_file = [(root, files) for root, dirs, files in os.walk("/home/maxbubblegum/Big_Data/TextAnalytics/Lyrics_Not_Processed/House/") if files] #set here the path of the directory of all your songs (if it contains other subdir no problem)

documents = []
for path, files in list_file:
    for canzoni in files:
        documents.append((path+canzoni))


tfidf = TfidfVectorizer().fit_transform(documents)
# no need to normalize, since Vectorizer will return normalized tf-idf
pairwise_similarity = tfidf * tfidf.T
print(type(pairwise_similarity))