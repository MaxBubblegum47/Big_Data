import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

# =============================================================================

# CRIME
read_file = pd.read_excel ("10.1_-_Drug_related_crimes.xlsx")
read_file.to_csv ("Drug_related_crimes.csv", index = None, header=True)  
crimes = pd.DataFrame(pd.read_csv("Drug_related_crimes.csv"))
col_list = ["Region", "Country/Territory", "Total", "Year"]
crimes = pd.read_csv("Drug_related_crimes.csv", usecols = col_list)
crimes_tmp = crimes.groupby(["Region", "Country/Territory", "Year"]).agg({"Total": "sum"}).reset_index()
res_crimes = crimes_tmp.loc[(crimes_tmp["Region"] == "Europe") & (crimes_tmp["Year"] == "2020")]
res_crimes = res_crimes.rename(columns={"Total": "Crimes"})

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

# =============================================================================

# COCAINE

read_file = pd.read_excel ("1.2_-_Prevalence_of_drug_use_in_the_general_population_including_NPS_national_data.xlsx", sheet_name="Cocaine")
read_file.to_csv ("cocaine_use.csv", index = None, header=True)  
cocaine_use = pd.DataFrame(pd.read_csv("cocaine_use.csv"))

cocaine_use = cocaine_use.drop(index = [0,1])

cocaine_use["Unnamed: 3"] = cocaine_use["Unnamed: 3"].apply(pd.to_numeric)

cocaine_use_tmp = cocaine_use.groupby(["Unnamed: 2"]).agg({"Unnamed: 3": "mean"}).reset_index()
res_cocaine_use = cocaine_use_tmp.sort_values("Unnamed: 3", ascending=False)
res_cocaine_use = res_cocaine_use.rename(columns={"Unnamed: 3": "Cocaine Use"})
res_cocaine_use = res_cocaine_use.rename(columns={"Unnamed: 2": "Country/Territory"})

# join crimes and cannabis use
crime_and_cocaine = pd.merge(res_crimes, res_cocaine_use, on="Country/Territory")


# normalised data of number of drug related crimes and cannabis use
df_min_max_scaled = crime_and_cocaine.copy()
column = "Crimes"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    
column = "Cocaine Use"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
 
# plot cannabis use + drug related crimes commited
grafico = df_min_max_scaled.sort_values(by="Crimes", ascending=False)
grafico.plot(x="Country/Territory", y=["Crimes", "Cocaine Use"], kind="bar")


# =============================================================================

# AMPHETAMINES
read_file = pd.read_excel ("1.2_-_Prevalence_of_drug_use_in_the_general_population_including_NPS_national_data.xlsx", sheet_name="Amphetamines")
read_file.to_csv ("amphetamines_use.csv", index = None, header=True)  
amphetamines_use = pd.DataFrame(pd.read_csv("amphetamines_use.csv"))

amphetamines_use = amphetamines_use.drop(index = [0,1])

amphetamines_use["Unnamed: 3"] = amphetamines_use["Unnamed: 3"].apply(pd.to_numeric)

amphetamines_use_tmp = amphetamines_use.groupby(["Unnamed: 2"]).agg({"Unnamed: 3": "mean"}).reset_index()
res_amphetamines_use = amphetamines_use_tmp.sort_values("Unnamed: 3", ascending=False)
res_amphetamines_use = res_amphetamines_use.rename(columns={"Unnamed: 3": "Amphetamines Use"})
res_amphetamines_use = res_amphetamines_use.rename(columns={"Unnamed: 2": "Country/Territory"})

# join crimes and cannabis use
crime_and_amphetamines = pd.merge(res_crimes, res_amphetamines_use, on="Country/Territory")


# normalised data of number of drug related crimes and cannabis use
df_min_max_scaled = crime_and_amphetamines.copy()
column = "Crimes"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    
column = "Amphetamines Use"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
 
# plot cannabis use + drug related crimes commited
grafico = df_min_max_scaled.sort_values(by="Crimes", ascending=False)
grafico.plot(x="Country/Territory", y=["Crimes", "Amphetamines Use"], kind="bar")

# =============================================================================

# ECSTASY

read_file = pd.read_excel ("1.2_-_Prevalence_of_drug_use_in_the_general_population_including_NPS_national_data.xlsx", sheet_name="Ecstasy")
read_file.to_csv ("ecstasy_use.csv", index = None, header=True)  
ecstasy_use = pd.DataFrame(pd.read_csv("ecstasy_use.csv"))

ecstasy_use = ecstasy_use.drop(index = [0,1])

ecstasy_use["Unnamed: 3"] = ecstasy_use["Unnamed: 3"].apply(pd.to_numeric)

ecstasy_use_tmp = ecstasy_use.groupby(["Unnamed: 2"]).agg({"Unnamed: 3": "mean"}).reset_index()
res_ecstasy_use = ecstasy_use_tmp.sort_values("Unnamed: 3", ascending=False)
res_ecstasy_use  = res_ecstasy_use.rename(columns={"Unnamed: 3": "Ecstasy Use"})
res_ecstasy_use  = res_ecstasy_use.rename(columns={"Unnamed: 2": "Country/Territory"})

# join crimes and cannabis use
crime_and_ecstasy = pd.merge(res_crimes, res_ecstasy_use , on="Country/Territory")


# normalised data of number of drug related crimes and cannabis use
df_min_max_scaled = crime_and_ecstasy.copy()
column = "Crimes"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    
column = "Ecstasy Use"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
 
# plot cannabis use + drug related crimes commited
grafico = df_min_max_scaled.sort_values(by="Crimes", ascending=False)
grafico.plot(x="Country/Territory", y=["Crimes", "Ecstasy Use"], kind="bar")



# =============================================================================

# OPIOIDS

read_file = pd.read_excel ("1.2_-_Prevalence_of_drug_use_in_the_general_population_including_NPS_national_data.xlsx", sheet_name="Opioids")
read_file.to_csv ("opioids_use.csv", index = None, header=True)  
opioids_use = pd.DataFrame(pd.read_csv("opioids_use.csv"))

opioids_use = opioids_use.drop(index = [0,1])

opioids_use["Unnamed: 3"] = opioids_use["Unnamed: 3"].apply(pd.to_numeric)

opioids_use_tmp = opioids_use.groupby(["Unnamed: 2"]).agg({"Unnamed: 3": "mean"}).reset_index()
res_opioids_use = opioids_use_tmp.sort_values("Unnamed: 3", ascending=False)
res_opioids_use = res_opioids_use.rename(columns={"Unnamed: 3": "Opioids Use"})
res_opioids_use = res_opioids_use.rename(columns={"Unnamed: 2": "Country/Territory"})

# join crimes and cannabis use
crime_and_opioids = pd.merge(res_crimes, res_opioids_use, on="Country/Territory")


# normalised data of number of drug related crimes and cannabis use
df_min_max_scaled = crime_and_opioids.copy()
column = "Crimes"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    
column = "Opioids Use"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
 
# plot cannabis use + drug related crimes commited
grafico = df_min_max_scaled.sort_values(by="Crimes", ascending=False)
grafico.plot(x="Country/Territory", y=["Crimes", "Opioids Use"], kind="bar")



# =============================================================================

# OPIATES

read_file = pd.read_excel ("1.2_-_Prevalence_of_drug_use_in_the_general_population_including_NPS_national_data.xlsx", sheet_name="Opiates")
read_file.to_csv ("opiates_use.csv", index = None, header=True)  
opiates_use = pd.DataFrame(pd.read_csv("opiates_use.csv"))

opiates_use  = opiates_use.drop(index = [0,1])

opiates_use["Unnamed: 3"] = opiates_use["Unnamed: 3"].apply(pd.to_numeric)

opiates_use_tmp = opiates_use.groupby(["Unnamed: 2"]).agg({"Unnamed: 3": "mean"}).reset_index()
res_opiates_use = opiates_use_tmp.sort_values("Unnamed: 3", ascending=False)
res_opiates_use = res_opiates_use.rename(columns={"Unnamed: 3": "Opiates Use"})
res_opiates_use = res_opiates_use.rename(columns={"Unnamed: 2": "Country/Territory"})

# join crimes and cannabis use
crime_and_opiates = pd.merge(res_crimes, res_opiates_use, on="Country/Territory")


# normalised data of number of drug related crimes and cannabis use
df_min_max_scaled = crime_and_opiates.copy()
column = "Crimes"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    
column = "Opiates Use"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
 
# plot cannabis use + drug related crimes commited
grafico = df_min_max_scaled.sort_values(by="Crimes", ascending=False)
grafico.plot(x="Country/Territory", y=["Crimes", "Opiates Use"], kind="bar")



# =============================================================================

# PRESCRIPTED OPIOIDS

read_file = pd.read_excel ("1.2_-_Prevalence_of_drug_use_in_the_general_population_including_NPS_national_data.xlsx", sheet_name="Prescription opioids")
read_file.to_csv ("prescription_opioids.csv", index = None, header=True)  
presc_opioids_use = pd.DataFrame(pd.read_csv("prescription_opioids.csv"))

presc_opioids_use  = presc_opioids_use.drop(index = [0,1])

presc_opioids_use["Unnamed: 3"] = presc_opioids_use["Unnamed: 3"].apply(pd.to_numeric)

presc_opioids_use_tmp = presc_opioids_use.groupby(["Unnamed: 2"]).agg({"Unnamed: 3": "mean"}).reset_index()
res_presc_opioids_use = presc_opioids_use_tmp.sort_values("Unnamed: 3", ascending=False)
res_presc_opioids_use = res_presc_opioids_use.rename(columns={"Unnamed: 3": "Prescription Opioids Use"})
res_presc_opioids_use = res_presc_opioids_use.rename(columns={"Unnamed: 2": "Country/Territory"})

# join crimes and cannabis use
crime_and_presc_opioids = pd.merge(res_crimes, res_presc_opioids_use, on="Country/Territory")


# normalised data of number of drug related crimes and cannabis use
df_min_max_scaled = crime_and_presc_opioids.copy()
column = "Crimes"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    
column = "Prescription Opioids Use"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
 
# plot cannabis use + drug related crimes commited
grafico = df_min_max_scaled.sort_values(by="Crimes", ascending=False)
grafico.plot(x="Country/Territory", y=["Crimes", "Prescription Opioids Use"], kind="bar")

 

# =============================================================================

# TRANQUILLANTS AND SEDATIVES

read_file = pd.read_excel ("1.2_-_Prevalence_of_drug_use_in_the_general_population_including_NPS_national_data.xlsx", sheet_name="Tranquillizers and sedatives")
read_file.to_csv ("tranquillizers_sedatives.csv", index = None, header=True)  
pollege_med_use = pd.DataFrame(pd.read_csv("tranquillizers_sedatives.csv"))

pollege_med_use  = pollege_med_use.drop(index = [0,1])

pollege_med_use["Unnamed: 3"] = pollege_med_use["Unnamed: 3"].apply(pd.to_numeric)

pollege_med_use_tmp = pollege_med_use.groupby(["Unnamed: 2"]).agg({"Unnamed: 3": "mean"}).reset_index()
res_pollege_med_use = pollege_med_use_tmp.sort_values("Unnamed: 3", ascending=False)
res_pollege_med_use = res_pollege_med_use.rename(columns={"Unnamed: 3": "Tranquillizers and Sedatives Use"})
res_pollege_med_use = res_pollege_med_use.rename(columns={"Unnamed: 2": "Country/Territory"})

# join crimes and cannabis use
crime_and_pollege_med = pd.merge(res_crimes, res_pollege_med_use, on="Country/Territory")


# normalised data of number of drug related crimes and cannabis use
df_min_max_scaled = crime_and_pollege_med.copy()
column = "Crimes"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    
column = "Tranquillizers and Sedatives Use"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
 
# plot cannabis use + drug related crimes commited
grafico = df_min_max_scaled.sort_values(by="Crimes", ascending=False)
grafico.plot(x="Country/Territory", y=["Crimes", "Tranquillizers and Sedatives Use"], kind="bar")

# =============================================================================

# UNIVERSITY (BACHELOR, MASTER DEGREE AND DOCTORAL)

col_list = ["GEO", "ISCED11", "TIME", "Value"]
university_data = pd.read_csv("educ_uoe_enrt03_1_Data.csv", usecols = col_list, encoding="iso-8859-1")
university_data = university_data.groupby(["GEO", "ISCED11", "TIME"]).agg({"Value": "sum"}).reset_index() 
university_data = university_data.loc[(university_data["TIME"] == 2020)]

university_data_tmp1 = university_data.loc[(university_data["ISCED11"] == "Bachelor's or equivalent level")]
university_data_tmp1 = university_data_tmp1.rename(columns={"Value": "Bachelor Values"})

del university_data_tmp1["TIME"]
del university_data_tmp1["ISCED11"]

university_data_tmp2 = university_data.loc[(university_data["ISCED11"] == "Master's or equivalent level")]
university_data_tmp2 = university_data_tmp2.rename(columns={"Value": "Master Values"})

del university_data_tmp2["TIME"]
del university_data_tmp2["ISCED11"]

university_data_tmp3 = university_data.loc[(university_data["ISCED11"] == "Doctoral or equivalent level")]
university_data_tmp3 = university_data_tmp3.rename(columns={"Value": "Doctoral Values"})

del university_data_tmp3["TIME"]
del university_data_tmp3["ISCED11"]

res_university_data = pd.merge(university_data_tmp1, university_data_tmp2, on="GEO")
res_university_data = pd.merge(res_university_data, university_data_tmp3, on="GEO")

res_university_data["Bachelor Values"] = (res_university_data["Bachelor Values"].str.split()).apply(lambda x: (x[0].replace(':', '0')))
res_university_data["Master Values"] = (res_university_data["Master Values"].str.split()).apply(lambda x: (x[0].replace(':', '0')))
res_university_data["Doctoral Values"] = (res_university_data["Doctoral Values"].str.split()).apply(lambda x: (x[0].replace(':', '0')))

res_university_data["Bachelor Values"] = (res_university_data["Bachelor Values"].str.split()).apply(lambda x: (x[0].replace(',', '')))
res_university_data["Master Values"] = (res_university_data["Master Values"].str.split()).apply(lambda x: (x[0].replace(',', '')))
res_university_data["Doctoral Values"] = (res_university_data["Doctoral Values"].str.split()).apply(lambda x: (x[0].replace(',', '')))

res_university_data["Total Students"] = res_university_data["Bachelor Values"].astype(float) + res_university_data["Master Values"].astype(float) + res_university_data["Doctoral Values"].astype(float) 

res_university_data = res_university_data.drop(res_university_data.index[9])
res_university_data = res_university_data.drop(res_university_data.index[9])
res_university_data = res_university_data.drop(res_university_data.index[11])

# print check
# print(res_university_data.sort_values(by="Total Students", ascending=False))

# join crimes and university studente
res_university_data = res_university_data.rename(columns={"GEO": "Country/Territory"})
crime_and_university = pd.merge(res_crimes, res_university_data, on="Country/Territory")

# normalised data of number of drug related crimes and cannabis use
df_min_max_scaled = crime_and_university.copy()
column = "Crimes"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    
column = "Total Students"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
 
# plot cannabis use + drug related crimes commited
grafico = df_min_max_scaled.sort_values(by="Crimes", ascending=False)
grafico.plot(x="Country/Territory", y=["Crimes", "Total Students"], kind="bar")

# =============================================================================

# UNIVERSITY AND CANNABIS

university_and_cannabis = pd.merge(res_cannabis_use, res_university_data, on="Country/Territory")

df_min_max_scaled = university_and_cannabis.copy()
column = "Cannabis Use"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())    
column = "Total Students"
df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())

grafico = df_min_max_scaled.sort_values(by="Total Students", ascending=False)
grafico.plot(x="Country/Territory", y=["Cannabis Use", "Total Students"], kind="bar")
