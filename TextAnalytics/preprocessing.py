import nltk
import os
from nltk.corpus import stopwords
import re
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

# stop_words = set(stopwords.words('english')) not working
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

with open("test.txt", encoding = "ISO-8859-1") as f:
    line = f.read()
    words = line.split()
    
    for w in words:
        if not w in stop_words:
            appendFile = open('filteredtext.txt','a') 

            # print("Before " + str(w))
            # CLEANING TEXT PARTS
            # w = w.lower() # lower case everything. By default I can do this thing inside the Stemmer
            w = re.sub("[\(\[].*?[\)\]]", "", w) # remove words in brackets
            w = stemmer.stem(w, True) # stemming with porter
            w = lemmatizer.lemmatize(w, 'v') # lemmatization
            # w = lemmatizer.lemmatize(w, 'n') # lemmatization nouns
            # w = lemmatizer.lemmatize(w, 'a') # lemmatization adjectives
            # w = lemmatizer.lemmatize(w, 's') # lemmatization satellite adjectives
            # print("After " + str(w))

            appendFile.write(" "+str(w))
            appendFile.close()

    with open("filteredtext.txt", "r") as f: #here we are opening the buffer and overwrite the song 
        with open("test.txt", "w") as f1:
            for line in f:
                f1.write(line)
    import os
    os.remove("filteredtext.txt") #we remove the buffer, we will not use it anymore

    f.close()