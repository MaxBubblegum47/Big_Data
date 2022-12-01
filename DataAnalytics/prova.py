import geopandas as gpd
import plotly.express as px
import pycountry
import numpy as np 
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn import preprocessing
import seaborn as sns

# =============================================================================

# CRIME
read_file = pd.read_excel ("10.1_-_Drug_related_crimes.xlsx")
read_file.to_csv ("Drug_related_crimes.csv", index = None, header=True)  
crimes = pd.DataFrame(pd.read_csv("Drug_related_crimes.csv"))
col_list = ["Region", "Country/Territory", "Total", "Year"]
crimes = pd.read_csv("Drug_related_crimes.csv", usecols = col_list)
crimes_tmp = crimes.groupby(["Region", "Country/Territory"]).agg({"Total": "sum"}).reset_index()
res_crimes = crimes_tmp.loc[(crimes_tmp["Region"] == "Europe")]
res_crimes = res_crimes.rename(columns={"Total": "Crimes"})

print(res_crimes)

# =============================================================================

# CANNABIS
read_file = pd.read_excel ("1.2_-_Prevalence_of_drug_use_in_the_general_population_including_NPS_national_data.xlsx", sheet_name="Cannabis")
read_file.to_csv ("cannabis_use.csv", index = None, header=True)  
cannabis_use = pd.DataFrame(pd.read_csv("cannabis_use.csv"))

cannabis_use = cannabis_use.drop(index = [0,1])

cannabis_use["Unnamed: 3"] = cannabis_use["Unnamed: 3"].apply(pd.to_numeric)

cannabis_use_tmp = cannabis_use.groupby(["Unnamed: 2"]).agg({"Unnamed: 3": "mean"}).reset_index()
res_cannabis_use = cannabis_use_tmp.sort_values("Unnamed: 3", ascending=False)
res_cannabis_use = res_cannabis_use.rename(columns={"Unnamed: 3": "Cannabis Use"})
res_cannabis_use = res_cannabis_use.rename(columns={"Unnamed: 2": "Country/Territory"})

# join crimes and cannabis use
crime_and_cannabis = pd.merge(res_crimes, res_cannabis_use, on="Country/Territory")


# normalised data of number of drug related crimes and cannabis use
df_min_max_scaled = crime_and_cannabis.copy()
column = "Crimes"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    
column = "Cannabis Use"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
 
# plot cannabis use + drug related crimes commited
grafico = df_min_max_scaled.sort_values(by="Crimes", ascending=False)
grafico.plot(x="Country/Territory", y=["Crimes", "Cannabis Use"], kind="bar")

input_countries = df_min_max_scaled["Country/Territory"]

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country, 'Unknown code') for country in input_countries]


df_min_max_scaled["Code"] = codes

#-----------------------------------------------------
# PLOTTING THE WORLD



df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
df_world = df_world[df_world.continent == "Europe"]

print(df_world["name"])

df_world_teams = df_world.merge(df_min_max_scaled, how="left", left_on=['iso_a3'], right_on=['Code'])

ax = df_world["geometry"].boundary.plot(figsize=(20,16))

df_world_teams.plot(column="Cannabis Use", ax=ax, cmap='Greens', 
                     legend=True, legend_kwds={"label": "Participation", "orientation":"horizontal"})

ax.set_title("Countries Crimes")

df_world_teams.to_csv("tmp.csv", sep='\t')