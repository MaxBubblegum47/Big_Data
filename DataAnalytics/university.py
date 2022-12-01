#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:54:38 2022

@author: maxbubblegum
"""

import pandas as pd
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

print(res_university_data.sort_values(by="Total Students", ascending=False))