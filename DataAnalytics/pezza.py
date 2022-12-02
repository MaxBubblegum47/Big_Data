df_min_max_scaled_presc_tranq_sed = tranq_sed_use.copy()
column = "Tranquillizers and sedatives"
df_min_max_scaled_presc_tranq_sed[column] = (df_min_max_scaled_presc_tranq_sed[column] - df_min_max_scaled_presc_tranq_sed[column].min()) / (df_min_max_scaled_presc_tranq_sed[column].max() - df_min_max_scaled_presc_tranq_sed[column].min())
 
# rinominazione di alcuni territori
df_min_max_scaled_presc_tranq_sed['Country/Territory'] = df_min_max_scaled_presc_tranq_sed['Country/Territory'].replace(['United Kingdom (England and Wales)'], 'United Kingdom')
df_min_max_scaled_presc_tranq_sed['Country/Territory'] = df_min_max_scaled_presc_tranq_sed['Country/Territory'].replace(['United States of America'], 'United States')
df_min_max_scaled_presc_tranq_sed['Country/Territory'] = df_min_max_scaled_presc_tranq_sed['Country/Territory'].replace(['Bolivia (Plurinational State of)'], 'Bolivia')
df_min_max_scaled_presc_tranq_sed['Country/Territory'] = df_min_max_scaled_presc_tranq_sed['Country/Territory'].replace(['Iran (Islamic Republic of)'], 'Iran')
df_min_max_scaled_presc_tranq_sed['Country/Territory'] = df_min_max_scaled_presc_tranq_sed['Country/Territory'].replace(['China, Taiwan Province of China'], 'China')

# rinominazione dei territori seguendo indicazioni ISO alpha 3
input_countries = df_min_max_scaled_presc_tranq_sed["Country/Territory"]

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country, 'Unknown code') for country in input_countries]

df_min_max_scaled_presc_tranq_sed["Code"] = codes

# rappresentazione grafica planisfero  
df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

df_world = df_world.merge(df_min_max_scaled_presc_tranq_sed, how="left", left_on=['iso_a3'], right_on=['Code'])

ax = df_world["geometry"].boundary.plot(figsize=(20,16))

df_world.plot(column="Tranquillizers and sedatives", ax=ax, cmap='BuPu', 
                     legend=True, legend_kwds={"label": "Use", "orientation":"horizontal"})

ax.set_title("Utilizzo Tranquillanti e Sedativi")