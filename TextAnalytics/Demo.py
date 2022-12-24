import os
import text2emotion as te
from lyricsgenius import Genius
# to print all the file
# list_file=[]
# list_file = [(root, files) for root, dirs, files in os.walk("/home/maxbubblegum/Desktop/Big_Data/TextAnalytics/Lyrics_Not_Processed") if files] #set here the path of the directory of all your songs (if it contains other subdir no problem)
# list_file.sort()
# print(list_file)

# for path, files in list_file:
#     print(path)
#     for canzoni in files:
#         file = open(path +"/" + str(canzoni),"r", encoding="ISO-8859-1") # encoding per windows
#         print(canzoni) # stampa nomi di canzoni
#         print(file.read()) # stampa path della canzone
#         # righe = file.read()
#         # words = righe.split()
        
#         # print(righe)


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

import requests
import statistics
from statistics import mode

# query the API
apiquery = "http://itunes.apple.com/search?term="+"Back in Black AC/DC"+"&media=music&entity=musicTrack&attribute=songTerm&limit=100"
resp = requests.get(apiquery)

while resp.status_code != 200:
    # Something went wrong
    print('GET /tasks/ {}'.format(resp.status_code))
    time.sleep(120)
    resp = requests.get(apiquery)

results = resp.json()['results']
#print("Number of results from itunes:", len(results))

# qui conviene fare tipo una stima, prendiamo il valore che capita più spesso e quello sarà il genere della mia canzone
genreRes = list()
for res in results:
    genreRes.append(res['primaryGenreName'])

print(mode(genreRes))