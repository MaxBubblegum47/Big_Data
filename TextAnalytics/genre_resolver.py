import requests
import statistics
from statistics import mode
import os
import requests
import statistics
from numpy import savetxt
import pandas as pd
import numpy as np
import time
import shutil

# creiamo una simulazione con tutte le canzoni e vediamo
# che genere esce fuori ed inseriamo dentro un array

list_file=[]
list_file = [(root, files) for root, dirs, files in os.walk("/home/maxbubblegum/Big_Data/TextAnalytics/Lyrics_Not_Processed/Lyrics") if files] #set here the path of the directory of all your songs (if it contains other subdir no problem)
list_file.sort()


final_result = []

for path, files in list_file:
    for canzoni in files:
        # print(path+canzoni) percorso completo della canzone da spostare
        # print(canzoni.split('_')[0]) # stampa nomi di canzoni
        apiquery = "http://itunes.apple.com/search?term="+canzoni.split('_')[0]+"&media=music&entity=musicTrack&attribute=songTerm&limit=100"
        time.sleep(1)
        
        # funziona meglio usare direttamente un'altra rete (cellulare come hotspot) o una vpn
        proxy = {
            "https": 'https://222.234.220.170:3128',
            "http": 'https://103.16.160.121:10006',
            "http": 'https://149.56.233.29:3128',
            "http": 'https://134.238.252.143:8080'
        }
        
        resp = requests.get(apiquery)

        # resp = requests.get(apiquery)

        while resp.status_code != 200:
            # Something went wrong
            print('GET /tasks/ {}'.format(resp.status_code))

            resp = requests.get(apiquery)

        results = resp.json()['results']

        genreRes = []

        for res in results:
            try:
                genreRes.append(res['primaryGenreName'])
            except:
                genreRes.append("Unknown")

       
        if genreRes:
            genre = mode(genreRes)
        else: 
            genre = "Unknown"
        if "/" in genre:
            genre = genre.split("/")[0]
                
        final_dir = os.path.join("/home/maxbubblegum/Big_Data/TextAnalytics/Lyrics_Not_Processed/", genre)

        if not os.path.exists(final_dir):
            os.mkdir(final_dir)

        if genre and genre not in final_result:
            final_result.append(genre)
            pd.DataFrame(final_result).to_csv('genre.csv')
        else:
            print("Genere non esistente o gia' presente")

        source = os.path.join(path, canzoni)
        # print(source)
        # print(final_dir)

        if os.path.isfile(source) and source not in final_dir:
            print("Moving files from: " + source + " to: " + final_dir)                      
            shutil.move(source, final_dir) 


print(final_result)