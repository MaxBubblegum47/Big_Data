import os
import text2emotion as te
from lyricsgenius import Genius
from sklearn.feature_extraction.text import TfidfVectorizer

# IDEA: FARE UN CONFRONTO CON SCILEARN RIGUARDO LE SIMILITUDINE TRA BRANI, QUINDI PRIMA DI TUTTO DIVIDO I BRANI E LI ORGANIZZO E POI FACCIO LE SIMILITUDINI
# ANOTHER PROBLEM: DIVIDERE E ORGANIZZARE I BRANI IN BASE AL GENERE MUSICALE DI APPARTENENZA

list_file = [(root, files) for root, dirs, files in os.walk("/home/maxbubblegum/Big_Data/TextAnalytics/Lyrics_Not_Processed/Lyrics/Eminem/") if files] #set here the path of the directory of all your songs (if it contains other subdir no problem)

documents = []
for path, files in list_file:
    for canzoni in files:
        documents.append((path+canzoni))


tfidf = TfidfVectorizer().fit_transform(documents)
# no need to normalize, since Vectorizer will return normalized tf-idf
pairwise_similarity = tfidf * tfidf.T
print(pairwise_similarity)


# LETTURA DI TUTTI QUANTI I FILE 
# to print all the file
# list_file=[]
# list_file = [(root, files) for root, dirs, files in os.walk("/home/maxbubblegum/Desktop/Big_Data/TextAnalytics/Lyrics_Not_Processed") if files] #set here the path of the directory of all your songs (if it contains other subdir no problem)
# list_file.sort()

# for path, files in list_file:
#     print(path)
#     for canzoni in files:
#         file = open(path +"/" + str(canzoni),"r", encoding="ISO-8859-1") # encoding per windows
#         print(canzoni) # stampa nomi di canzoni
#         print(file.read()) # stampa path della canzone
#         # righe = file.read()
#         # words = righe.split()
        
#         # print(righe)

#-----------------------------------------------------------------------------------------------

# LETTURA DELLE RIGHE DI UNA CANZONE
# song = open("/home/maxbubblegum/Desktop/Big_Data/TextAnalytics/Lyrics_Not_Processed/Lyrics/The Neighbourhood/Sweater Weather_The Neighbourhood", encoding="ISO-8859-1")

# for line printing
# print(song.read())

# per valutare le emozioni
# emoticon = te.get_emotion(song.read())
# print(emoticon)

# proviamo a ripulire il testo e poi proviamo a vedere che cosa esce fuori

# otteniamo le informazioni con genius API
# -0X7yZzbz_GMYpxs2YYqeK6LbNzdOLfpQTDiS313tX9ja9dgRv-o0SCRzhHuJ68HvUsfKow_swFF3OeHdunHSQ

# genius = Genius(" -0X7yZzbz_GMYpxs2YYqeK6LbNzdOLfpQTDiS313tX9ja9dgRv-o0SCRzhHuJ68HvUsfKow_swFF3OeHdunHSQ")
# song = genius.search_song("Sweater Weather")

# print(dir(song))
# print(song.stats)

#-----------------------------------------------------------------------------------------------

# UTILIZZO DI ITUNES PER OTTENERE INFORMAZIONI RIGUARDO AL GENERE MUSICALE
# import requests
# import statistics
# from statistics import mode

# # query the API
# apiquery = "http://itunes.apple.com/search?term="+"Back in Black"+"&media=music&entity=musicTrack&attribute=songTerm&limit=100"
# resp = requests.get(apiquery)

# while resp.status_code != 200:
#     # Something went wrong
#     print('GET /tasks/ {}'.format(resp.status_code))
#     time.sleep(120)
#     resp = requests.get(apiquery)

# results = resp.json()['results']
# #print("Number of results from itunes:", len(results))

# # qui conviene fare tipo una stima, prendiamo il valore che capita più spesso e quello sarà il genere della mia canzone
# genreRes = list()
# for res in results:
#     genreRes.append(res['primaryGenreName'])

# print(mode(genreRes))