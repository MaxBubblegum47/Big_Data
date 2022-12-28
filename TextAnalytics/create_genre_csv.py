import os
import csv

directory_list = list()
for root, dirs, files in os.walk("/home/maxbubblegum/Big_Data/TextAnalytics/Lyrics_Not_Processed/", topdown=False):
    for name in dirs:
        directory_list.append(os.path.join(root, name))

genre = list()
for elem in directory_list:
    # stampa dei generi musicali appena formati
    genre.append(elem.split("/")[-1:])

genre.sort()

with open('music_genre.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(genre)
