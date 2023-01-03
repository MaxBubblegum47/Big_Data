import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))




from collections import Counter
import pandas as pd
import re
from langdetect import detect
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from collections import Counter


list_file = [(root, files) for root, dirs, files in os.walk("/home/maxbubblegum/Big_Data/TextAnalytics/Lyrics_Not_Processed/Hard Rock/") if files] #set here the path of the directory of all your songs (if it contains other subdir no problem)

for path, files in list_file:
    for canzoni in files:
        tf = TfidfVectorizer(analyzer='word', min_df=0, max_features= 100 ,stop_words='english', lowercase=True)
        tfidf_matrix = tf.fit_transform(canzoni) # qui ci vanno le lyrics

        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
        results = {}
        
        for idx, row in df.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[idx][i], df['id'][i]) for i in similar_indices]
            results[row['id']] = similar_items[1:]

