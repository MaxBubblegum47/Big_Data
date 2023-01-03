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