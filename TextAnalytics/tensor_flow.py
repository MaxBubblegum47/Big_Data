import pandas as pd
import numpy as np

df = pd.read_csv('lyrics.csv', on_bad_lines='skip')

df['ranker_genre'] = np.where(
    (df['ranker_genre'] == 'screamo')|
    (df['ranker_genre'] == 'punk rock')|
    (df['ranker_genre'] == 'heavy metal'), 
    'alt rock', 
    df['ranker_genre']
)
# group creation
group = ['song', 'year', 'album', 'genre', 'artist', 'ranker_genre']

# fixing the name of the song
lyrics_by_song = df.sort_values(group)\
        .groupby(group).lyric\
        .apply(' '.join)\
        .apply(lambda x: x.lower())\
        .reset_index(name='lyric')

lyrics_by_song["lyric"] = lyrics_by_song['lyric'].str.replace(r'[^\w\s]','')

from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import Dense
import random

# select genre to analyze
genres = [
    'pop', 'alt rock', 'Hip Hop',
]

LYRIC_LEN = 200 # each song has to be > 400 characters
N = random.randint(1000, 3000) # random number of records to pull from each genre
RANDOM_SEED = random.randint(200, 1000) # random seed to make results repeatable

train_df = pd.DataFrame()
test_df = pd.DataFrame()

# loop over each genre
for genre in genres: 

    # create a subset with the correct genre and the right lenght of the song
    subset = lyrics_by_song[  
        (lyrics_by_song.ranker_genre==genre) & 
        (lyrics_by_song.lyric.str.len() > LYRIC_LEN)
    ]

    # dataset creation
    train_set = subset.sample(n=N, random_state=RANDOM_SEED, replace=True)
    test_set = subset.drop(train_set.index)
    train_df = train_df.append(train_set) # append subsets to the master sets
    test_df = test_df.append(test_set)

train_df = shuffle(train_df)
test_df = shuffle(test_df)

# Encode the labels as integers
encoder = LabelEncoder()
y_train = encoder.fit_transform(train_df.ranker_genre)
y_test = encoder.transform(test_df.ranker_genre)

# Vectorize the lyrics
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_df.lyric)
X_test = vectorizer.transform(test_df.lyric)

model = tf.keras.Sequential()
model.add(Dense(128, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(3, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

y_train_tensor = tf.convert_to_tensor(y_train)
y_test_tensor = tf.convert_to_tensor(y_test)

# Convert the vectors to a dense tensor
X_train = tf.convert_to_tensor(X_train.todense())
X_test = tf.convert_to_tensor(X_test.todense())


history = model.fit(X_train, y_train_tensor, epochs=10, validation_data=(X_test, y_test_tensor))

# display the data
import matplotlib.pyplot as plt

# Get the training and validation loss values
loss = history.history['loss']
val_loss = history.history['val_loss']

# Plot the training and validation loss
plt.plot(loss)
plt.plot(val_loss)
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training loss', 'Validation loss'])
plt.show()

# display result by music genre
from sklearn.metrics import classification_report

# predict labels for test data
y_pred = model.predict(X_test)

# convert predicted labels back to original labels
y_pred = encoder.inverse_transform(y_pred)

# print classification report
print(classification_report(y_test, y_pred, target_names=genres))


