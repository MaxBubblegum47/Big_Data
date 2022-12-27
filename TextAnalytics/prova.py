import os

list_file=[]
list_file = [(root, files) for root, dirs, files in os.walk("/home/maxbubblegum/Desktop/Big_Data/TextAnalytics/Lyrics_Not_Processed") if files] #set here the path of the directory of all your songs (if it contains other subdir no problem)
list_file.sort()

for path, files in list_file:
    print(path)
    for canzoni in files:
        file = open(path +"/" + str(canzoni),"r", encoding="ISO-8859-1") # encoding per windows
        print(canzoni) # stampa nomi di canzoni
        print(file.read()) # stampa path della canzone
        # righe = file.read()
        # words = righe.split()
        
        # print(righe)