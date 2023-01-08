import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from nltk.corpus import stopwords
import random
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV

# Read in the CSV file and filter the data to include only rows with 'screamo', 'punk rock', or 'heavy metal' in the 'ranker_genre' column
df = pd.read_csv('lyrics.csv', on_bad_lines='skip')
df['ranker_genre'] = np.where(
    (df['ranker_genre'] == 'screamo')|
    (df['ranker_genre'] == 'punk rock')|
    (df['ranker_genre'] == 'heavy metal'), 
    'alt rock', 
    df['ranker_genre']
)

# Group the data by song, year, album, genre, artist, and ranker_genre, and concatenate the lyrics into a single string for each group
group = ['song', 'year', 'album', 'genre', 'artist', 'ranker_genre']
lyrics_by_song = df.sort_values(group)\
        .groupby(group).lyric\
        .apply(' '.join)\
        .apply(lambda x: x.lower())\
        .reset_index(name='lyric')

# Remove non-alphanumeric characters from the 'lyric' column
lyrics_by_song["lyric"] = lyrics_by_song['lyric'].str.replace(r'[^\w\s]','')

# Select the genres to analyze
genres = ['pop', 'alt rock', 'Hip Hop']

# Set the minimum length for each song
LYRIC_LEN = 200 # each song has to be > 400 characters

# Select a random number of records to pull from each genre
N = random.randint(1000, 3000)

# Set a random seed to make the results repeatable
RANDOM_SEED = random.randint(200, 1000)

# Initialize the train and test dataframes
train_df = pd.DataFrame()
test_df = pd.DataFrame()

# Loop over each genre
for genre in genres: 
    # Create a subset with the correct genre and the right length of the song
    subset = lyrics_by_song[  
        (lyrics_by_song.ranker_genre==genre) & 
        (lyrics_by_song.lyric.str.len() > LYRIC_LEN)
    ]

    # Split the subset into training and test sets
    train_set = subset.sample(n=N, random_state=R
ANDOM_SEED, replace=True)
    test_set = subset.drop(train_set.index)
    
    # Append the subsets to the master sets
    train_df = train_df.append(train_set)
    test_df = test_df.append(test_set)

# Shuffle the train and test dataframes
train_df = shuffle(train_df)
test_df = shuffle(test_df)

# Define a function to create a pipeline with a count vectorizer and a Multinomial Naive Bayes classifier
def create_count_nb_pipeline():
    return Pipeline([
        ('vect', CountVectorizer()),
        ('clf', MultinomialNB())
    ])

# Define a function to create a pipeline with a Tf-idf vectorizer and a Multinomial Naive Bayes classifier
def create_tfidf_nb_pipeline():
    return Pipeline([
        ('vect', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])

# Create the pipelines
count_nb_pipeline = create_count_nb_pipeline()
tfidf_nb_pipeline = create_tfidf_nb_pipeline()

# Use cross-validation to evaluate the performance of the count vectorizer/Multinomial NB pipeline
scores = cross_val_score(count_nb_pipeline, train_df.lyric, train_df.ranker_genre, cv=5)
print(f"Mean count vectorizer/Multinomial NB accuracy: {scores.mean():.3f} +/- {scores.std():.3f}")

# Use cross-validation to evaluate the performance of the Tf-idf vectorizer/Multinomial NB pipeline
scores = cross_val_score(tfidf_nb_pipeline, train_df.lyric, train_df.ranker_genre, cv=5)
print(f"Mean Tf-idf vectorizer/Multinomial NB accuracy: {scores.mean():.3f} +/- {scores.std():.3f}")

# Define a parameter grid for the count vectorizer/Multinomial NB pipeline
param_grid = {
    'vect__max_df': [0.5, 0.75, 1.0],
    'vect__min_df': [2, 3, 4],
    'vect__max_features': [None, 1000, 5000],
    'clf__alpha': [0.1, 0.5, 1.0]
}

# Use grid search to tune the hyperparameters of the count vector
# Use randomized search to tune the hyperparameters of the count vectorizer/Multinomial NB pipeline
random_search = RandomizedSearchCV(count_nb_pipeline, param_distributions=param_grid, n_iter=50, cv=5, random_state=RANDOM_SEED)
random_search.fit(train_df.lyric, train_df.ranker_genre)
print(f"Best count vectorizer/Multinomial NB accuracy: {random_search.best_score_:.3f}")
print(f"Best count vectorizer/Multinomial NB parameters: {random_search.best_params_}")

# Use randomized search to tune the hyperparameters of the Tf-idf vectorizer/Multinomial NB pipeline
random_search = RandomizedSearchCV(tfidf_nb_pipeline, param_distributions=param_grid, n_iter=50, cv=5, random_state=RANDOM_SEED)
random_search.fit(train_df.lyric, train_df.ranker_genre)
print(f"Best Tf-idf vectorizer/Multinomial NB accuracy: {random_search.best_score_:.3f}")
print(f"Best Tf-idf vectorizer/Multinomial NB parameters: {random_search.best_params_}")

# Use grid search to tune the hyperparameters of the count vectorizer/Multinomial NB pipeline with Tf-idf transformer
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB())
])
param_grid = {
    'vect__max_df': [0.5, 0.75, 1.0],
    'vect__min_df': [2, 3, 4],
    'vect__max_features': [None, 1000, 5000],
    'clf__alpha': [0.1, 0.5, 1.0]
}
grid_search = GridSearchCV(pipeline, param_grid, cv=5)
grid_search.fit(train_df.lyric, train_df.ranker_genre)
print(f"Best count vectorizer/Tf-idf transformer/Multinomial NB accuracy: {grid_search.best_score_:.3f}")
print(f"Best count vectorizer/Tf-idf transformer/Multinomial NB parameters: {grid_search.best_params_}")
