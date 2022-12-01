#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 20:19:52 2022

@author: maxbubblegum
"""

import pandas as pd
import matplotlib.pyplot as plt

col_list = ["GEO", "TIME", "ISCED11", "Value"]
df = pd.read_csv ("/home/maxbubblegum/Desktop/Data_Analytics_LorenzoStigliano_136174/grad_percent/edat_lfse_03_1_Data.csv", usecols = col_list, encoding="iso-8859-1")

df_fr = df.copy()
df_de = df.copy()

df = df.loc[(df["GEO"] == "Italy") & (df["ISCED11"] == "Tertiary education (levels 5-8)")]
df["Value"] = (df["Value"].str.split()).apply(lambda x: (x[0].replace(':', '0')))
df["Value"] = df["Value"].astype(float)


#--------------------------
df_fr = df_fr.loc[(df_fr["GEO"] == "France") & (df_fr["ISCED11"] == "Tertiary education (levels 5-8)")]
df_fr["Value"] = (df_fr["Value"].str.split()).apply(lambda x: (x[0].replace(':', '0')))
df_fr["Value"] = df_fr["Value"].astype(float)
df_fr.plot(x="TIME", y="Value")

#---------------------------

df_de = df_de.loc[(df_de["GEO"] == "Spain") & (df_de["ISCED11"] == "Tertiary education (levels 5-8)")]
df_de["Value"] = (df_de["Value"].str.split()).apply(lambda x: (x[0].replace(':', '0')))
df_de["Value"] = df_de["Value"].astype(float)




res = pd.DataFrame()
res = pd.merge(df, df_fr, on="TIME")
res_tmp = pd.merge(res, df_de, on="TIME")

print(res_tmp)
res_tmp.to_csv("res_timeseries.csv")

res_tmp.plot(x="TIME", y=["Value_x", "Value_y", "Value"],
        kind="line", figsize=(10, 10))
 
# display plot
plt.show()


df_min_max_scaled = res_tmp.copy()

column = "Value_x"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    

column = "Value_y"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    

column = "Value"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    
 
# plot cannabis use + drug related crimes commited
grafico = df_min_max_scaled
grafico.plot(x="TIME", y=["Value_x", "Value_y", "Value"],
        kind="line", figsize=(10, 10))
