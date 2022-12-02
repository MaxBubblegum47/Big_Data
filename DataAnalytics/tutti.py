import pandas as pd
import matplotlib.pyplot as plt

'''
si legge in input il documento in formato xlsx scegliendo il foglio relativo
all'utilizzo della cannabis
'''
read_file = pd.read_excel ("1.2_-_Prevalence_of_drug_use_in_the_general_population_including_NPS_national_data.xlsx", sheet_name="Cannabis")

# si effettua una conversione del doumento in formato csv
read_file.to_csv ("cannabis_use.csv", index = None, header=True)  

cannabis_use = pd.DataFrame(pd.read_csv("cannabis_use.csv"))

# pulizia del testo da informazioni accessorie
cannabis_use = cannabis_use.drop(index = [0,1])

# rinominazione delle colonne per una migliore lettura
cannabis_use = cannabis_use.rename(columns={"Unnamed: 8": "TIME"})
cannabis_use = cannabis_use.rename(columns={"Unnamed: 3": "Cannabis Use"})
cannabis_use = cannabis_use.rename(columns={"Unnamed: 2": "Country/Territory"})

# conversione della colonna 3 da stringhe a valore numerico
cannabis_use["Cannabis Use"] = cannabis_use["Cannabis Use"].apply(pd.to_numeric)

cannabis_use.drop(['Unnamed: 1', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 9', 'Unnamed: 10'
, 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13'], axis=1, inplace=True)

# ordinamento in base alla percentuale di utilizzo
number_of_country = 0
for i, j in cannabis_use.iterrows():
    c = j["Country/Territory"]     
    cannabis_tmp = cannabis_use.copy()
    cannabis_tmp = cannabis_tmp.loc[cannabis_tmp["Country/Territory"] == c]
    cannabis_tmp = cannabis_tmp.sort_values(by="TIME")
    cannabis_tmp.plot(x="TIME", y=["Cannabis Use"], kind = "line", figsize=(10,10))
    
    number_of_country += 1
    if number_of_country == 10:
        break


# devo fare un loop su tutti gli stati

# df = df.loc[(df["GEO"] == "Italy") & (df["ISCED11"] == "Tertiary education (levels 5-8)")]
# df["Value"] = (df["Value"].str.split()).apply(lambda x: (x[0].replace(':', '0')))
# df["Value"] = df["Value"].astype(float)

# res_tmp = pd.merge(res, df_de, on="TIME")
