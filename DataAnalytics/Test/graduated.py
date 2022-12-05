#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:46:04 2022

@author: maxbubblegum
"""
import pandas as pd
import geopandas as gpd
import pycountry

col_list = ["GEO", "TIME", "ISCED11", "Value"]
df = pd.read_csv ("/home/maxbubblegum/Desktop/Data_Analytics_LorenzoStigliano_136174/grad_percent/edat_lfse_03_1_Data.csv", usecols = col_list, encoding="iso-8859-1")

df = df.loc[(df["TIME"] == 2020) & (df["ISCED11"] == "Tertiary education (levels 5-8)")]


df['GEO'] = df['GEO'].replace(['Germany (until 1990 former territory of the FRG)'], 'Germany')

# fix country code
input_countries = df["GEO"]

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country, 'Unknown code') for country in input_countries]

df["Code"] = codes

df  = df.drop(index = [2105])
df  = df.drop(index = [2099])
df  = df.drop(index = [2093])



df_min_max_scaled = df.copy()

df_min_max_scaled["Value"] = df["Value"].astype(float)

column = "Value"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    

df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
df_world = df_world[df_world.continent == "Europe"]



df_world_teams = df_world.merge(df, how="left", left_on=['iso_a3'], right_on=['Code'])

ax = df_world["geometry"].boundary.plot(figsize=(20,16))

df_world_teams.plot(column="Value", ax=ax, cmap='Blues')

ax.set_title("Graduated Tertiary")

print(df.sort_values("Value", ascending=False))


